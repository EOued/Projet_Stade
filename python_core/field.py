from python_core.default import DAYS
from enum import Enum

from copy import deepcopy


class FitType(Enum):
    FIRST_FIT = 0
    BEST_FIT = 1
    WORST_FIT = 2


# Defined on a week
class Field:
    def __init__(
        self,
        name: str,
        periods: list[int],
    ):
        self.name = name
        self.orig_periods = deepcopy(periods)
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

        self.teams = [{}, {}, {}, {}, {}, {}, {}]

    def reset(self):
        self.teams = [{}, {}, {}, {}, {}, {}, {}]
        self.periods = deepcopy(self.orig_periods)

    def fit(
        self, day, duration, team_name, team_locked_periods, fit_type: FitType
    ) -> tuple[int, int]:
        self.periods[day] &= ~team_locked_periods
        mask = 2**duration - 1
        fittable_mask = []
        for i in range(24):
            if self.periods[day] & mask == mask:
                if fit_type == FitType.FIRST_FIT:
                    if team_name not in self.teams:
                        self.teams[day][team_name] = 0
                    self.teams[day][team_name] ^= mask
                    self.periods[day] ^= mask
                    return (self.periods[day] & (2 ** (i + duration) - 1), i)
                fittable_mask.append((self.periods[day] & (2 ** (i + duration) - 1), i))
            mask = mask << 1
        if fittable_mask == []:
            return (-1, -1)
        continuation_list = []
        sequence_length = 0
        positions = []
        for i in range(len(fittable_mask)):
            positions.append(i)
            sequence_length += 1
            # Unset
            continuation_list.append(-1)

            # Sequence break
            if (
                i == len(fittable_mask) - 1
                or fittable_mask[i][1] + 1 != fittable_mask[i + 1][1]
            ):
                for position in positions:
                    continuation_list[position] = sequence_length
                positions.clear()
                sequence_length = 0

        extremum_func = min if fit_type == FitType.BEST_FIT else max
        extremum_pos = continuation_list.index(extremum_func(continuation_list))
        if extremum_pos < 0 or extremum_pos >= len(fittable_mask):
            return (-1, -1)
        mask = (2**duration - 1) << fittable_mask[extremum_pos][1]
        if team_name not in self.teams[day]:
            self.teams[day][team_name] = 0
        self.teams[day][team_name] ^= mask
        self.periods[day] ^= mask

        return fittable_mask[extremum_pos]

    def __eq__(self, other):
        if not isinstance(other, Field):
            return False
        same_periods = True
        for a, b in zip(self.daysperiods, other.daysperiods):
            same_periods &= a == b
        return self.name == other.name and same_periods

    def print(self):
        """
        Print all periods.
        """
        print(
            f'"{self.name}" - {"Natural" if isinstance(self, Natural) else "Synthetic"}:'
        )
        for day in range(7):
            print(f"\t{DAYS[day]}")
            print(f"\t\t{bin(self.periods[day])}")
        return


class Natural(Field):
    def __init__(self, name: str, periods: list[int]):
        super().__init__(name, periods)
        self.hours_availables = 15

    def print(self):
        super().print()
        print(f"\tHours available {self.hours_availables}")

    def reset(self):
        self.hours_availables = 15
        super().reset()

    def fit(
        self, day, duration, team_name, team_locked_periods, fit_type: FitType
    ) -> tuple[int, int]:
        if self.hours_availables - duration < 0:
            return (-1, -1)
        self.hours_availables -= duration
        return super().fit(day, duration, team_name, team_locked_periods, fit_type)
