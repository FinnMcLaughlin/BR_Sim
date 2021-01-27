import json

class Player:
    def __init__(self, _x, _y, _health, _weapon):
        self.x = _x
        self.y = _y
        self.health = _health
        self.weapon = _weapon

    #--General Information Methods
    def get_current_position(self):
        return self.x, self.y

    def get_current_health(self):
        return self.health

    def get_current_weapon(self):
        return self.weapon


    #--Identify Methods
    def identify_new_information(self, tile_map, tile_object):
        surrounding_tiles = self.check_surroundings(tile_map, tile_object)
        return surrounding_tiles

    # Check contents of surrounding tiles
    def check_surroundings(self, tile_map, tile_object):
        surround_tiles = []

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
    def assess_information(self, surrounding_tiles, tile_objects):
        danger_tiles = []
        surr_tile_index = 0

        for tile in surrounding_tiles:
            if not tile == tile_objects.NONE:
                danger_info = {surr_tile_index: tile}
                danger_tiles.append(danger_info)

            surr_tile_index += 1

        return danger_tiles

    def make_decision(self, danger_tiles):
        # Index 0 - Danger Above - Move Y-1
        # Index 1 - Danger Right - Move X-1
        # Index 2 - Danger Below - Move Y+1
        # Index 3 - Danger Left - Move X+1

        if len(danger_tiles) > 0:
            for tile in danger_tiles:
                for index in tile:
                    print(str(index) + " " + str(tile[index]))

                    if index == 0:
                        curr_x, curr_y = self.get_current_position()
                        self.move_player(curr_x, curr_y+1)
                        return
                    if index == 1:
                        curr_x, curr_y = self.get_current_position()
                        self.move_player(curr_x-1, curr_y)
                        return
                    if index == 2:
                        curr_x, curr_y = self.get_current_position()
                        self.move_player(curr_x, curr_y-1)
                        return
                    if index == 3:
                        curr_x, curr_y = self.get_current_position()
                        self.move_player(curr_x+1, curr_y)
                        return


    #--Attempt Methods
    def attempt_decision(self):
        pass

    def move_player(self, new_x, new_y):
        print("Old Position: " + str(self.get_current_position()))

        self.x = new_x
        self.y = new_y

        print("New Position: " + str(self.get_current_position()))


    #--Combat Methods
    def take_damage(self, hit_value):
        self.health = self.health - hit_value