from default import DAYS, FieldPortion


# Defined on a week
class Field:
    def __init__(
        self,
        name: str,
        periods: dict[str, list[list[int]]],
        portion: FieldPortion = FieldPortion.WHOLE,
    ):
        self.name = name
        self.periods = periods
        self.Monperiods: list[list[str]] = []
        self.Tueperiods: list[list[str]] = []
        self.Wenperiods: list[list[str]] = []
        self.Thuperiods: list[list[str]] = []
        self.Friperiods: list[list[str]] = []
        self.Satperiods: list[list[str]] = []
        self.Sunperiods: list[list[str]] = []

        self.min = min(self.periods, key=lambda elem: elem[-1])[1]
        self.max = max(self.periods, key=lambda elem: elem[-1])[1]

        self.daysperiods = [
            self.Monperiods,
            self.Tueperiods,
            self.Wenperiods,
            self.Thuperiods,
            self.Friperiods,
            self.Satperiods,
            self.Sunperiods,
        ]

        self.key = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

        for day in range(7):
            for i in range(len(self.periods[self.key[day]])):
                self.daysperiods[day].append([""] * self.periods[self.key[day]][i][-1])

        self.portion = (
            portion if isinstance(portion, FieldPortion) else FieldPortion(portion)
        )

    def set_period(self, portion: FieldPortion):
        self.portion = (
            portion if isinstance(portion, FieldPortion) else FieldPortion(portion)
        )

    def print(self):
        """
        Print all periods.
        """
        print(f"\"{self.name}\" - {self.portion.name}:")
        for i in range(7):
            print(f"\t{DAYS[i]}")
            for j in range(len(self.periods[self.key[i]])):
                print(f"\t\tPeriod: {self.periods[self.key[i]][j][0]} h: {self.daysperiods[i][j]}")
        return

    def fit(self, name: str, duration: int) -> int:
        """
        Tries to fit the duration given in a continuous period.
        The function will first try to fit the whole duration in the first period that can fit it.
        If there is no periods that allows for it, the function will try to fit the maximum number of hours in a period.

        Parameters:
        name (str): The name of the team.
        duration (int): The numbers of hours to fit.

        Returns:
        The number of hours that have not been fitted.
        """
        best_fit = (-1, -1)
        best_fit_size = -1
        for i in range(len(self.daysperiods)):
            dayperiod = self.daysperiods[i]
            for j in range(len(dayperiod)):
                period = dayperiod[j]
                if duration <= period.count(""):
                    index = period.index("")
                    for k in range(duration):
                        period[index + k] = name
                    return 0
                if period.count("") > best_fit_size:
                    best_fit_size = period.count("")
                    best_fit = (i, j)

        # No perfect fit found, setting the first fit
        period = self.daysperiods[best_fit[0]][best_fit[1]]
        size = period.count("")
        index = period.index("")
        for k in range(size):
            period[index + k] = name
        return duration - size


class Natural(Field):
    def __init__(
        self,
        name: str,
        periods: dict[str, list[list[int]]],
        portion: FieldPortion = FieldPortion.WHOLE,
    ):
        super().__init__(name, periods, portion)
        self.hours_availables = 15

    def fit(self, name: str, duration: int) -> int:
        """
        Tries to fit the duration given in a continuous period.
        The function will first try to fit the whole duration in the first period that can fit it.
        If there is no periods that allows for it, the function will try to fit the maximum number of hours in a period.
        The function will stops when the number of hours fitted is at 15.

        Parameters:
        name (str): The name of the team.
        duration (int): The numbers of hours to fit.

        Returns:
        The number of hours that have not been fitted.
        """
        if self.hours_availables == 0:
            return duration

        max_tofit = min(duration, self.hours_availables)
        unfitted_hours = super().fit(name, max_tofit)
        self.hours_availables -= (max_tofit - unfitted_hours)
        return unfitted_hours + (duration - max_tofit)
