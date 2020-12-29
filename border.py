# Enum type describing varieties of boundaries between tiles

import enum

class Border(enum.Enum):
    WALL = 1
    EMPTY = 2
    DOOR = 3
    SECRET_DOOR = 4
    TRAPPED_DOOR = 5
