from graphics import Point, Line
import random
import time
import pdb


class Cell:
    def __init__(self,
                 x_start,
                 y_start,
                 x_end,
                 y_end,
                 win=None,
                 has_left_wall=True,
                 has_right_wall=True,
                 has_top_wall=True,
                 has_bottom_wall=True
                 ):

        self.__x_start = x_start
        self.__y_start = y_start
        self.__x_end = x_end
        self.__y_end = y_end
        self.__win = win
        self.visited = False
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall

    def draw(self):
        if self.__win is None:
            return

        left_line = Line(
            Point(self.__x_start, self.__y_start),
            Point(self.__x_start, self.__y_end)
        )
        if self.has_left_wall:
            self.__win.draw_line(left_line)
        else:
            self.__win.draw_line(left_line, 'white')

        right_line = Line(
            Point(self.__x_end, self.__y_start),
            Point(self.__x_end, self.__y_end)
        )
        if self.has_right_wall:
            self.__win.draw_line(right_line)
        else:
            self.__win.draw_line(right_line, 'white')

        top_line = Line(
            Point(self.__x_start, self.__y_start),
            Point(self.__x_end, self.__y_start)
        )
        if self.has_top_wall:
            self.__win.draw_line(top_line)
        else:
            self.__win.draw_line(top_line, 'white')

        bottom_line = Line(
            Point(self.__x_start, self.__y_end),
            Point(self.__x_end, self.__y_end)
        )
        if self.has_bottom_wall:
            self.__win.draw_line(bottom_line)
        else:
            self.__win.draw_line(bottom_line, 'white')

    def middle(self):
        x_middle = (self.__x_start + self.__x_end) / 2
        y_middle = (self.__y_start + self.__y_end) / 2
        return Point(x_middle, y_middle)

    def draw_move(self, dest_cell, undo=False):
        if self.__win is None:
            return

        fill = 'red'
        if undo:
            fill = 'gray'

        line = Line(self.middle(), dest_cell.middle())
        self.__win.draw_line(line, fill)


class Maze:
    def __init__(self,
                 x_start,
                 y_start,
                 num_rows,
                 num_cols,
                 cell_size_x,
                 cell_size_y,
                 win=None,
                 seed=None,
                 ):
        self.__x_start = x_start
        self.__y_start = y_start
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []

        if seed:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_visited()

    def __create_cells(self):
        for i in range(self.__num_rows):
            row = []
            for j in range(self.__num_cols):
                row.append(
                    Cell(
                        self.__x_start + j * self.__cell_size_x,
                        self.__y_start + i * self.__cell_size_y,
                        self.__x_start + (j + 1) * self.__cell_size_x,
                        self.__y_start + (i + 1) * self.__cell_size_y,
                        self.__win
                    )
                )
            self.__cells.append(row)
            if self.__win is not None:
                for j in range(self.__num_cols):
                    self.__draw_cell(i, j)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__cells[self.__num_rows -
                     1][self.__num_cols - 1].has_bottom_wall = False
        if self.__win is not None:
            self.__draw_cell(0, 0)
            self.__draw_cell(self.__num_rows - 1, self.__num_cols - 1)

    def __get_neighbors_directions(self, i, j):
        neighbors = []
        if i != 0:
            neighbors.append((-1, 0))
        if j != 0:
            neighbors.append((0, -1))
        if i != self.__num_rows - 1:
            neighbors.append((1, 0))
        if j != self.__num_rows - 1:
            neighbors.append((0, 1))
        return neighbors

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        neighbors_directions = self.__get_neighbors_directions(i, j)

        while True:
            unvisited_directions = list(filter(
                lambda pos: not self.__cells[i + pos[0]][j + pos[1]].visited,
                neighbors_directions))

            n_directions = len(unvisited_directions)
            if n_directions == 0:
                self.__draw_cell(i, j)
                return

            next_dir = unvisited_directions[random.randrange(n_directions)]
            match next_dir:
                case (-1, 0):
                    self.__cells[i][j].has_top_wall = False
                    self.__cells[i - 1][j].has_bottom_wall = False
                case (1, 0):
                    self.__cells[i][j].has_bottom_wall = False
                    self.__cells[i + 1][j].has_top_wall = False
                case (0, -1):
                    self.__cells[i][j].has_left_wall = False
                    self.__cells[i][j - 1].has_right_wall = False
                case (0, 1):
                    self.__cells[i][j].has_right_wall = False
                    self.__cells[i][j + 1].has_left_wall = False

            self.__break_walls_r(i + next_dir[0], j + next_dir[1])

    def __reset_visited(self):
        for row in self.__cells:
            for cell in row:
                cell.visited = False

    def __solve_r(self, i, j):

        # This introduces a time pause to animate the algorithm
        self.__animate()

        if (i == self.__num_rows - 1 and j == self.__num_cols - 1):
            return True

        self.__cells[i][j].visited = True

        paths = []
        # Remember starting cell has no top wall
        if not (i == 0 and j == 0):
            if not (self.__cells[i][j].has_top_wall
                    or self.__cells[i - 1][j].visited):
                paths.append((i - 1, j))

        if not (self.__cells[i][j].has_left_wall
                or self.__cells[i][j - 1].visited):
            paths.append((i, j - 1))

        if not (self.__cells[i][j].has_right_wall
                or self.__cells[i][j + 1].visited):
            paths.append((i, j + 1))

        if not (self.__cells[i][j].has_bottom_wall
                or self.__cells[i + 1][j].visited):
            paths.append((i + 1, j))

        for y, x in paths:
            self.__cells[i][j].draw_move(
                self.__cells[y][x])
            if self.__solve_r(y, x):
                return True
            self.__cells[i][j].draw_move(
                self.__cells[y][x], undo=True)

        return False

    def solve(self):
        return self.__solve_r(0, 0)

    def __animate(self):
        self.__win.redraw()
        time.sleep(0.005)

    def __draw_cell(self, i, j):
        self.__cells[i][j].draw()
        self.__animate()
