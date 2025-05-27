from default import FieldPortion, FieldType


class Team:
    def __init__(
        self,
        name: str,
        fieldportion: FieldPortion,
        gametime: int,
        priority: int,
        fieldtype: FieldType,
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

    def print(self):
        """
        Prints the team.
        """
        print(f"Team \"{self.name}\":")
        print(f"\tField portion: {self.fieldportion.name}")
        print(f"\tGame time: {self.gametime}")
        print(f"\tPriority: {self.priority}")
        print(f"\tField type: {self.fieldtype.name}")
