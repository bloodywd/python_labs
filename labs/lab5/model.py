import copy
import random
from enum import Enum


class BlockType(Enum):
    STRAIGHT = 0
    CORNER = 1


class Block:
    def __init__(self, block_type, rotation=random.randint(0, 3), is_lit=False):
        self.block_type = block_type
        self.rotation = rotation
        self.is_lit = is_lit

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def randomize_rotation(self):
        self.rotation = random.randint(0, 3)

    def light_up(self):
        self.is_lit = True

    def light_down(self):
        self.is_lit = False

    def get_connections(self):
        if self.block_type == BlockType.STRAIGHT:
            return ["up", "down"] if self.rotation % 2 == 0 else ["left",
                                                                  "right"]
        else:
            return [
                ["up", "right"],
                ["down", "right"],
                ["left", "down"],
                ["up", "left"]
            ][self.rotation]


class GameBoardModel:
    DIRECTIONS = {
        'left': (0, -1),
        'right': (0, 1),
        'up': (-1, 0),
        'down': (1, 0)
    }

    OPPOSITE_DIRECTIONS = {
        'up': 'down',
        'right': 'left',
        'down': 'up',
        'left': 'right'
    }

    def __init__(self, size):
        self.size = size
        self.grid = []
        self.solved_grid = []
        self.create_board()

    @staticmethod
    def get_block_type_and_rotation(conns):
        CORNER_ROTATIONS = {
            ("right", "up"): 0,
            ("down", "right"): 1,
            ("down", "left"): 2,
            ("left", "up"): 3,
        }

        STRAIGHT_ROTATIONS = {
            ("down", "up"): 0,
            ("left", "right"): 1,
            ("up",): 0,
            ("down",): 0,
            ("right",): 1,
            ("left",): 1,
        }
        if conns in STRAIGHT_ROTATIONS.keys():
            return STRAIGHT_ROTATIONS[conns], BlockType.STRAIGHT
        else:
            return CORNER_ROTATIONS[conns], BlockType.CORNER

    def create_board(self):
        connections = self.path_to_connections(self.generate_slice_path())

        for i in range(self.size):
            row = []
            for j in range(self.size):
                conns = connections[i][j]
                rotation, block_type = GameBoardModel.get_block_type_and_rotation(
                    tuple(sorted(conns)))

                block = Block(block_type, rotation)
                row.append(block)
            self.solved_grid.append(row)

        self.grid = copy.deepcopy(self.solved_grid)

        for row in self.grid:
            for block in row:
                block.randomize_rotation()

        self.update_lightning()

    def generate_slice_path(self):
        size = self.size
        path = []

        def slice(start_point, width, height, offset=(0, 0)):
            nonlocal path
            offset_x, offset_y = offset
            x, y = start_point

            if width <= 0 or height <= 0:
                return

            direction = random.choice(["x", "y"]) if (
                        width > 1 and height > 1) else "x" if width > height else "y"

            if direction == "y":
                step = 1 if y == 0 else -1
                end = width if step == 1 else -1
                while y != end:
                    path.append((x + offset_x, y + offset_y))
                    y += step

                new_width = width
                new_height = height - 1
                new_offset = (offset_x + 1, offset_y) if x == 0 else (offset_x, offset_y)
                new_start = (0 if x == 0 else new_height - 1,
                             new_width - 1 if step == 1 else 0)

            else:
                step = 1 if x == 0 else -1
                end = height if step == 1 else -1
                while x != end:
                    path.append((x + offset_x, y + offset_y))
                    x += step

                new_width = width - 1
                new_height = height
                new_offset = (offset_x, offset_y + 1) if y == 0 else (offset_x, offset_y)
                new_start = (new_height - 1 if step == 1 else 0,
                             0 if y == 0 else new_width - 1)

            slice(new_start, new_width, new_height, new_offset)

        slice((0, 0), size, size)
        return path

    def path_to_connections(self, path):
        connections = [[[] for _ in range(self.size)] for _ in
                       range(self.size)]

        for idx in range(len(path) - 1):
            i1, j1 = path[idx]
            i2, j2 = path[idx + 1]
            di, dj = i2 - i1, j2 - j1

            for dir_name, (ddi, ddj) in self.DIRECTIONS.items():
                if (di, dj) == (ddi, ddj):
                    connections[i1][j1].append(dir_name)
                    connections[i2][j2].append(
                        self.OPPOSITE_DIRECTIONS[dir_name])
                    break

        return connections

    def get_board(self):
        return self.grid

    def set_board_to_solved(self):
        self.grid = self.solved_grid
        self.update_lightning()

    def get_size(self):
        return self.size

    def update_lightning(self):
        for row in self.grid:
            for block in row:
                block.light_down()

        self.grid[0][0].light_up()

        queue = [(0, 0)]
        while queue:
            i, j = queue.pop(0)
            current_block = self.grid[i][j]
            for direction in current_block.get_connections():
                di, dj = self.__class__.DIRECTIONS[direction]
                ni, nj = i + di, j + dj

                if 0 <= ni < self.size and 0 <= nj < self.size:
                    neighbor = self.grid[ni][nj]
                    opposite_dir = self.__class__.OPPOSITE_DIRECTIONS[
                        direction]
                    if opposite_dir in neighbor.get_connections() and not neighbor.is_lit:
                        neighbor.light_up()
                        queue.append((ni, nj))

    def rotate_block(self, i, j):
        self.grid[i][j].rotate()
        self.update_lightning()
        return self.is_win()

    def is_win(self):
        return all(block.is_lit for row in self.grid for block in row)
