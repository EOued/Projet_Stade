from default import FieldPortion, FieldType


class Team:
    def __init__(
        self,
        name: str,
        fieldportion: FieldPortion,
        gametime: int,
        priority: int,
        fieldtype: FieldType,
        blocksize: list[int],
        excluded_periods_mon: int = 0,
        excluded_periods_tue: int = 0,
        excluded_periods_wes: int = 0,
        excluded_periods_thu: int = 0,
        excluded_periods_fri: int = 0,
        excluded_periods_sat: int = 0,
        excluded_periods_sun: int = 0,
    ):
        self.name: str = name
        self.fieldportion: FieldPortion = (
            fieldportion
            if isinstance(fieldportion, FieldPortion)
            else FieldPortion(fieldportion)
        )
        self.gametime: int = gametime
        self.priority: int = priority
        self.fieldtype: FieldType = (
            fieldtype if isinstance(fieldtype, FieldType) else FieldType(fieldtype)
        )
        self.blocksize = blocksize

        self.excluded_periods_mon: int = excluded_periods_mon
        self.excluded_periods_tue: int = excluded_periods_tue
        self.excluded_periods_wes: int = excluded_periods_wes
        self.excluded_periods_thu: int = excluded_periods_thu
        self.excluded_periods_fri: int = excluded_periods_fri
        self.excluded_periods_sat: int = excluded_periods_sat
        self.excluded_periods_sun: int = excluded_periods_sun

        self.excluded_days = [
            self.excluded_periods_mon,
            self.excluded_periods_tue,
            self.excluded_periods_wes,
            self.excluded_periods_thu,
            self.excluded_periods_fri,
            self.excluded_periods_sat,
            self.excluded_periods_sun
        ]

        print(f"Blocksize {self.blocksize}")

    def print(self):
        """
        Prints the team.
        """
        print(f'"{self.name}":')
        print(f"\tField portion: {self.fieldportion.name}")
        print(f"\tGame time: {self.gametime}")
        print(f"\tPriority: {self.priority}")
        print(f"\tField type: {self.fieldtype.name}")
        return

    def set_gametime(self, decrement: int):
        self.gametime = decrement
        return
