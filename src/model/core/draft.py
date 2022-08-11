"""Representation of a fantasy football draft."""
from src.model.core.phys_representations import Player, Team
from src.model.core.settings import LeagueSettings


class Draft:
    """Representation of a draft, with functions to modify the picks in the draft."""

    def __init__(
        self,
        order: list[Team],
        rounds: int,
        player_pool: list[Player],
        settings: LeagueSettings,
    ) -> None:
        """
        Create a draft, tracking the teams, available players, and settings of the league.

        :param order: List of teams participating in snake draft, sorted by the order they pick in round 1
        :param rounds: Number of rounds in draft
        :param player_pool: Players available to pick from in the draft
        :param settings: Settings of the league the draft is occurring in
        """
        self._order: list[Team] = order
        self._rounds: int = rounds
        self._picks: list[Player] = []
        self._undrafted: list[Player] = player_pool
        self._settings: LeagueSettings = settings

    def set_pick(self, player: Player, pick_num: int | None = None) -> None:
        """
        Set the xth pick of the draft (starting at 1) as the given player.

        :param player: Player who was drafted at given spot (or next spot)
        :param pick_num: If int, location in draft player was picked. If None, evaluates internally to next pick
        :raises ValueError: Pick number provided out of range (not a past pick or immediate next pick)
        :raises RuntimeError: Player unavailable to pick, can't add another pick
        """
        if player not in self._undrafted:
            raise RuntimeError(f"Player {player} not available to pick")
        if (not pick_num) or (pick_num - 1 == len(self._picks)):
            # If adding next pick, remove player from undrafted and add to next pick's team
            if len(self._picks) == len(self._order) * self._rounds:
                raise RuntimeError("Can't add another pick. Draft already complete.")
            self.pick_num_to_team(len(self._picks) + 1).roster.add_player(player)
            self._undrafted.remove(player)
            self._picks.append(player)
        elif (len(self._picks) < pick_num - 1) or (pick_num <= 0):
            raise ValueError(
                f"Pick number {pick_num} is out of range. The next pick is pick {len(self._picks) + 1}"
            )
        else:
            # If changing pick, remove player from team and add to player pool.
            self.pick_num_to_team(pick_num).roster.remove_player(player)
            self._undrafted.append(self._picks[pick_num - 1])
            # Then remove new player from player pool and to team
            self.pick_num_to_team(pick_num).roster.add_player(player)
            self._undrafted.remove(player)
            self._picks[pick_num - 1] = player

    def delete_picks(self, num_picks: int | None) -> None:
        """
        Deletes the given numbers of picks from end of the draft

        :param num_picks: Number of picks to delete from end of draft. None to delete all picks.
        """
        new_num_picks = num_picks if num_picks else len(self._picks)
        for pick in range(new_num_picks):
            self.pick_num_to_team(len(self._picks)).roster.remove_player(
                self._picks[-1]
            )
            self._undrafted.append(self._picks[-1])
            self._picks.pop()

    def pick_num_to_team(self, pick_num: int) -> Team:
        """
        Convert a pick number to the team picking at that spot.

        :param pick_num: Pick number to convert (1-based)
        :raises ValueError: Pick number out of bounds of draft picks
        :return: Team picking at given pick number
        """
        num_picks: int = len(self._order) * self._rounds
        if pick_num <= 0 or pick_num > num_picks:
            raise ValueError(f"Pick number {pick_num} for draft with {num_picks} picks")
        team_num = (pick_num - 1) % len(self._order)
        round = (pick_num - 1) // len(self._order) + 1
        if round % 2 == 0:
            team_num = len(self._order) - team_num - 1
        return self._order[team_num]
