# utils.py

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


def get_local_position(parent_pos, parent_dir, child_pos):
    p_x, p_y = parent_pos
    x, y = rotate_point(child_pos, -parent_dir, parent_pos)
    return x - p_x, y - p_y


def get_global_position(parent_pos, parent_dir, child_pos):
    p_x, p_y = parent_pos
    x, y = rotate_point(child_pos, parent_dir, (0, 0))
    return x + p_x, y + p_y