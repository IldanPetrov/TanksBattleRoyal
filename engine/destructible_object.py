# destructable_object.py
from engine.game_object import GameObject


class DestructibleObject:
    def __init__(self, hp=100):
        self.hp = hp
        self.last_dmg_time = 0

    def get_dmg(self, dmg, now=0):
        self.hp = max(0, self.hp - dmg)
        self.last_dmg_time = now

        if self.hp <= 0:
            self.destroy()

    def destroy(self):
        if self in GameObject.registry:
            GameObject.registry.remove(self)
        del self


class HealableDestructibleObject(DestructibleObject):
    def __init__(self, max_hp=100, autoheal=False, autoheal_delay=5, autoheal_speed=5):
        self.max_hp = max_hp
        self.autoheal = autoheal
        self.autoheal_delay = autoheal_delay
        self.autoheal_speed = autoheal_speed
        super().__init__(max_hp)

    def get_heal(self, heal):
        self.hp = min(self.max_hp, self.hp + heal)

    def update(self, dt):
        self.last_dmg_time += dt
        if self.last_dmg_time > self.autoheal_delay:
            self.hp += self.autoheal_speed * dt
