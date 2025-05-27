from field import Field, Natural
from team import Team
from default import FieldType
import onload as ol

ol.load()

# Creating teams

teams: list[Team] = []

for team_name, team_values in ol.teams_config.items():
    teams.append(Team(team_name, *team_values))

# Creating fields

synthetic_fields: list[Field] = []
natural_fields: list[Natural] = []
fieldtypestr = ["natural", "synthetic"]

for field_name, field_values in ol.fields_config.items():
    if field_values["type"] == 0:
        natural_fields.append(Natural(field_name, field_values["periods"]))
    else:
        synthetic_fields.append(Field(field_name, field_values["periods"]))


sf_index, nf_index = 0, 0
while teams and sf_index < len(synthetic_fields) and nf_index < len(natural_fields):
    team = teams[0]
    field = (
        natural_fields[nf_index]
        if team.fieldtype == FieldType.NATURAL
        else synthetic_fields[sf_index]
    )

    print(f"{team.name}, {team.gametime}")
    unfitted_hours = field.fit(team.name, team.gametime)
    # Current field can't fit any team
    if unfitted_hours == team.gametime:
        if team.fieldtype == FieldType.NATURAL:
            nf_index += 1
        else:
            sf_index += 1

    teams.pop(0)
    if unfitted_hours != 0:
        team.set_gametime(unfitted_hours)
        teams.append(team)

    if team.fieldtype == FieldType.NATURAL:
        print("Natural field(s):")
        for field in natural_fields:
            field.print()
    else:
        print("Synthetic field(s):")
        for field in synthetic_fields:
            field.print()
