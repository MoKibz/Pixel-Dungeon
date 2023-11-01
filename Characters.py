import pygame

class Characters:

    def __init__(self):
        self._Alive = True
        self.movement_speed = 10
        self.Type = ['close_range', 'long_range']
        self.attack_range = {self.Type[0]: 20,
                             self.Type[1]: 200}
        self.defence = 100
        self.health = 100

class Shooter(Characters):

    def __init__(self):
        super().__init__()
        self.Character_Type = self.attack_range[self.Type[1]]
        self.Stats = [self.health, (self.defence - 20)]
        self.speed = self.movement_speed - 2













