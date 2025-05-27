from field import Field, Natural
from team import Team
from default import FieldPortion
import onload as ol

ol.load()

# Creating teams

teams: list[Team] = []

for team_name, team_values in ol.teams_config.items():
    teams.append(Team(team_name, *team_values))

# Creating fields

fields: list[Field] = []
fieldtypeclass = [Natural, Field]
fieldtypestr = ["natural", "synthetic"]

for i in range(2):
    periods = ol.settings_config["fields_periods"][fieldtypestr[i]]
    for _ in range(ol.settings_config["fields_number"][fieldtypestr[i]]):
        fields.append(fieldtypeclass[i](periods))

