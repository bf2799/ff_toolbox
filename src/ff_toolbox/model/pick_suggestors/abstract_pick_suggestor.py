"""Module for the abstract pick suggestor and its dependencies."""

from abc import ABC, abstractmethod

from ff_toolbox.model.core.draft import Draft
from ff_toolbox.model.core.phys_representations import Player
from ff_toolbox.model.pick_analyzers.abstract_pick_analyzer import AbstractPickAnalyzer
from ff_toolbox.model.pick_predictors.abstract_pick_predictor import (
    AbstractPickPredictor,
)


class AbstractPickSuggestor(ABC):
    """
    Base class for suggesting picks.

    Pick suggestions have access to pick predictors and pick analyzers to suggest picks.
    Their algorithms will likely combine pick predictors x rounds in the future with the pick analyzer to produce
    a more comprehensive relative score for each undrafted player.
    """

    def __init__(
        self,
        my_pick_analyzer: AbstractPickAnalyzer,
        pick_predictor: AbstractPickPredictor,
    ) -> None:
        """
        Determine which pick analyzer and pick predictor to use for this pick suggestor.

        :param my_pick_analyzer: Pick analyzer to use
        :param pick_predictor: Pick predictor to use
        """
        self._my_pick_analyzer: AbstractPickAnalyzer = my_pick_analyzer
        self._pick_predictor: AbstractPickPredictor = pick_predictor

    @abstractmethod
    def get_suggestions(self, draft_status: Draft) -> dict[Player, float]:
        """
        Calculate overall relative player rating for every available player in the draft.

        :param draft_status: Current draft
        :return: All (player, relative score) pairs for available players in draft
        """
        pass
