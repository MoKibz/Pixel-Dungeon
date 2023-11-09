import pygame

class Characters:

    def __init__(self):
        self._Alive = True
        self.level = 1
        self.movement_speed = 10
        self.Type = ['close_range', 'long_range']
        self.attack_range = {self.Type[0]: 30,
                             self.Type[1]: 210}
        self.defence = 100
        self.health = 100
        self.Weapons = ['gun', 'sword']
        self.Potions = ['health_potion', 'defence_potion']

def Attack(self):
    pass

class Shooter(Characters):
    def __init__(self):
        super().__init__()
        self.lvl = self.level
        self.Character_Type = self.attack_range[self.Type[1]]
        self.Stats = [self.health, (self.defence - 20)]
        self.speed = self.movement_speed - 2
        self.Shooter_item = [self.Weapons[0], self.Potions[0], self.Potions[1]]
        

class Melee(Characters):
    def __init__(self):
        super().__init__()
        self.lvl = self.level
        self.Character_Type = self.attack_range[self.Type[0]]
        self.Stats = [self.health, (self.defence + 10)]
        self.speed = self.movement_speed + 5
        self.Melee_item = [self.Weapons[1], self.Potions[0], self.Potions[1]]












