from default import DAYS, FieldPortion


# Defined on a week
class Field:
    def __init__(
        self,
        name: str,
        periods: list[int],
        portion: FieldPortion = FieldPortion.WHOLE,
    ):
        self.name = name
        self.periods = periods
        self.Monperiods: list[str] = [""] * 24
        self.Tueperiods: list[str] = [""] * 24
        self.Wenperiods: list[str] = [""] * 24
        self.Thuperiods: list[str] = [""] * 24
        self.Friperiods: list[str] = [""] * 24
        self.Satperiods: list[str] = [""] * 24
        self.Sunperiods: list[str] = [""] * 24

        self.daysperiods = [
            self.Monperiods,
            self.Tueperiods,
            self.Wenperiods,
            self.Thuperiods,
            self.Friperiods,
            self.Satperiods,
            self.Sunperiods,
        ]

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

    def generate_periods(
        self, day: int, restriction: int = 16777215, get_period_hours=False
    ):
        periods_number = restriction & self.periods[day]
        l = []
        sublist = []
        period_hours = []
        for hour in range(24):
            if periods_number & (1 << hour):
                if get_period_hours and not sublist:
                    period_hours.append(hour)
                sublist.append(self.daysperiods[day][hour])
            elif sublist:
                l.append(sublist)
                sublist = []

        if sublist:
            l.append(sublist)
        if get_period_hours:
            return l, period_hours
        return l

    def generate_periods_indexes(self, day: int, restriction: int = 16777215):
        periods_number = restriction & self.periods[day]
        l = []
        sublist = []
        for hour in range(24):
            if periods_number & (1 << hour) and self.daysperiods[day][hour] == "":
                sublist.append(hour)
            elif sublist:
                l.append(sublist)
                sublist = []

        if sublist:
            l.append(sublist)
        return l

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
        for day in range(7):
            print(f"\t{DAYS[day]}")
            periods, periods_hours = self.generate_periods(day, get_period_hours=True)
            for index, period in enumerate(periods):
                print(f"\t\tPeriod {periods_hours[index]} h: {period}")
        return

    def fit(
        self,
        name: str,
        duration: int,
        min_blocksize=1,
        max_blocksize=24,
        restricted_days: list[int] = [16777215] * 7,
    ) -> int:
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
        for day, dayperiod in enumerate(self.daysperiods):
            available_periods = self.generate_periods_indexes(day, restricted_days[day])

            for index, period_indexes in enumerate(available_periods):
                count = len(period_indexes)
                print(f"count {count}")
                if duration_ti <= count:
                    dayperiod[period_indexes[0] : period_indexes[duration_ti - 1]] = [
                        name
                    ] * duration_ti
                    return duration - duration_ti

                if count >= min_blocksize and count > best_fit_size:
                    best_fit_size = count
                    best_fit = (day, index)

        # There is no best fit found
        if best_fit_size == -1:
            return -1

        # No perfect fit found, setting the best fit
        print("BEST FIT")
        day = best_fit[0]
        period_indexes = self.generate_periods_indexes(day, restricted_days[day])[
            best_fit[1]
        ]
        size = min(len(period_indexes), max_blocksize)
        self.daysperiods[day][period_indexes[0] : period_indexes[size - 1]] = [
            name
        ] * size
        return duration - size


class Natural(Field):
    def __init__(
        self,
        name: str,
        periods: list[int],
        portion: FieldPortion = FieldPortion.WHOLE,
    ):
        super().__init__(name, periods, portion)
        self.hours_availables = 15

    def print(self):
        super().print()
        print(f"\tHours available {self.hours_availables}")

    def fit(
        self,
        name: str,
        duration: int,
        min_blocksize=1,
        max_blocksize=24,
        restricted_days: list[int] = [16777215] * 7,
    ) -> int:
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
        unfitted_hours = super().fit(
            name, max_tofit, min_blocksize, max_blocksize, restricted_days
        )
        self.hours_availables -= max_tofit - unfitted_hours
        return unfitted_hours + (duration - max_tofit)
