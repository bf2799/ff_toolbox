"""Module to help map ranking distribution to fantasy points distributions and vice versa."""

import numpy as np
import numpy.typing as npt
import pandas as pd
import scipy as scp


class PointsRankingMapper:
    """
    Helps map distributions of points to rankings with a given value map.

    When using this class, it is assumed that both points and ranking distributions can be described by solely mean and variance.
    However, only points distributions are assumed to be Gaussian.
    The distribution of the ranking is assumed to be unknown, since it heavily depends on the given map.
    """

    # TODO: Add gamma as a distribution type
    _valid_points_dist_types: list[str] = ["gaussian"]

    def __init__(self, points: npt.NDArray[np.float64], points_dist_type: str) -> None:
        """
        Create a new mapper with the given map between "ranks" and "points".

        :param points: List of points, from rank 1 to rank n, where n is length of points array
        :param points_dist_type: One of "gaussian" or "gamma." Gaussian is useful for season-long points, while gamma is best for individual game points
        :raises ValueError: points_dist_type parameter is invalid value
        """
        # Smooth points with rolling blackman filter
        series_points: pd.Series = pd.Series(points)
        self._smoothed_points: npt.NDArray[np.float64] = (
            series_points.rolling(7, win_type="blackman", center=True, closed="both")
            .mean()
            .fillna(series_points)
        ).to_numpy()
        # Set points bins as midpoints between smoothed points
        self._points_bins: npt.NDArray[np.float64] = (
            np.add(self._smoothed_points[1:], self._smoothed_points[:-1]) / 2
        )
        # Set ranks to save computation time later
        self._ranks: npt.NDArray[np.float64] = np.array(
            range(1, self._smoothed_points.shape[0] + 1)
        )
        # Validate points distribution type
        if points_dist_type not in self._valid_points_dist_types:
            raise ValueError(
                f"Points distribution {points_dist_type} is invalid. Must be one of {self._valid_points_dist_types}"
            )
        self._points_dist_type: str = points_dist_type

    def points_to_rank_mean(
        self, points_means: npt.NDArray[np.float64]
    ) -> npt.NDArray[np.float64]:
        """
        Convert points mean to ranking mean.

        :param points_means: Mean point(s)
        :return: Mean ranks for given points
        """
        return np.interp(
            points_means,
            xp=np.flip(self._smoothed_points),
            fp=np.flip(self._ranks),
        )

    def rank_to_points_mean(
        self, rank_means: npt.NDArray[np.float64]
    ) -> npt.NDArray[np.float64]:
        """
        Convert ranking mean to points mean.

        :param rank_means: Mean ranking(s)
        :return: Mean points for given ranks
        """
        return np.interp(
            rank_means,
            xp=self._ranks,
            fp=self._smoothed_points,
        )

    def points_to_rank_variance(
        self, points_variance: float, points_mean: float
    ) -> float:
        """
        Find the rank variance given a mean and variance of points scored.

        :param points_variance: Variance of points
        :param points_mean: Mean of points
        :return: Variance of rank
        """
        # Using points distribution type, mean, and variance, find probability of being in each rank bin
        bin_cdfs: npt.NDArray[np.float64] = np.zeros(self._smoothed_points.shape[0] - 2)
        match self._points_dist_type:
            case "gaussian":
                norms: npt.NDArray[np.float64] = (
                    self._points_bins - points_mean
                ) / np.sqrt(points_variance)
                bin_cdfs = scp.stats.norm.cdf(norms)

        rank_probs: npt.NDArray[np.float64] = np.r_[
            1 - bin_cdfs[0], -np.diff(bin_cdfs), bin_cdfs[-1]
        ]

        # Find weighted variance of probabilities of being at each rank to determine rank variance
        rank_mean: float = self.points_to_rank_mean(np.array([points_mean]))[0]
        # Variance is sum of squares / sum(weights), but sum(weights) is just 1 in this case
        variance: float = np.sum(
            np.multiply(np.power(self._ranks - rank_mean, 2), rank_probs)
        )
        return variance

    def rank_to_points_variance(self, rank_variance: float, rank_mean: float) -> float:
        """
        Find the points variance given a mean and variance of ranking.

        :param rank_variance: Variance of ranking
        :param rank_mean: Mean of ranking
        :raises: RuntimeError: Minimization calculation couldn't finish
        :return: Variance of points
        """

        def _points_to_rank_variance_error(
            points_variance: float, points_mean: float, target_rank_variance: float
        ) -> float:
            return abs(
                self.points_to_rank_variance(points_variance, points_mean)
                - target_rank_variance
            )

        # Initial guess for 1 points STDEV = points @ (rank mean + 1 rank STDEV) - points @ rank_mean
        #   1 points VAR = (1 points STDEV)^2
        initial_var_guess = (
            self.rank_to_points_mean(rank_mean + np.sqrt(rank_variance))
            - self.rank_to_points_mean(np.array([rank_mean]))
        ) ** 2
        # Minimize rank variance error of (variance parameter to points_to_rank_variance - rank_variance)
        result: scp.optimize.OptimizeResult = scp.optimize.minimize(
            _points_to_rank_variance_error,
            initial_var_guess,
            args=(
                self.rank_to_points_mean(np.array([rank_mean])),
                rank_variance,
            ),
            method="Nelder-Mead",
            tol=1e-2,
        )
        if not result.success:
            raise RuntimeError("Minimization of rank variance error couldn't converge")
        # We only have 1 variance passed in to minimization, so taking 0th element will always work
        return float(result.x[0])

    def rank_confidence_intervals(
        self,
        rank_means: npt.NDArray[np.float64],
        rank_variances: npt.NDArray[np.float64],
        confidence: float,
    ) -> npt.NDArray[np.float64]:
        """
        Calculate the confidence interval boundaries of players' ranks, given their rank means and variances.

        :param rank_means: Mean rank(s) of shape (n,1)
        :param rank_variances: Mean variance(s) of shape (n,1). Must be same length as means
        :param confidence: Confidence from 0-1
        :return: 2-D array of shape (n,2), where n = length of inputs, 2 dimensions are lower/upper rank interval boundaries
        """
        # Validate parameters
        if rank_means.shape != rank_variances.shape:
            raise ValueError(
                f"Rank Mean shape {rank_means.shape} and Rank Variances shape {rank_variances.shape} do not match"
            )
        if not (0 <= confidence <= 1):
            raise ValueError(
                f"Confidence should in interval of 0-1. It is {confidence}"
            )

        # Calculate point means and standard deviations
        point_means: npt.NDArray[np.float64] = self.rank_to_points_mean(rank_means)
        point_stdevs: npt.NDArray[np.float64] = np.sqrt(
            np.array(
                [
                    self.rank_to_points_variance(var, mean)
                    for mean, var in zip(rank_means, rank_variances)
                ]
            )
        )

        # Convert point means, point stdevs, and confidence into rank boundaries
        ranks: npt.NDArray[np.float64] = np.zeros([point_means.shape[0], 2])
        match self._points_dist_type:
            case "gaussian":
                stdevs: float = scp.stats.norm.ppf((1 + confidence) / 2)
                high_ranks = self.points_to_rank_mean(
                    point_means + point_stdevs * stdevs
                )
                low_ranks = self.points_to_rank_mean(
                    point_means - point_stdevs * stdevs
                )
                ranks = np.transpose(np.vstack((high_ranks, low_ranks)))
        return ranks


points = np.array(
    [
        323.2841185,
        290.590578,
        267.3593978,
        253.8683827,
        243.0641088,
        232.6697426,
        229.1015056,
        226.6911122,
        222.0704225,
        219.3224866,
        213.3166586,
        209.9305488,
        207.9995143,
        207.3759106,
        205.5628946,
        204.348713,
        201.4939291,
        197.7901894,
        196.5973774,
        193.163186,
        190.5687227,
        187.8227295,
        185.7445362,
        183.4774162,
        181.8251578,
        180.6221467,
        178.9660029,
        174.8285576,
        172.0733366,
        171.1287033,
        166.867897,
        163.405051,
        161.9286061,
        158.8523555,
        157.2146673,
        153.9281204,
        152.9446333,
        151.9805731,
        151.1976688,
        146.9737737,
        145.6799417,
        144.621661,
        142.7153958,
        140.7576493,
        139.1704711,
        137.9956289,
        136.5225838,
        135.8824672,
        133.9606605,
        132.0349684,
        129.569694,
        128.2831472,
        127.0325401,
        124.0509956,
        122.8455561,
        120.1262749,
        118.4808159,
        116.86644,
        115.6833414,
        114.9820301,
        113.9271491,
        112.1714424,
        111.3477416,
        109.7843613,
        109.3268577,
        107.3098592,
        105.6338028,
        105.3929092,
        103.9528898,
        100.7173385,
        99.38125304,
        98.74696455,
        96.4511899,
        93.77610491,
        92.91452161,
        91.41962118,
        90.45798932,
        89.57503643,
        88.5381253,
        87.31228752,
        86.85672657,
        86.00291404,
        85.37688198,
        82.21709568,
        81.29431763,
        79.22389509,
        77.77610491,
        77.16124332,
        74.44973288,
        73.76930549,
        72.35551238,
        71.40165129,
        68.9057795,
        67.96260321,
        67.18941234,
        63.27974745,
    ]
)
mapper = PointsRankingMapper(points, "gaussian")
rank_means_ = np.array([66.2, 62.1, 58.2, 64.5, 57.5, 56.1, 55.6, 62.2, 54.5, 49.0])
rank_stdevs = np.array([5.9, 12.9, 6.2, 6.4, 6.4, 8.6, 3.9, 4.7, 6.3, 5.5])
rank_vars = np.power(rank_stdevs, 2)

ranks = mapper.rank_confidence_intervals(rank_means_, rank_vars, 0.8)
for val in ranks[:, 0]:
    print(val)
for val in ranks[:, 1]:
    print(val)
