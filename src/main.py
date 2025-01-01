import graphics
from maze import Maze


def main():
    window = graphics.Window(800, 600)
    n_rows = 10
    n_cols = 10
    maze = Maze(100, 100, n_rows, n_cols, 600/n_rows, 400/n_cols, window)
    window.wait_for_close()


if __name__ == "__main__":
    main()
