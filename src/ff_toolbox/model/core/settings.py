"""Types of settings existing throughout fantasy football toolbox."""

from dataclasses import dataclass

from ff_toolbox.model.core.phys_representations import RosterSpot


@dataclass
class ScoringSettings:
    """
    Ways a player can score in fantasy football and points associated with each.

    :param pass_yd: Points per passing yard
    :param pass_td: Points per passing touchdown
    :param rush_yd: Points per rushing yard
    :param rush_td: Points per rushing touchdown
    :param rec: Points per reception
    :param rec_yd: Points per receiving yard
    :param rec_td: Points per receiving touchdown
    :param fumb: Points per fumble lost
    :param inter: Points per interception thrown
    :param fg0_39: Points per field goal 0-39 yards
    :param fg40_49: Points per field goal 40-49 yards
    :param fg50_: Points per field goal 50+ yards
    :param fg_miss: Points per field goal missed
    :param xp_make: Points per extra point made
    :param xp_miss: Points per extra point missed
    """

    pass_yd: float
    pass_td: float
    rush_yd: float
    rush_td: float
    rec: float
    rec_yd: float
    rec_td: float
    fumb: float
    inter: float
    fg0_39: float
    fg40_49: float
    fg50_: float
    fg_miss: float
    xp_make: float
    xp_miss: float


@dataclass
class LeagueSettings:
    """
    Ways a fantasy football league can be set up.

    :param roster_settings: For each type of roster spot, the max number of players of that type on a roster
    :param scoring_settings: How the league's games are scored
    """

    roster_settings: dict[RosterSpot, int]
    scoring_settings: ScoringSettings
