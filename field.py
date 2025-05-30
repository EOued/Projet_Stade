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

    def __eq__(self, other):
        if not isinstance(other, Field):
            return False
        same_periods = True
        for a, b in zip(self.daysperiods, other.daysperiods):
            same_periods &= a == b
        return (
            self.name == other.name
            and self.portion.value == other.portion.value
            and same_periods
        )

    def incr_portion(self):
        self.portion = FieldPortion(self.portion.value + 1)

    def decr_portion(self):
        self.portion = FieldPortion(self.portion.value - 1)

    def print(self):
        """
        Print all periods.
        """
        print(
            f'"{self.name}" - {self.portion.name} - {"Natural" if isinstance(self, Natural) else "Synthetic"}:'
        )
        for i in range(7):
            print(f"\t{DAYS[i]}")
            for j in range(len(self.periods[self.key[i]])):
                print(
                    f"\t\tPeriod: {self.periods[self.key[i]][j][0]} h: {self.daysperiods[i][j]}"
                )
        return

    def fit(self, name: str, duration: int, min_blocksize=1, max_blocksize=24) -> int:
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
        if duration < min_blocksize:
            # Failure : The duration we try to fit is smaller than the min duration
            return -2
        print("fit function", name, min_blocksize, max_blocksize)
        best_fit = (-1, -1)
        best_fit_size = -1
        duration_ti = min(duration, max_blocksize)
        # If fitting the whole block, then the unfitted block is smaller than min_blocksize
        if 0 < duration - duration_ti < min_blocksize:
            duration_ti = min(duration_ti, duration - min_blocksize)

        print(f"duration {duration}, duration_ti {duration_ti}")
        for i in range(len(self.daysperiods)):
            dayperiod = self.daysperiods[i]
            for j in range(len(dayperiod)):
                period = dayperiod[j]
                count = period.count("")
                print(f"count {count}")
                if duration_ti <= count:
                    index = period.index("")
                    period[index : index + duration_ti] = [name] * duration_ti
                    return duration - duration_ti

                if count >= min_blocksize and count > best_fit_size:
                    best_fit_size = count
                    best_fit = (i, j)

        # There is no best fit found
        if best_fit_size == -1:
            return -1

        # No perfect fit found, setting the best fit
        print("BEST FIT")
        period = self.daysperiods[best_fit[0]][best_fit[1]]
        size = min(period.count(""), max_blocksize)
        index = period.index("")
        print(period, size, index)
        period[index : index + size] = [name] * size
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

    def print(self):
        super().print()
        print(f"\tHours available {self.hours_availables}")

    def fit(self, name: str, duration: int, min_blocksize=1, max_blocksize=24) -> int:
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
        unfitted_hours = super().fit(name, max_tofit, min_blocksize, max_blocksize)
        self.hours_availables -= max_tofit - unfitted_hours
        return unfitted_hours + (duration - max_tofit)
