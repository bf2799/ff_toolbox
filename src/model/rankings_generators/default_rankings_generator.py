"""Module for default rankings generator and any helpers needed."""

from src.model.core.phys_representations import PlayerRanking
from src.model.rankings_generators.abstract_rankings_generator import (
    AbstractRankingsGenerator,
)


class DefaultRankingsGenerator(AbstractRankingsGenerator):
    """
    Class to return default rankings exactly the same as consensus rankings.

    Useful for helping to simulate auto-picking.
    """

    def __init__(self, consensus_rankings: PlayerRanking) -> None:
        """
        Initializes parent class with consensus rankings.

        :param consensus_rankings:
        """
        super().__init__(consensus_rankings)

    def generate_rankings(self) -> PlayerRanking:
        """
        Generate rankings that are exactly the same as consensus rankings

        :return: Consensus player rankings
        """
        return self._consensus_rankings
