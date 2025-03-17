"""Module for simple pick suggestor and any dependencies."""

from typing import override

from ff_toolbox.model.core.draft import Draft
from ff_toolbox.model.core.phys_representations import Player
from ff_toolbox.model.pick_suggestors.abstract_pick_suggestor import (
    AbstractPickSuggestor,
)


class SimplePickSuggestor(AbstractPickSuggestor):
    """Simplest pick suggestor, taking player with most relative value regardless of draft context."""

    @override
    def get_suggestions(self, draft_status: Draft) -> dict[Player, float]:
        """Get player suggestions that are equivalent to "my rankings" of undrafted players.

        Params:
            draft_status (Draft): Current draft status

        Returns:
            dict[Player, float]: Dictionary of {undrafted_player, relative_suggestion_strength}, sorted by suggestion strength
        """
        player_rankings = self._my_pick_analyzer.eval_players(
            avail_players=draft_status.undrafted,
            my_ranking=self._pick_predictor.my_rankings,
            my_roster=draft_status.pick_num_to_team(
                pick_num=len(draft_status.drafted)
            ).roster,
            settings=draft_status.settings,
        )
        return dict(sorted(player_rankings.items(), key=lambda x: x[1], reverse=True))
