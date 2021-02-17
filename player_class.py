from Enum_Classes import tile_object_type, weapon_type
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
    # Gets surrounding tile info, updated health, combat info etc.
    def identify_new_information(self, tile_map):
        info_json = "{\"surr_tiles\": " + str(self.check_surroundings(tile_map)) +\
                    ", \"curr_health\": " + str(self.get_current_health()) + \
                    "}"

        return json.loads(info_json)

    def update_surrounding_tile_object_arrays(self, d_zone_array, enemy_array, tile, tile_pos):
        for t_object in tile.object:
            if t_object.value == 1:
                d_zone_array.append(tile_pos)
            # TODO: Update so that the tile the player is currently in checks for more than one player object before declaring an enemy is present
            if t_object.value == 2:
                enemy_array.append(tile_pos)

        return d_zone_array, enemy_array

    # Check contents of current tile and surrounding tiles
    # TODO: Clean up to make more effecient, once the logic has been figured out
    def check_surroundings(self, tile_map):
        danger_zone_coords = []
        enemy_zone_coords = []
        # building_zone_coords = []

        self.update_surrounding_tile_object_arrays(danger_zone_coords, enemy_zone_coords, tile_map[self.x][self.y], 0)

        if not self.x - 1 < 0:
            self.update_surrounding_tile_object_arrays(danger_zone_coords, enemy_zone_coords, tile_map[self.x-1][self.y], 1)
        else:
            danger_zone_coords.append(1)

        try:
            self.update_surrounding_tile_object_arrays(danger_zone_coords, enemy_zone_coords, tile_map[self.x][self.y+1], 2)
        except IndexError:
            danger_zone_coords.append(2)

        try:
            self.update_surrounding_tile_object_arrays(danger_zone_coords, enemy_zone_coords, tile_map[self.x+1][self.y], 3)
        except IndexError:
            danger_zone_coords.append(3)

        if not self.y - 1 < 0:

            self.update_surrounding_tile_object_arrays(danger_zone_coords, enemy_zone_coords, tile_map[self.x][self.y-1], 4)
        else:
            danger_zone_coords.append(4)

        return "{\"danger_zone\": " + str(danger_zone_coords)+ ", \"enemy\": " + str(enemy_zone_coords) + "}"

    #--Assessment Methods
    # Based on the surrounding tiles, whether or not any danger is present is stored in the danger_tile list
    def assess_information(self, _json_info):
        # Index 1 - Danger Above - Move X+1
        # Index 2 - Danger Right - Move Y-1
        # Index 3 - Danger Below - Move X-1
        # Index 4 - Danger Left - Move Y+1

        # return player_action: [action_details]

        decision_json = "[]"

        if len(_json_info['surr_tiles']['danger_zone']) > 0:
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

        return json.loads(decision_json)

    # TODO: Clean up to make more effecient, once the logic has been figured out. Add make decsion for combat, looting etc.
    def make_decision(self, _info_json):
        decision_json = self.assess_information(_info_json)

        print(decision_json)
        if len(decision_json) > 0:
            for key in decision_json[0]:
                if key == "move_player":
                    return key, decision_json[0][key]

        else:
            return "no_moves", []


    #--Attempt Methods
    def attempt_action(self):
        return random.randrange(1, 21)

    def move_player(self, new_x, new_y):
        print("Old Position: " + str(self.get_current_position()))

        self.x = new_x
        self.y = new_y

        print("New Position: " + str(self.get_current_position()))


    #--Combat Methods
    def take_damage(self, hit_value):
        self.health = self.health - hit_value

        if self.health < 0:
            self.health = 0

    def take_armour_damage(self, value):
        self.armour = self.armour - value

        if self.armour < 1:
            self.armour = 1

    def update_mobility(self, value):
        self.mobility = self.mobility + value