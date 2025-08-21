from engine.game_object import GameObject


class MaterialObject(GameObject):
    def __init__(self, name, length=40, width=40, collision=True, **kwargs):
        super().__init__(name, kwargs.get("x", 0), kwargs.get("y", 0), kwargs.get("dir", 0), kwargs.get("parent", None))
        self.length = length
        self.width = width
        self.collision = collision

    def collided_to(self, other: "MaterialObject"):
        """Вызов при коллизии"""
        pass
