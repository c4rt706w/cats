class Skill:
    def  __init__(self, name = '', level = 0, damage = 0):
        self.name = name
        self.level = level
        self.damage = damage

    def get_damage(self):
        return self.damage

    def get_info(self):
        return f'{ self.name }: { self.level } lvl skill deals { self.damage } damage'

class Equipment:
    def __init__(self, name = '', level = 0):
        self.name = name
        self.level = level

class Toy(Equipment):
    def __init__(self, name = '', level = 0, damage = 0):
        super().__init__(name, level)
        self.damage = damage

    def get_damage(self):
        return self.damage

    def get_info(self):
        return f'{ self.name }: { self.level } lvl skill buffs { self.damage } damage'

class Suit(Equipment):
    def __init__(self, name = '', level = 0, stamina = 0):
        super().__init__(name, level)
        self.stamina = stamina

    def get_stam(self):
        return self.stamina

    def get_info(self):
        return f'{ self.name }: { self.level } lvl skill buffs { self.stamina } hp'