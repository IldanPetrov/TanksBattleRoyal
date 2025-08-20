import math


def rotate_point(point, angle, base=(0, 0)):
    """
    Поворот точки вокруг base на angle (в градусах).
    """
    angle_rad = math.radians(angle)
    px, py = point
    bx, by = base

    dx = px - bx
    dy = py - by

    qx = bx + math.cos(angle_rad) * dx - math.sin(angle_rad) * dy
    qy = by + math.sin(angle_rad) * dx + math.cos(angle_rad) * dy
    return qx, qy

