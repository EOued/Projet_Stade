from field import Field, Natural
from team import Team
from default import FieldPortion, FieldType
import onload as ol
import copy

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

# Team sorting
"""
Using multi-level sort: first field type, then priority
"""

teams.sort(key=lambda x: (x.fieldportion.value, x.priority))

unfitted_teams = []

sf_index, nf_index = 0, 0
while teams:
    subteam_portion = teams[0].fieldportion
    subteam_priority = teams[0].priority

    subteam = [
        x
        for x in teams
        if x.fieldportion == subteam_portion and x.priority == subteam_priority
    ]
    teams = [
        x
        for x in teams
        if x.fieldportion != subteam_portion or x.priority != subteam_priority
    ]

    while (
        subteam and sf_index < len(synthetic_fields) and nf_index < len(natural_fields)
    ):
        team = subteam[0]
        field = (
            natural_fields[nf_index]
            if team.fieldtype == FieldType.NATURAL
            else synthetic_fields[sf_index]
        )
        fields = (
            natural_fields if team.fieldtype == FieldType.NATURAL else synthetic_fields
        )
        index = nf_index if team.fieldtype == FieldType.NATURAL else sf_index

        print(field.portion, team.fieldportion)

        if field.portion != team.fieldportion:
            field.incr_portion()
            fields.insert(index + 1, copy.deepcopy(field))
            continue

        print(team.blocksize)
        print(*team.blocksize)
        unfitted_hours = field.fit(team.name, team.gametime, *team.blocksize)

        # Hours left for current team can't be fitted because they are smaller than the min. block size
        if unfitted_hours == -2:
            unfitted_teams.append(subteam.pop(0))
            continue

        # Failed to found a best fit, but the current field may be still used for other teams
        if unfitted_hours == -1:
            next_index = next(
                (
                    (
                        i
                        for i, x in enumerate(fields)
                        if x.portion.value == field.portion.value + 1
                    )
                ),
                -1,
            )

            if next_index == -1 or next_index < index:
                fields.append(fields.pop(index))
            else:
                fields.insert(next_index, fields.pop(index))
            continue

        print(f"{team.name}, {team.gametime}, {unfitted_hours}")

        # Current field can't fit any team
        if unfitted_hours == team.gametime:
            if team.fieldtype == FieldType.NATURAL:
                nf_index += 1
            else:
                sf_index += 1
            print("+++++++++++Changed field++++++++++")
            continue

        subteam.pop(0)
        if unfitted_hours != 0:
            team.set_gametime(unfitted_hours)
            subteam.append(team)
    # Left loop because one type of terrain is full
    if subteam:
        print("Can't fit all teams")
        break

for field in natural_fields:
    field.print()
for field in synthetic_fields:
    field.print()
