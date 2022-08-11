"""Conglomeration of data types that represent physical things in the fantasy football world."""
from dataclasses import dataclass
from enum import Enum


class Position(Enum):
    """Possible primary positions of fantasy football players."""

    QB = 0
    RB = 1
    WR = 2
    TE = 3
    DST = 4
    K = 5


class RosterSpot(Enum):
    """Possible roster spots on a roster, listed in order of priority"""

    QB = 0
    RB = 1
    WR = 2
    TE = 3
    DST = 4
    K = 5
    FLEX = 6
    QBFLEX = 7
    BENCH = 8
    IR = 9


@dataclass
class Player:
    """
    Representation of football player in fantasy football.

    :param position: Primary position of player
    :param name: Full name of player
    :param team: NFL team of player
    :param ir_eligible: Whether player can use IR slot or not
    """

    position: Position
    name: str
    team: str
    ir_eligible: bool

    def is_roster_eligible(self, roster_spot: RosterSpot) -> bool:
        """
        Return whether player is eligible for given roster spot on a fantasy team.

        :param roster_spot: Roster spot to check eligibility for
        :return: True if player is eligible for roster spot, False if not
        """
        match roster_spot:
            case RosterSpot.QB:
                return self.position == Position.QB
            case RosterSpot.RB:
                return self.position == Position.RB
            case RosterSpot.WR:
                return self.position == Position.WR
            case RosterSpot.TE:
                return self.position == Position.TE
            case RosterSpot.DST:
                return self.position == Position.DST
            case RosterSpot.K:
                return self.position == Position.K
            case RosterSpot.FLEX:
                return self.position in [Position.RB, Position.WR, Position.TE]
            case RosterSpot.QBFLEX:
                return self.position in [
                    Position.QB,
                    Position.RB,
                    Position.WR,
                    Position.TE,
                ]
            case RosterSpot.BENCH:
                return True
            case RosterSpot.IR:
                return self.ir_eligible

    def __str__(self) -> str:
        return f"{self.name} {self.team} ({self.position.name})"


class Roster:
    """
    Representation of an owner's roster in fantasy football.

    :param settings: Roster spot settings
    :param players: Current players on the roster associated with each roster spot
    """

    def __init__(self, settings: dict[RosterSpot, int]) -> None:
        """
        Create a new, empty roster with given roster settings.

        :param settings: Max number of players for each roster spot type
        """
        self._settings: dict[RosterSpot, int] = settings
        self._players: dict[RosterSpot, list[Player]] = {pos: [] for pos in RosterSpot}

    def add_player(self, player: Player) -> None:
        """
        Add new player to roster if possible.

        :param player: Player to add to roster
        :raises RuntimeError: No space on roster for player
        """
        added: bool = False
        for spot in RosterSpot:
            if (player.is_roster_eligible(spot)) and (
                len(self._players[spot]) < self._settings[spot]
            ):
                self._players[spot].append(player)
                added = True
                break
        if not added:
            raise RuntimeError(f"No space on roster for player {player}")

    def remove_player(self, player: Player) -> None:
        """
        Remove given player from roster if on roster.

        :param player: Player to remove from roster
        """
        for roster_spot, players in self._players.items():
            if player in players:
                self._players[roster_spot].remove(player)

    def swap_players(self, player1: Player, player2: Player) -> None:
        """
        Swap roster spots of two players on roster.

        :param player1: First player to swap
        :param player2: Second player to swap
        :raise RuntimeError: Unable to swap two players
        """
        # Validate each other's roster spot
        p1_roster_spot: RosterSpot | None = None
        p2_roster_spot: RosterSpot | None = None
        for roster_spot, players in self._players.items():
            if player1 in players and player2.is_roster_eligible(roster_spot):
                p1_roster_spot = roster_spot
            if player2 in players and player1.is_roster_eligible(roster_spot):
                p2_roster_spot = roster_spot
        # Swap spot on roster
        if not (p1_roster_spot and p2_roster_spot):
            raise RuntimeError(
                f"Couldn't swap players {player1} and {player2} on roster"
            )
        self._players[p1_roster_spot].remove(player1)
        self._players[p1_roster_spot].append(player2)
        self._players[p2_roster_spot].remove(player2)
        self._players[p2_roster_spot].append(player1)

    def move_player(self, player: Player, roster_spot: RosterSpot) -> None:
        """
        Move player from current roster spot to a given open roster spot.

        :param player: Player whose spot to change
        :param roster_spot: Roster spot to move to
        """
        # Verify there's space at roster spot for player and player is eligible to play there
        if len(self._players[roster_spot]) >= self._settings[roster_spot]:
            raise RuntimeError(
                f"No open roster spot at {roster_spot.name} to move player to"
            )
        if not player.is_roster_eligible(roster_spot):
            raise RuntimeError(
                f"Player {player} isn't eligible to be placed at {roster_spot.name}"
            )
        # Verify player is on roster and remove them from roster temporarily
        player_on_roster: bool = False
        for roster_spot, players in self._players.items():
            if player in players:
                self._players[roster_spot].remove(player)
                player_on_roster = True
                break
        if not player_on_roster:
            raise RuntimeError(f"Player {player} does not already exist on roster")
        # Add player back to new roster spot
        self._players[roster_spot].append(player)

    def __str__(self) -> str:
        return "\n".join(
            [
                f"{key.name}: {player}"
                for key, players in self._players.items()
                for player in players
            ]
        )


@dataclass
class Team:
    """
    Representation of an owner's fantasy team in fantasy football.

    :param name: Team name
    :param owner: Owner's name
    :param roster: Team's roster
    """

    name: str
    owner: str
    roster: Roster
