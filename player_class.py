import random
import json

class Player:
    def __init__(self, _x, _y, _health, _armour, _mobility, _weapon):
        self.x = _x
        self.y = _y
        self.health = _health
        self.armour = _armour
        self.mobility = _mobility
        self.weapon = _weapon

    #--General Information Methods
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
    def identify_new_information(self, tile_map, tile_object):
        surrounding_tiles = self.check_surroundings(tile_map, tile_object)
        return surrounding_tiles

    # Check contents of current tile and surrounding tiles
    # TODO: Clean up to make more effecient, once the logic has been figured out
    def check_surroundings(self, tile_map, tile_object):
        surround_tiles = [
            tile_map[self.x][self.y].object
        ]

        if not self.y - 1 < 0:
            surround_tiles.append(tile_map[self.x][self.y - 1].object)
        else:
            surround_tiles.append(tile_object.DANGER_ZONE)

        try:
            surround_tiles.append(tile_map[self.x + 1][self.y].object)
        except IndexError:
            surround_tiles.append(tile_object.DANGER_ZONE)

        try:
            surround_tiles.append(tile_map[self.x][self.y + 1].object)
        except IndexError:
            surround_tiles.append(tile_object.DANGER_ZONE)

        if not self.x - 1 < 0:
            surround_tiles.append(tile_map[self.x - 1][self.y].object)
        else:
            surround_tiles.append(tile_object.DANGER_ZONE)

        return surround_tiles

    #--Assessment Methods
    # Based on the surrounding tiles, whether or not any danger is present is stored in the danger_tile list
    def assess_information(self, surrounding_tiles, tile_objects):
        danger_tiles = []
        surr_tile_index = 0

        for tile in surrounding_tiles:
            print("TILE: " + str(tile))
            if not tile_objects.NONE in tile:
                danger_info = {surr_tile_index: tile}
                danger_tiles.append(danger_info)

            surr_tile_index += 1

        return danger_tiles

    # TODO: Clean up to make more effecient, once the logic has been figured out
    def make_decision(self, danger_tiles, t_object):
        # Index 1 - Danger Above - Move Y+1
        # Index 2 - Danger Right - Move X-1
        # Index 3 - Danger Below - Move Y-1
        # Index 4 - Danger Left - Move X+1

        # return player_action: [action_details]

        # If DANGER_ZONE in danger_tiles, move
        # Elif PLAYER in danger_tiles, combat

        enemy_present = False
        enemy_index = 0
        danger_zone_present = False
        danger_index = 0

        if len(danger_tiles) > 0:
            for tile in danger_tiles:
                for index in tile:

                    print(str(index) + " " + str(tile[index]))

                    if t_object.DANGER_ZONE in tile[index] :
                        danger_zone_present = True
                        danger_index = index

                    if t_object.PLAYER in tile[index]:
                        enemy_present = True
                        enemy_index = index


        if danger_zone_present:
            if danger_index == 1:
                curr_x, curr_y = self.get_current_position()
                return "move_player", [[curr_x, curr_y], [curr_x, curr_y+1]]
            if danger_index == 2:
                curr_x, curr_y = self.get_current_position()
                return "move_player", [[curr_x, curr_y], [curr_x - 1, curr_y]]
            if danger_index == 3:
                curr_x, curr_y = self.get_current_position()
                return "move_player", [[curr_x, curr_y], [curr_x, curr_y - 1]]
            if danger_index == 4:
                curr_x, curr_y = self.get_current_position()
                return "move_player", [[curr_x, curr_y], [curr_x + 1, curr_y]]

        '''if enemy_present:
            if enemy_index == 0:
                curr_x, curr_y = self.get_current_position()
                return "attack_enemy", [[curr_x, curr_y], [curr_x, curr_y+1]]
            if enemy_index == 1:
                curr_x, curr_y = self.get_current_position()
                return "attack_enemy", [[curr_x, curr_y], [curr_x - 1, curr_y]]
            if enemy_index == 2:
                curr_x, curr_y = self.get_current_position()
                return "attack_enemy", [[curr_x, curr_y], [curr_x, curr_y - 1]]
            if enemy_index == 3:
                curr_x, curr_y = self.get_current_position()
                return "attack_enemy", [[curr_x, curr_y], [curr_x + 1, curr_y]]'''

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