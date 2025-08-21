import os

with open(os.path.abspath("../assets/sprites/StandardHull.png"), "rb") as f:
    sprite = f.read()
    print(sprite)