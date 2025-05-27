from default import FieldPortion

class Team:
    def __init__(self, name, fieldportion: FieldPortion, gametime, priority, fieldtype):
        self.name = name
        self.fieldportion = fieldportion
        self.gametime = gametime
        self.priority = priority
        self.fieldtype = fieldtype


