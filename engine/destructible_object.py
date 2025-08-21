class DestructibleObject:
    def __init__(self, max_hp=100, autoheal=False, autoheal_delay=5, autoheal_speed=5):
        self.max_hp = max_hp
        self.hp = max_hp
        self.autoheal = autoheal
        self.autoheal_delay = autoheal_delay
        self.autoheal_speed = autoheal_speed
        self.last_dmg_time = 0

    def get_dmg(self, dmg, now=0):
        self.hp = max(0, self.hp - dmg)
        self.last_dmg_time = now

    def get_heal(self, heal):
        self.hp = min(self.max_hp, self.hp + heal)

    def update(self, dt):
        self.last_dmg_time += dt
        if self.last_dmg_time > self.autoheal_delay:
            self.hp += self.autoheal_speed / dt