"""Module for the Null Pick Predictor and its helpers."""

from typing import override

from ff_toolbox.model.core.draft import Draft
from ff_toolbox.model.core.phys_representations import Player
from ff_toolbox.model.pick_predictors.abstract_pick_predictor import (
    AbstractPickPredictor,
)


class NullPickPredictor(AbstractPickPredictor):
    """Pick predictor that assumes players will always be available in the future.

    Useful for eliminating pick prediction as a step dynamically without changing code dependent on having a pick predictor.
    """

    @override
    def predict_picks(
        self, draft_status: Draft, num_picks: list[int]
    ) -> dict[Player, list[float]]:
        """Assign probability of 1 for availability of every undrafted player in draft.

        Params:
            draft_status (Draft): Current state of the draft
            num_picks (list[int]): Number of picks into the future to predict (can be multiple picks to see availability at)

        Returns:
            dict[Player, list[float]]: Dictionary of (player, probability of availability at each pick provided) pairs
        """
        return {player: [1] * len(num_picks) for player in draft_status.undrafted}
