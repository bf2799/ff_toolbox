"""Module for an abstract rankings generator and its unique dependencies."""
from abc import ABC, abstractmethod

from src.model.core.phys_representations import PlayerRanking


class AbstractRankingsGenerator(ABC):
    """
    Base class for a rankings generator,outlinining all functions and values rankings generators must implement.

    A rankings generator takes a set of consensus rankings and shuffles it during the generate_rankings function.
    Different rankings generators will have different algorithms the random shuffle is based on.
    """

    def __init__(self, consensus_rankings: PlayerRanking) -> None:
        """
        Hold a set of consensus rankings for the rankings generators

        :param consensus_rankings: Consensus rankings to base generator shufflings off of
        """
        self._consensus_rankings: PlayerRanking = consensus_rankings

    @abstractmethod
    def generate_rankings(self) -> PlayerRanking:
        """
        Generate rankings based off consensus rankings

        :return: Shuffled player ranking
        """
        pass
