"""Module for simple pick suggestor and any dependencies."""

from src.model.core.draft import Draft
from src.model.core.phys_representations import Player
from src.model.pick_analyzers.abstract_pick_analyzer import AbstractPickAnalyzer
from src.model.pick_predictors.abstract_pick_predictor import AbstractPickPredictor
from src.model.pick_suggestors.abstract_pick_suggestor import AbstractPickSuggestor


class SimplePickSuggestor(AbstractPickSuggestor):
    def __init__(
        self,
        my_pick_analyzer: AbstractPickAnalyzer,
        pick_predictor: AbstractPickPredictor,
    ) -> None:
        super().__init__(my_pick_analyzer, pick_predictor)

    def get_suggestions(self, draft_status: Draft) -> dict[Player, float]:
        pass
