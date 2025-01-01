import graphics
from maze import Maze


def main():
    window = graphics.Window(800, 600)
    n_rows = 30
    n_cols = 30
    maze = Maze(100, 100, n_rows, n_cols, 600 /
                n_rows, 400/n_cols, window)
    maze.solve()
    window.wait_for_close()


if __name__ == "__main__":
    main()
