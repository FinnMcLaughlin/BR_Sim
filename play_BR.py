from player_class import Player
from weapon_class import Weapon
from Enum_Classes import tile_object_type, weapon_type
import random
import time

class GridTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.danger_zone = False
        self.object = [tile_object_type.NONE]

    def update_tile_object(self, t_object):
        #print("\n-----------Previous Tile Object " + str(self.x) + ", " + str(self.y) + " -> " + str(self.object))
        #print("Adding: " + str(t_object))
        if t_object == tile_object_type.NONE:
            self.object = [tile_object_type.NONE]
        else:
            if tile_object_type.NONE in self.object:
                self.object.remove(tile_object_type.NONE)
            self.object.append(t_object)

        #print("-----------New Tile Object " + str(self.x) + ", " + str(self.y) + " -> " + str(self.object))

    def remove_tile_object(self, t_object):
        if t_object in self.object:
            #print("\n-----------Previous Tile Object " + str(self.x) + ", " + str(self.y) + " -> " + str(self.object))
            #print("Removing: " + str(t_object))
            self.object.pop(self.object.index(t_object))
            if len(self.object) < 1:
                self.object.append(tile_object_type.NONE)
            #print("-----------New Tile Object " + str(self.x) + ", " + str(self.y) + " -> " + str(self.object))


SMALL_MAP = 5
MEDIUM_MAP = 11
LARGE_MAP = 21

all_players = []

#--Map Functionality
def initializeMap(size):
    return populate_grid(size, size)

def populate_grid(rows, columns):
    """
    Method to create a 2D array that represents the game map, where each tile contains an instance of the GridTile class

    :param rows: the amount of rows in the 2D array
    :param columns: the amount of columns in the 2D array
    :return: the initialized 2D array that represents the game map
    """
    tile_array = []

    for x in range(0, rows):
        col_array = []
        for y in range(0, columns):
            col_array.append(GridTile(x, y))

        tile_array.append(col_array)

    return tile_array

def encloseRing(_grid_map, count):
    """
    Method to periodically minimize the safe area of the map that the players can be inside of without them losing
    health. The method changes the danger zone boolean of each of the outer most safe tiles to True every x amount of
    turns.

    :param _grid_map: 2D array that represents the game map
    :param count: value of how many times the ring has closed since the beginning of the game
    """
    minimum = count
    maximum = (len(_grid_map)-1) - count

    for row in grid_map:
        for tile in row:
            if tile.x == minimum or tile.x == maximum or tile.y == minimum or tile.y == maximum:
                if not tile.danger_zone:
                    tile.danger_zone = True
                    tile.update_tile_object(tile_object_type.DANGER_ZONE)

def displayMap(_grid_map):
    """
    Method used for testing to display the current state of the map; the size, player locations, danger zone locations etc.

    :param _grid_map: 2D array that represents the game map
    """
    tiles = _grid_map

    for row in tiles:
        row_str = ""

        for col in range(len(row)):
            if tile_object_type.PLAYER in row[col].object:
                row_str = row_str + "player "
            else:
                row_str = row_str + str(row[col].danger_zone) + " "

        print(row_str)


#--Weapon Initialization
def initializeWeapons():
    """
    Very basic weapon initialization for testing current combat functionality

    :return: a list of 4 weapon instances

    # TODO: Streamline classes and initialization of weapons
    """
    return [
        Weapon("Knuckle Dusters", weapon_type.MELEE, 14, 1.2, 26, 1, None),
        Weapon("Crowbar", weapon_type.MELEE, 19, 1.5, 18, 1, None),
        Weapon("Axe", weapon_type.MELEE, 25, 1.7, 8, 21, None),
        Weapon("Shotgun", weapon_type.RANGED, 40, 1.8, 4, 28, 2)
    ]


#--Player Turn Functionality
def player_turn(_player, _grid_map):
    """
    Method to carry out a given player's turn, which follows these steps:
        - Identify New Information: The player takes into account all surrounding information, as well as the current
        status of the player (health, current weapon & equipment etc.)
        - Make Decision: Based on the information gathered in the previos step, the player contemplates all potential
        decisions it should make for it's turn, concluding with a final decision, and the details of the decision made
        - Assess Decision: Based on the decision made by the player, and the details of the decision, the player will
        then attempt to carry out the decision as an action, which might change the state of the player or the map

    :param _player: the player who's turn is being made
    :param _grid_map: 2D array that represents the game map
    """
    info_json = _player.identify_new_information(_grid_map)

    print(info_json)

    decision, details = _player.make_decision(info_json)

    assess_decision(_player, _grid_map, decision, details)

def assess_decision(_player, _grid_map, _decision, _details):
    """
    Method to attempt to carry out the action decided by the player on their turn, as well as updating the map when
    necessary

    :param _player: the player who's turn is being made
    :param _grid_map: 2D array that represents the game map
    :param _decision: the final decision made by the player
    :param _details: the details of the decision made by the player

    # TODO: Clean up to make more efficient, once the logic has been figured out
    # TODO: Add functionality to include the following actions: Combat, Looting, Healing
    """
    if _decision == "move_player":
        # Decision: "move_player", Details: [[prev_x, prev_y], [new_x, new_y]]
        prev_x = _details[0][0]
        prev_y = _details[0][1]
        new_x = _details[1][0]
        new_y = _details[1][1]

        _grid_map[prev_x][prev_y].remove_tile_object(tile_object_type.PLAYER)
        _player.move_player(new_x, new_y)
        _grid_map[new_x][new_y].update_tile_object(tile_object_type.PLAYER)

    if _decision == "attack_enemy":
        for other_player in all_players:
            if _player.get_current_position() == other_player.get_current_position() and not _player.get_player_name() == other_player.get_player_name():
                simulate_combat(_player, other_player)
                return


    if _decision == "no_moves":
        print("No Move")


#--Combat Functionality
def get_hit_limit_value(armour_value, mobility_value, attack_speed):
    """
    Method to calculate the minimum value the attacking player needs to roll on a D20 dice to hit the target player, which
    is based on the attack speed of the attacking player, as well as the armour value and mobility value of the target
    player

    :param armour_value: the armour value of the target player
    :param mobility_value: the mobility value of the target player
    :param attack_speed: the attack speed of the attacking player
    :return: the minimum value needed to not miss the target player
    """
    print("Attacking Speed: " + str(attack_speed))

    print("Enemy Armour: " + str(armour_value) + " Mobility: " + str(mobility_value))

    if attack_speed > mobility_value:
        return round(((armour_value * 6) - ((armour_value * 3) / (attack_speed/mobility_value))) / 5)
    elif attack_speed < mobility_value:
        return round(((armour_value * 6) - ((armour_value * 3) * (attack_speed / mobility_value))) / 5)

def calculate_bypass_armour(hit_limit):
    """
    Method to calculate the minimum value the attacking player needs to roll on a D20 dice to bypass the target player's
    armour and hit them directly

    :param hit_limit: the hit limit value calculated as the minimum value the attacking player needs to roll on a D20
    dice to hit the target player
    :return: the minimum value needed to hit the target player directly
    """
    return ((20 - hit_limit) / 3) * 2

def calculate_hit_damage(weapon_power_value):
    """
    Method to calculate the damage done to the target player. This is calculated by getting a random value between half
    the weapon power of the attacking player's weapon and the total weapon power of the attacking player's weapon

    :param weapon_power_value: the weapon power of the attacking player's weapon
    :return: the damage that the attacking player's attack has done to the target player
    """
    return random.randrange(int(weapon_power_value / 2), (weapon_power_value + 1))

def simulate_combat(attacking_player, target_player):
    """
    Simulation of an attack by one player to another. Combat simulation takes the following steps:
        - Calculating the hit limit value: Getting the minimum value the attacking player must roll on a D20 dice to not
        miss the target player
        - Calculating bypassing armour limit: Based on the hit limit value, the minimum value for the attacking player to
        bypass the armour and hit the target player directly is calculated
        - Attack attempt: Once the hit limit value and bypass armour value have been calculated, the attacking player
        attempts the action (i.e. gets a random integer between 1 & 20), hoping to successfully hit the target player

    :param attacking_player: the player who is attacking
    :param target_player: the player who is targeted
    """
    hit_limit = get_hit_limit_value(target_player.get_current_armour(), target_player.get_current_mobility(),
                                    attacking_player.get_current_weapon().get_attack_speed())

    print("Hit Limit Value: " + str(hit_limit))

    bypass_armour_limit = round(hit_limit + calculate_bypass_armour(hit_limit))

    print("By Pass Limit Value: " + str(bypass_armour_limit))

    roll_value = attacking_player.attempt_action()

    if roll_value == 20:
        print("!!Critical Hit!! on " + str(target_player.get_player_name()))
        hit_value = round(calculate_hit_damage(attacking_player.get_current_weapon().get_power()) * attacking_player.get_current_weapon().get_critical_multiplier())
        print("Hit For: " + str(hit_value))
        target_player.take_damage(hit_value)

    elif roll_value >= bypass_armour_limit:
        print(str(target_player.get_player_name()) + " Hit")
        hit_value = calculate_hit_damage(attacking_player.get_current_weapon().get_power())
        print("Hit For: " + str(hit_value))
        target_player.take_damage(hit_value)

    elif roll_value >= hit_limit:
        print(str(target_player.get_player_name()) + " Armour Hit")
        armour_hit = random.randrange(1, 4)
        target_player.take_armour_damage(armour_hit)

    else:
        print("Miss")

    print("\n")


#--Main
if __name__ == "__main__":
    map_size = MEDIUM_MAP

    grid_map = initializeMap(map_size)

    all_weapons = initializeWeapons()

    ring_close_turns = map_size // 2

    overall_count = 0

    p1_start_x, p1_start_y = 9, 1
    p2_start_x, p2_start_y = 10, 3

    player1 = Player("Player 1", p1_start_x, p1_start_y, 100, 10, 28, all_weapons[0])
    all_players.append(player1)
    grid_map[p1_start_x][p1_start_y].update_tile_object(tile_object_type.PLAYER)

    player2 = Player("Player 2", p2_start_x, p2_start_y, 100, 10, 22, all_weapons[1])
    all_players.append(player2)
    grid_map[p2_start_x][p2_start_y].update_tile_object(tile_object_type.PLAYER)

    #displayMap(grid_map)
    #player_turn(player1, grid_map)
    #player_turn(player2, grid_map)

    '''
    while player1.get_current_health() > 0 and player2.get_current_health() > 0:
        simulate_combat(player1, player2)
        simulate_combat(player2, player1)

        print("Player 1 Health: " + str(player1.get_current_health()) + " Player 2 Health: " + str(player2.get_current_health())
              + "\n\n------------------------------------------------------------------------")'''


    while overall_count < ring_close_turns:
        turn_count = 0

        displayMap(grid_map)

        while turn_count < 3:
            print("\nTurn: " + str(turn_count))
            time.sleep(3)
            player_turn(player1, grid_map)
            player_turn(player2, grid_map)
            turn_count += 1

        encloseRing(grid_map, overall_count)

        print("\n\n")

        overall_count += 1

    while len(all_players) > 1:
        if player1.get_current_health() > 0:
            player_turn(player1, grid_map)
        else:
            all_players.remove(player1)
        time.sleep(2)
        if player2.get_current_health() > 0:
            player_turn(player2, grid_map)
        else:
            all_players.remove(player2)

    print("Winner is: " + str(all_players[0].get_player_name()))