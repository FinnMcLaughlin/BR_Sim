from enum import Enum

class tile_object_type(Enum):
    NONE = 0
    DANGER_ZONE = 1
    PLAYER = 2

class weapon_type(Enum):
    MELEE = 0
    RANGED = 1
    SPECIAL = 2