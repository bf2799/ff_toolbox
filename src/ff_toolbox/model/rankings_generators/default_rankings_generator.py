"""Module for default rankings generator and any helpers needed."""

from typing import override

from ff_toolbox.model.core.phys_representations import PlayerRanking
from ff_toolbox.model.rankings_generators.abstract_rankings_generator import (
    AbstractRankingsGenerator,
)


class DefaultRankingsGenerator(AbstractRankingsGenerator):
    """Class to return default rankings exactly the same as consensus rankings.

    Useful for helping to simulate auto-picking.
    """

    @override
    def generate_rankings(self) -> PlayerRanking:
        """Generate rankings that are exactly the same as consensus rankings.

        Returns:
            PlayerRanking: Consensus player rankings
        """
        return self._consensus_rankings
