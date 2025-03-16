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
    """Possible roster spots on a roster, listed in order of priority."""

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
    """Representation of football player in fantasy football.

    Params:
        position (Position): Primary position of player
        name (str): Full name of player
        team (str): NFL team of player
        ir_eligible (bool): Whether player can use IR slot or not
    """

    position: Position
    name: str
    team: str
    ir_eligible: bool

    def is_roster_eligible(self, roster_spot: RosterSpot) -> bool:
        """Return whether player is eligible for given roster spot on a fantasy team.

        Params:
            roster_spot (RosterSpot): Roster spot to check eligibility for

        Returns:
            bool: True if player is eligible for roster spot, False if not
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
    """Representation of an owner's roster in fantasy football."""

    def __init__(self, settings: dict[RosterSpot, int]) -> None:
        """Create a new, empty roster with given roster settings.

        Params:
            settings (dict[RosterSpot, int]): Max number of players for each roster spot type
        """
        self._settings: dict[RosterSpot, int] = settings
        self._players: dict[RosterSpot, list[Player]] = {pos: [] for pos in RosterSpot}

    def add_player(self, player: Player) -> None:
        """Add new player to roster if possible.

        Params:
            player (Player): Player to add to roster

        Raises:
            RuntimeError: No space on roster for player
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
        """Remove given player from roster if on roster.

        Params:
            player (Player): Player to remove from roster
        """
        for roster_spot, players in self._players.items():
            if player in players:
                self._players[roster_spot].remove(player)

    def swap_players(self, player1: Player, player2: Player) -> None:
        """Swap roster spots of two players on roster.

        Params:
            player1 (Player): First player to swap
            player2 (Player): Second player to swap

        Raises:
            RuntimeError: Unable to swap two players
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
        """Move player from current roster spot to a given open roster spot.

        Params:
            player (Player): Player whose spot to change
            roster_spot (RosterSpot): Roster spot to move to
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
    """Representation of an owner's fantasy team in fantasy football.

    Params:
        name (str): Team name
        owner (str): Owner's name
        roster (Roster): Team's roster
    """

    name: str
    owner: str
    roster: Roster


class PlayerRanking:
    """Holds a list of player rankings and gets different types of rankings based on overall."""

    def __init__(self, players: list[Player]) -> None:
        """Store an overall list of players as a ranking, from highest rank to lowest rank.

        Params:
            players (list[Player]): List of players, ranked
        """
        self._players: list[Player] = players

    def get_ovr_rankings(self) -> list[Player]:
        """Return current overall rankings, with all positions mixed in.

        Returns:
            list[Player] List of overall rankings, high ranking to low
        """
        return self._players

    def get_pos_rankings(self, position: Position) -> list[Player]:
        """Return current player rankings, filtered by a given position.

        Params:
            position (Position): Player position to filter by

        Returns:
            list[Player] List of players at given position
        """
        return [player for player in self._players if player.position == position]
