"""Module for the simple pick analyzer and any sub-classes it needs to leverage."""

from typing import override

from ff_toolbox.model.core.phys_representations import Player, PlayerRanking, Roster
from ff_toolbox.model.core.settings import LeagueSettings
from ff_toolbox.model.pick_analyzers.abstract_pick_analyzer import AbstractPickAnalyzer


class SimplePickAnalyzer(AbstractPickAnalyzer):
    """Assigns values to available players based on VOR. More detailed analysis of how this occurs will come."""

    @override
    def eval_players(
        self,
        avail_players: list[Player],
        my_ranking: PlayerRanking,
        my_roster: Roster,
        settings: LeagueSettings,
    ) -> dict[Player, float]:
        """Assign a VOR (value over replacement) to each player. More details to come.

        Params:
            avail_players (list[Player]): Players to evaluate
            my_ranking (PlayerRanking): Personal ranking of all players (can include non-available players)
            my_roster (Roster): Current roster construction of team evaluating players
            settings (LeagueSettings): League settings to abide by

        Returns:
            dict[Player, float]: Dictionary of (player, value) pairs
        """
        # Current fake implementation for sake of testing architectural development
        return {
            player: (
                0
                if player not in my_ranking.get_ovr_rankings()
                else (
                    len(my_ranking.get_ovr_rankings())
                    - my_ranking.get_ovr_rankings().index(player)
                )
            )
            for player in avail_players
        }
