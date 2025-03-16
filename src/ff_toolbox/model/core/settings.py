"""Types of settings existing throughout fantasy football toolbox."""

from dataclasses import dataclass

from ff_toolbox.model.core.phys_representations import RosterSpot


@dataclass
class ScoringSettings:
    """Ways a player can score in fantasy football and points associated with each.

    Params:
        pass_yd (float): Points per passing yard
        pass_td (float): Points per passing touchdown
        rush_yd (float): Points per rushing yard
        rush_td (float): Points per rushing touchdown
        rec (float): Points per reception
        rec_yd (float): Points per receiving yard
        rec_td (float): Points per receiving touchdown
        fumb (float): Points per fumble lost
        inter (float): Points per interception thrown
        fg0_39 (float): Points per field goal 0-39 yards
        fg40_49 (float): Points per field goal 40-49 yards
        fg50_ (float): Points per field goal 50+ yards
        fg_miss (float): Points per field goal missed
        xp_make (float): Points per extra point made
        xp_miss (float): Points per extra point missed
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
    """Ways a fantasy football league can be set up.

    Params:
        roster_settings (dict[RosterSpot, int]): For each type of roster spot, the max number of players of that type on a roster
        scoring_settings (ScoringSettings): How the league's games are scored
    """

    roster_settings: dict[RosterSpot, int]
    scoring_settings: ScoringSettings
