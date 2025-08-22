# tank.py

from engine.material_object import MaterialObject
from engine.destructible_object import HealableDestructibleObject
from engine.smart_object import SmartObject
from game.hull import Hull
from game.gun import Gun


class Tank(MaterialObject, HealableDestructibleObject, SmartObject):
    def __init__(self, hull_cls, gun_cls, x=0, y=0, dir=0, name='Tank'):
        MaterialObject.__init__(self, name, x=x, y=y, dir=dir, length=80, width=80)
        HealableDestructibleObject.__init__(self, autoheal=True)

        self.ammo = 30
        self.gears = 0
        self.blueprints = 0
        self.hull_lvl = 0
        self.gun_lvl = 0
        self.hull = None
        self.gun = None

        self.equip_hull(hull_cls)
        self.equip_gun(gun_cls)

    def equip_hull(self, hull_cls):
        self.unpin()
        if self.hull:
            del self.hull
        self.hull = hull_cls(lvl=self.hull_lvl)
        self.hull.set_position(*self.get_position())
        self.hull.set_dir(self.get_dir())
        self.pin_to(self.hull)
        if self.gun:
            self.max_hp = self.hull.armor + self.gun.armor

    def equip_gun(self, gun_cls):
        if self.gun:
            del self.gun
        self.gun = gun_cls(lvl=self.gun_lvl)
        self.gun.set_position(*self.get_position())
        self.gun.set_dir(self.get_dir())
        self.gun.pin_to(self)
        if self.hull:
            self.max_hp = self.hull.armor + self.gun.armor

    def pickup_item(self, item):
        pass

    def destroy(self):
        gun = self.gun
        hull = self.hull
        # self = LootBox(*self.get_position() ,hull_cls=hull.__class__, gun_cls=gun.__class__, ammo=self.ammo, gears=self.gears,
        #                blueprints=self.blueprints)
        gun.active_sprite = "corpse"
        hull.active_sprite = "corpse"
        gun.pin_to(hull)
        pass
