from player_class import Player
from weapon_class import Weapon
from enum import Enum
import random
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
        self.object = [tile_object.NONE]

    def update_tile_object(self, t_object):
        print("\n-----------Previous Tile Object " + str(self.x) + ", " + str(self.y) + " -> " + str(self.object))
        print("Adding: " + str(t_object))
        if t_object == tile_object.NONE:
            self.object = [tile_object.NONE]
        else:
            if tile_object.NONE in self.object:
                self.object.remove(tile_object.NONE)
            self.object.append(t_object)

        print("\n-----------New Tile Object " + str(self.x) + ", " + str(self.y) + " -> " + str(self.object))

    def remove_tile_object(self, t_object):
        if t_object in self.object:
            print("\n-----------Previous Tile Object " + str(self.x) + ", " + str(self.y) + " -> " + str(self.object))
            print("Removing: " + str(t_object))
            self.object.pop(self.object.index(t_object))
            if len(self.object) < 1:
                self.object.append(tile_object.NONE)
            print("\n-----------New Tile Object " + str(self.x) + ", " + str(self.y) + " -> " + str(self.object))


SMALL_MAP = 5
MEDIUM_MAP = 11
LARGE_MAP = 21

#--Map Functionality
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
                if not tile.danger_zone:
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
        Weapon("Knuckle Dusters", weapon_type.MELEE, 14, 1.2, 26, 1, None),
        Weapon("Crowbar", weapon_type.MELEE, 19, 1.5, 18, 1, None),
        Weapon("Axe", weapon_type.MELEE, 25, 1.7, 8, 21, None),
        Weapon("Shotgun", weapon_type.RANGED, 40, 1.8, 4, 28, 2)
    ]


def player_turn(_player, _grid_map):
    surrounding_tiles = _player.identify_new_information(_grid_map, tile_object)

    danger_tiles = _player.assess_information(surrounding_tiles, tile_object)

    print(danger_tiles)

    decision, details =_player.make_decision(danger_tiles, tile_object)

    assess_decision(_player, _grid_map, decision, details)

# TODO: Clean up to make more effecient, once the logic has been figured out
def assess_decision(_player, _grid_map, _decision, _details):
    if _decision == "move_player":
        # Decision: "move_playrer", Details: [[prev_x, prev_y], [new_x, new_y]]
        prev_x = _details[0][0]
        prev_y = _details[0][1]
        new_x = _details[1][0]
        new_y = _details[1][1]

        _grid_map[prev_x][prev_y].remove_tile_object(tile_object.PLAYER)
        _player.move_player(new_x, new_y)
        _grid_map[new_x][new_y].update_tile_object(tile_object.PLAYER)

    if _decision == "attack_enemy":
        print("ATTACK")

    if _decision == "no_moves":
        print("No Move")


#--Combat Functionality
def get_hit_limit_value(armour_value, mobility_value, attack_speed):
    print("Attacking Speed: " + str(attack_speed))

    print("Enemy Armour: " + str(armour_value) + " Mobility: " + str(mobility_value))

    if attack_speed > mobility_value:
        return round(((armour_value * 6) - ((armour_value * 3) / (attack_speed/mobility_value))) / 5)
    elif attack_speed < mobility_value:
        return round(((armour_value * 6) - ((armour_value * 3) * (attack_speed / mobility_value))) / 5)

def calculate_bypass_armour(hit_limit):
    return ((20 - hit_limit) / 3) * 2

def calculate_hit_damage(weapon_power_value):
    return random.randrange(int(weapon_power_value / 2), (weapon_power_value + 1))

def simulate_combat(attacking_player, enemy_player):
    hit_limit = get_hit_limit_value(enemy_player.get_current_armour(), enemy_player.get_current_mobility(),
                                    attacking_player.get_current_weapon().get_attack_speed())

    print("Hit Limit Value: " + str(hit_limit))

    bypass_armour_limit = round(hit_limit + calculate_bypass_armour(hit_limit))

    print("By Pass Limit Value: " + str(bypass_armour_limit))

    roll_value = attacking_player.attempt_action()

    if roll_value == 20:
        print("!!Critical Hit!!")
        hit_value = calculate_hit_damage(attacking_player.get_current_weapon().get_power())
        enemy_player.take_damage((hit_value * attacking_player.get_current_weapon().get_critical_multiplier()))

    elif roll_value >= bypass_armour_limit:
        print("Player Hit")
        hit_value = calculate_hit_damage(attacking_player.get_current_weapon().get_power())
        enemy_player.take_damage(hit_value)

    elif roll_value >= hit_limit:
        print("Armour Hit")
        armour_hit = random.randrange(1, 4)
        enemy_player.take_armour_damage(armour_hit)

    else:
        print("Miss")

    print("\n")


if __name__ == "__main__":
    map_size = SMALL_MAP

    grid_map = initializeMap(map_size)
    all_weapons = initializeWeapons()

    ring_close_turns = map_size // 2

    overall_count = 0

    player1 = Player(3, 1, 100, 10, 28, all_weapons[0])
    grid_map[3][1].update_tile_object(tile_object.PLAYER)
    player2 = Player(3, 1, 100, 10, 22, all_weapons[1])
    # grid_map[3][1].update_tile_object(tile_object.PLAYER)
    '''
    while player1.get_current_health() > 0 and player2.get_current_health() > 0:
        simulate_combat(player1, player2)
        simulate_combat(player2, player1)

        print("Player 1 Health: " + str(player1.get_current_health()) + " Player 2 Health: " + str(player2.get_current_health())
              + "\n\n------------------------------------------------------------------------")

    '''
    while overall_count < ring_close_turns:
        turn_count = 0

        displayMap(grid_map)

        while turn_count < 3:
            print("\nTurn: " + str(turn_count))
            time.sleep(3)
            player_turn(player1, grid_map)
            turn_count += 1

        encloseRing(grid_map, overall_count)

        print("\n\n")

        overall_count += 1

    displayMap(grid_map)