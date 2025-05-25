from default import DAYS


# Defined on a week
class Field:
    def __init__(self, periods: list[tuple[int, int]]):
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

        for i in range(len(self.periods)):
            self.Monperiods.append([""] * self.periods[i][-1])
            self.Tueperiods.append([""] * self.periods[i][-1])
            self.Wenperiods.append([""] * self.periods[i][-1])
            self.Thuperiods.append([""] * self.periods[i][-1])
            self.Friperiods.append([""] * self.periods[i][-1])
            self.Satperiods.append([""] * self.periods[i][-1])
            self.Sunperiods.append([""] * self.periods[i][-1])

        self.daysperiods = [
            self.Monperiods,
            self.Tueperiods,
            self.Wenperiods,
            self.Thuperiods,
            self.Friperiods,
            self.Satperiods,
            self.Sunperiods,
        ]

    def print(self):
        for i in range(7):
            print(DAYS[i])
            print("-" * 5)
            for j in range(len(self.periods)):
                print(f"Period: {self.periods[j][0]} h")
                print(self.daysperiods[i][j])
            print()

    # first fit, max fit if first fit not found
    def fit(self, name: str, duration: int):
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
