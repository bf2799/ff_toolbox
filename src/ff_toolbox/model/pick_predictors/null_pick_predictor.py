"""Module for the Null Pick Predictor and its helpers."""

from ff_toolbox.model.core.draft import Draft
from ff_toolbox.model.core.phys_representations import Player, PlayerRanking
from ff_toolbox.model.pick_analyzers.abstract_pick_analyzer import AbstractPickAnalyzer
from ff_toolbox.model.pick_predictors.abstract_pick_predictor import (
    AbstractPickPredictor,
)
from ff_toolbox.model.rankings_generators.abstract_rankings_generator import (
    AbstractRankingsGenerator,
)


class NullPickPredictor(AbstractPickPredictor):
    """
    Pick predictor that assumes players will always be available in the future.

    Useful for eliminating pick prediction as a step dynamically without changing code dependent on having a pick predictor.
    """

    def __init__(
        self,
        my_pick_analyzer: AbstractPickAnalyzer,
        opp_pick_analyzer: AbstractPickAnalyzer,
        my_rankings: PlayerRanking,
        opp_rankings_generator: AbstractRankingsGenerator,
    ) -> None:
        """
        Takes in a set of my rankings/pick analyzer and opponent rankings generator/pick analyzer for consistent pick prediction use.

        :param my_pick_analyzer: How to analyze my picks for player value
        :param opp_pick_analyzer: How to analyze opponent picks for player value
        :param my_rankings: How my players are ranked
        :param opp_rankings_generator: How to generate rankings for opponent players
        """
        super().__init__(
            my_pick_analyzer, opp_pick_analyzer, my_rankings, opp_rankings_generator
        )

    def predict_picks(
        self, draft_status: Draft, num_picks: list[int]
    ) -> dict[Player, list[float]]:
        """
        Assign probability of 1 for availability of every undrafted player in draft

        :param draft_status: Current state of the draft
        :param num_picks: Number of picks into the future to predict (can be multiple picks to see availability at)
        :return: Dictionary of (player, probability of availability at each pick provided) pairs
        """
        return {player: [1] * len(num_picks) for player in draft_status.undrafted}
