"""Module for holding abstract pick predictor and any helpers it needs."""

from abc import ABC, abstractmethod

from ff_toolbox.model.core.draft import Draft
from ff_toolbox.model.core.phys_representations import Player, PlayerRanking
from ff_toolbox.model.pick_analyzers.abstract_pick_analyzer import AbstractPickAnalyzer
from ff_toolbox.model.rankings_generators.abstract_rankings_generator import (
    AbstractRankingsGenerator,
)


class AbstractPickPredictor(ABC):
    """Base class for a pick predictor, outlinining all functions and values pick predictors must implement.

    A pick predictor predicts the probability each player will be available x more picks into the future in a draft.
    Selections are divided into "my" selections and "opponent" selections.
    "My" picks are predicted by passing "my rankings" into "my pick analyzer" for player values.
    "Opponent" picks are predicted by generating rankings using the "opponent rankings generator," passing that into the "opponent pick analyzer," and leveraging resulting player values.
    """

    def __init__(
        self,
        my_pick_analyzer: AbstractPickAnalyzer,
        opp_pick_analyzer: AbstractPickAnalyzer,
        my_rankings: PlayerRanking,
        opp_rankings_generator: AbstractRankingsGenerator,
    ) -> None:
        """Take in a set of my rankings/pick analyzer and opponent rankings generator/pick analyzer for consistent pick prediction use.

        Params:
            my_pick_analyzer (AbstractPickAnalyzer): How to analyze my picks for player value
            opp_pick_analyzer (AbstractPickAnalyzer): How to analyze opponent picks for player value
            my_rankings (PlayerRanking): How my players are ranked
            opp_rankings_generator (AbstractRankingsGenerator): How to generate rankings for opponent players
        """
        self._my_pick_analyzer: AbstractPickAnalyzer = my_pick_analyzer
        self._opp_pick_analyzer: AbstractPickAnalyzer = opp_pick_analyzer
        self._my_rankings: PlayerRanking = my_rankings
        self._opp_rankings_generator: AbstractRankingsGenerator = opp_rankings_generator

    @abstractmethod
    def predict_picks(
        self, draft_status: Draft, num_picks: list[int]
    ) -> dict[Player, list[float]]:
        """Calculate probability each player will be available num_picks into the future given current draft status.

        Params:
            draft_status (Draft): Current state of the draft
            num_picks (list[int]): Number of picks into the future to predict (can be multiple picks to see availability at)

        Returns:
            dict[Player, list[float]]: Dictionary of (player, probability of availability at each pick provided) pairs
        """

    @property
    def my_rankings(self) -> PlayerRanking:
        """Get my rankings as read-only.

        Returns:
            PlayerRanking: My rankings
        """
        return self._my_rankings
