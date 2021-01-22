from play_BR import tile_object

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
    def identify_new_information(self, tile_map):
        surrounding_tiles = self.check_surroundings(tile_map)
        return surrounding_tiles

    # Check contents of surrounding tiles
    def check_surroundings(self, tile_map):
        surrounding_tile_contents = [
            tile_map[self.x][self.y + 1].tile_object,
            tile_map[self.x + 1][self.y].tile_object,
            tile_map[self.x][self.y - 1].tile_object,
            tile_map[self.x - 1][self.y].tile_object
        ]

        return surrounding_tile_contents


    #--Assessment Methods
    def assess_decisions(self, surrounding_tiles):
        pass


    #--Attempt Methods
    def attempt_decision(self):
        pass

    def move_player(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


    #--Combat Methods
    def take_damage(self, hit_value):
        self.health = self.health - hit_value