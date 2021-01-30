from player_class import Player
from weapon_class import Weapon
from enum import Enum
import time

class tile_object(Enum):
    NONE = 0
    DANGER_ZONE = 1
    PLAYER = 2

class weapon_type(Enum):
    MELEE = 0
    RANGED = 1
    SPECIAL = 2

class GridTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.danger_zone = False
        self.object = tile_object.NONE

    def update_tile_object(self, t_object):
        self.object = t_object

SMALL_MAP = 5
MEDIUM_MAP = 11
LARGE_MAP = 21

def initializeMap(size):
    return populate_grid(size, size)


def populate_grid(rows, columns):
    tile_array = []

    for x in range(0, rows):
        col_array = []
        for y in range(0, columns):
            col_array.append(GridTile(x, y))

        tile_array.append(col_array)

    return tile_array


def encloseRing(_grid_map, count):
    minimum = count
    maximum = (len(_grid_map)-1) - count

    for row in grid_map:
        for tile in row:
            if tile.x == minimum or tile.x == maximum or tile.y == minimum or tile.y == maximum:
                tile.danger_zone = True
                tile.update_tile_object(tile_object.DANGER_ZONE)


def displayMap(_grid_map):
    tiles = _grid_map

    for row in tiles:
        row_str = ""

        for col in range(len(row)):
            row_str = row_str + str(row[col].danger_zone) + " "

        print(row_str)

# Very basic weapon initialization
# TODO: Streamline classes and initialization of weapons
def initializeWeapons():
    return [
        Weapon("Knuckle Dusters", weapon_type.MELEE, 14, 1.2, 3, 2, None),
        Weapon("Crowbar", weapon_type.MELEE, 19, 1.5, 6, 4, None),
        Weapon("Axe", weapon_type.MELEE, 25, 1.7, 8, 5, None),
        Weapon("Shotgun", weapon_type.RANGED, 40, 1.8, 4, 9, None)
    ]


def player_turn(_player, _grid_map):
    surrounding_tiles = _player.identify_new_information(_grid_map, tile_object)

    danger_tiles = player.assess_information(surrounding_tiles, tile_object)

    print(danger_tiles)

    player.make_decision(danger_tiles)


if __name__ == "__main__":
    map_size = SMALL_MAP

    grid_map = initializeMap(map_size)
    all_weapons = initializeWeapons()

    ring_close_turns = map_size // 2

    overall_count = 0

    player = Player(3, 1, 100, None)

    while overall_count < ring_close_turns:
        turn_count = 0

        displayMap(grid_map)

        while turn_count < 3:
            print("\nTurn: " + str(turn_count))
            time.sleep(3)
            player_turn(player, grid_map)
            turn_count += 1

        encloseRing(grid_map, overall_count)

        print("\n\n")

        overall_count += 1

    displayMap(grid_map)