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

for field_name, field_values in ol.fields_config.items():
    fields.append(
        Natural(field_name, field_values["periods"])
        if field_values["type"] == 0
        else Field(field_name, field_values["periods"])
    )

for field in fields:
    field.print()
    print()
