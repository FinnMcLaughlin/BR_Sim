import time

class GridTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.danger_zone = False

SMALL_MAP = 5
MEDIUM_MAP = 11
LARGE_MAP = 21

def iniatilzeMap(size):
    return populate_grid(size, size)


def populate_grid(rows, columns):
    tile_array = []

    for x in range(0, rows):
        col_array = []
        for y in range(0, columns):
            col_array.append(GridTile(x, y))

        tile_array.append(col_array)

    return tile_array


def encloseRing(grid_map, count):
    minimum = count
    maximum = (len(grid_map)-1) - count

    print(minimum)
    print(maximum)

    for row in grid_map:
        for tile in row:
            if tile.x == minimum or tile.x == maximum or tile.y == minimum or tile.y == maximum:
                tile.danger_zone = True


def displayMap(grid_map):
    tiles = grid_map

    for row in tiles:
        row_str = ""

        for col in range(len(row)):
            row_str = row_str + str(row[col].danger_zone) + " "

        print(row_str)


if __name__ == "__main__":
    map_size = MEDIUM_MAP

    grid_map = iniatilzeMap(map_size)

    ring_close_turns = map_size // 2

    overall_count = 0

    while overall_count < ring_close_turns:
        turn_count = 0

        displayMap(grid_map)

        while turn_count < 3:
            print("Turn: " + str(turn_count))
            time.sleep(3)
            turn_count += 1

        encloseRing(grid_map, overall_count)

        print("\n\n")

        overall_count += 1

    displayMap(grid_map)