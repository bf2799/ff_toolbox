"""Module to hold an abstract pick analyzer and any helper data types."""

from abc import ABC, abstractmethod

from src.model.core.phys_representations import Player, PlayerRanking, Roster
from src.model.core.settings import LeagueSettings


class AbstractPickAnalyzer(ABC):
    """
    Base class for a pick analyzer, outlinining all functions pick analyzers must implement.

    A pick analyzer evaluates a list of available players and assigns them a list of relative values.
    As input, 1 set of player rankings and 1 team roster are used to help pick analyzers change weighting based on context.
    """

    def __init__(self) -> None:
        """No-op"""
        pass

    @abstractmethod
    def eval_players(
        self,
        avail_players: list[Player],
        my_ranking: PlayerRanking,
        my_roster: Roster,
        settings: LeagueSettings,
    ) -> dict[Player, float]:
        """
        Evaluate players given inputs and output a list of those players with their relative values.

        :param avail_players: Players to evaluate
        :param my_ranking: Personal ranking of all players (can include non-available players)
        :param my_roster: Current roster construction of team evaluating players
        :param settings: League settings to abide by
        :return: Dictionary of (player, value) pairs
        """
        pass
