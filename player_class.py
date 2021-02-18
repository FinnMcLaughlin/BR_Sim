import random
import json

class Player:
    def __init__(self, _name, _x, _y, _health, _armour, _mobility, _weapon):
        self.name = _name
        self.x = _x
        self.y = _y
        self.health = _health
        self.armour = _armour
        self.mobility = _mobility
        self.weapon = _weapon

    #--General Information Methods
    def get_player_name(self):
        return self.name

    def get_current_position(self):
        return self.x, self.y

    def get_current_health(self):
        return self.health

    def get_current_armour(self):
        return self.armour

    def get_current_mobility(self):
        return self.mobility

    def get_current_weapon(self):
        return self.weapon


    #--Identify Methods
    def identify_new_information(self, tile_map):
        """
        Method to get the contents of the surrounding tiles, the players current health, combat information etc. that will
        be factored into the decision made by the player each time it is their turn to perform an action

        :param tile_map: 2D array containing information on each tile in the map
        :return: json object of all necessary information to be factored into the player's decision for what action to
        carry out on their turn

        # TODO: Add functionality to include the following in the JSON object: Combat Information, Current Weapon & Equipment
        """
        info_json = "{\"surr_tiles\": " + str(self.check_surroundings(tile_map)) +\
                    ", \"curr_health\": " + str(self.get_current_health()) + \
                    "}"

        return json.loads(info_json)

    def update_surrounding_tile_object_arrays(self, d_zone_array, enemy_array, tile, tile_pos):
        """
        Function that checks a given tiles object based on the enum class 'tile object type' and updates the respective
        list with it's position in relation to the player's current position

        :param d_zone_array: list containing the index of the danger zone in relation to the player's current position
        :param enemy_array: list containing the index of the enemy position(s) in relation to the player's current position
        :param tile: the tile that is being checked
        :param tile_pos: the index of the tile in relation to the current position of the player
        :return: the updated lists of the danger_zone & enemy array

        # TODO: Add functionality to include the following in the surround check: Buildings
        """
        for t_object in tile.object:
            if t_object.value == 1:
                d_zone_array.append(tile_pos)
            if t_object.value == 2:
                enemy_array.append(tile_pos)
            if t_object.value == 3:
                #building_array.append(tile_pos)
                continue

        return d_zone_array, enemy_array

    def check_surroundings(self, tile_map):
        """
        Method to return information on the player's surrounding tiles, that will be factored into the decision made on
        the player's turn

        :param tile_map: 2D array containing information on each tile in the map
        :return: json string of lists containing the index of their respective danger in relation to the player

        # TODO: Clean up to make more efficient, once the logic has been figured out
        """

        danger_zone_coords = []
        enemy_zone_coords = []
        # building_zone_coords = []

        # Tile the player is currently in
        self.update_surrounding_tile_object_arrays(danger_zone_coords, enemy_zone_coords, tile_map[self.x][self.y], 0)

        # Tile north of player
        if not self.x - 1 < 0:
            self.update_surrounding_tile_object_arrays(danger_zone_coords, enemy_zone_coords, tile_map[self.x-1][self.y], 1)
        else:
            danger_zone_coords.append(1)

        # Tile east of player
        try:
            self.update_surrounding_tile_object_arrays(danger_zone_coords, enemy_zone_coords, tile_map[self.x][self.y+1], 2)
        except IndexError:
            danger_zone_coords.append(2)

        # Tile south of player
        try:
            self.update_surrounding_tile_object_arrays(danger_zone_coords, enemy_zone_coords, tile_map[self.x+1][self.y], 3)
        except IndexError:
            danger_zone_coords.append(3)

        # Tile west of player
        if not self.y - 1 < 0:
            self.update_surrounding_tile_object_arrays(danger_zone_coords, enemy_zone_coords, tile_map[self.x][self.y-1], 4)
        else:
            danger_zone_coords.append(4)

        # Removes one instance of a player object from the player's current tile, as that is the player themselves
        enemy_zone_coords.remove(0)

        return "{\"danger_zone\": " + str(danger_zone_coords)+ ", \"enemy\": " + str(enemy_zone_coords) + "}"

    #--Assessment Methods
    def assess_information(self, _json_info):
        """
        Based on the info_json object, decisions are made and formatted into a decision_json object

        Index 1 - Danger Above - Move X+1 (1 row down)
        Index 2 - Danger Right - Move Y-1 (1 column left)
        Index 3 - Danger Below - Move X-1 (1 row up)
        Index 4 - Danger Left - Move Y+1  (1 column right)

        :param _json_info: json object containing information on surrounding tiles
        :return: all possible decisions the player can make, formatted as json object

        TODO: Clean up to make more efficient, once the logic has been figured out
        """

        decision_json = "[]"

        # If all surrounding tiles are danger_zone, then the player can no longer move
        if 0 < len(_json_info['surr_tiles']['danger_zone']) < 4:
            curr_x, curr_y = self.get_current_position()

            danger_index = _json_info['surr_tiles']['danger_zone'][0]

            move_decision = "{\"move_player\": "

            if danger_index == 1:
                move_decision = move_decision + str([[curr_x, curr_y], [curr_x + 1, curr_y]]) + "}"
            if danger_index == 2:
                move_decision = move_decision + str([[curr_x, curr_y], [curr_x, curr_y - 1]]) + "}"
            if danger_index == 3:
                move_decision = move_decision + str([[curr_x, curr_y], [curr_x - 1, curr_y]]) + "}"
            if danger_index == 4:
                move_decision = move_decision + str([[curr_x, curr_y], [curr_x, curr_y + 1]]) + "}"

            decision_json = decision_json[:-1] + move_decision + "]"

        elif len(_json_info['surr_tiles']['enemy']) > 0:
            curr_x, curr_y = self.get_current_position()

            enemy_index = _json_info['surr_tiles']['enemy'][0]

            if enemy_index == 0:
                decision_json = decision_json[:-1] + "{\"attack_enemy\": []} ]"
                print(decision_json)
                return json.loads(decision_json)

            move_decision = "{\"move_player\": "

            if enemy_index == 1:
                move_decision = move_decision + str([[curr_x, curr_y], [curr_x + 1, curr_y]]) + "}"
            if enemy_index == 2:
                move_decision = move_decision + str([[curr_x, curr_y], [curr_x, curr_y - 1]]) + "}"
            if enemy_index == 3:
                move_decision = move_decision + str([[curr_x, curr_y], [curr_x - 1, curr_y]]) + "}"
            if enemy_index == 4:
                move_decision = move_decision + str([[curr_x, curr_y], [curr_x, curr_y + 1]]) + "}"

            decision_json = decision_json[:-1] + move_decision + "]"

        return json.loads(decision_json)

    def make_decision(self, _info_json):
        """
        Method to make a decision on behalf of the player based on info JSON object passed in, which is subsequently
        passed to the assess_information method, for a list of possible decisions that the player should make

        :param _info_json: json object containing information on surrounding tiles
        :return: json object containing information on the move decided by the player

        # TODO: Clean up to make more effecient, once the logic has been figured out. Add make decsion for combat, looting etc.
        # TODO: Add functionality to include the following in the surround check: Combat, Looting, Healing
        """
        decision_json = self.assess_information(_info_json)

        print(decision_json)

        if len(decision_json) > 0:
            for key in decision_json[0]:
                if key == "move_player":
                    return key, decision_json[0][key]
                if key == "attack_enemy":
                    return key, decision_json[0][key]

        else:
            return "no_moves", []


    #--Attempt Methods
    def attempt_action(self):
        """
        Method that essentially rolls a D20 dice, representing how successful the player's attempt at performing an
        action

        :return: a random integer from 1 - 20
        """
        return random.randrange(1, 21)

    def move_player(self, new_x, new_y):
        """
        Method to move the player to a new position on the map

        :param new_x: New X Coordinate of the player (Row)
        :param new_y: New Y Coordinate of the player (Column)
        """
        print("Old Position: " + str(self.get_current_position()))

        self.x = new_x
        self.y = new_y

        print("New Position: " + str(self.get_current_position()))


    #--Combat Methods
    def take_damage(self, hit_value):
        """
        Method to take damage to the player's health when in combat situation. If the player's health drops below 0, the
        player's health is reset to 0, as that is the lowest it can potentially be

        :param hit_value: The value of the damage taken from the player's health
        """
        self.health = self.health - hit_value

        if self.health < 0:
            self.health = 0

    def take_armour_damage(self, value):
        """
        Method to take damage to the player's armour when in combat situation. If the player's armour drops below 1, the
        player's armour is reset to 1, as that is the lowest it can potentially be

        :param value: The value of the damage taken from the player's armour
        """
        self.armour = self.armour - value

        if self.armour < 1:
            self.armour = 1

    def update_mobility(self, value):
        """
        Updates the player's mobility. This value may rise or fall based on the total weight of the equipment the player
        is carrying (weapon, armour etc.)

        :param value: The value that player's mobility will update by (can be a negative value)
        """
        self.mobility = self.mobility + value