from python_core.field import Field, FitType, Natural
from python_core.team import Team
from python_core.default import FieldPortion


class Connector:
    def __init__(self):
        self.fields = []
        self.teams = []
        self.fit_type = FitType.FIRST_FIT

    def parse_fields(self, fields_data):
        for field in fields_data:
            data = field[0]
            periods = field[1]
            f = Field if data[1] else Natural
            self.fields.append(f(data[0], periods))

    def parse_teams(self, teams_data):
        for team in teams_data:
            data = team[0]
            periods = team[1]
            self.teams.append(Team(data[0], FieldPortion(data[1]), data[2], periods))

    def fit(self):
        self.teams.sort(key=lambda team: (team.fieldportion.value, team.priority))

        unfittable = []
        for team in self.teams:
            for iday, day in enumerate(team.periods):
                for period in day:
                    fitted = False
                    for field in self.fields:
                        # Check field type
                        field_type = int(not isinstance(field, Natural))
                        if field_type != period[1]:
                            continue
                        fittable = field.fit(
                            iday,
                            period[0],
                            team.name,
                            team.locked_periods[iday],
                            self.fit_type,
                        )
                        if fittable != (-1, -1):
                            fitted = True
                            mask = (2 ** period[0] - 1) << fittable[1]
                            team.add_field(iday, field.name, mask)
                            break
                    if fitted:
                        continue

                    unfittable.append([team.name, iday, period[0], period[1]])
        return unfittable

    def get_team_list(self):
        return [team.name for team in self.teams]

    def get_field_list(self):
        return [field.name for field in self.fields]

    def get_fields_from_team(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team.fields
        return None

    def get_teams_from_field(self, field_name):
        for field in self.fields:
            if field.name == field_name:
                return field.teams
        return None

    def set_fit_type(self, fit_type):
        if fit_type != self.fit_type:
            for element in self.teams + self.fields:
                element.reset()
            self.fit_type = fit_type
            self.fit()
