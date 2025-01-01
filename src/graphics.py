from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = 'Maze Solver'
        self.__root.geometry(f"{width}x{height}")

        self.__canvas = Canvas(width=width, height=height)
        self.__canvas.pack(expand=1, fill=BOTH)

        self.__is_running = False
        # This line connects the closing event of the GUI to the call
        # of the close() method of this class
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()

    def draw_line(self, line, fill='black'):
        line.draw(self.__canvas, fill)

    def close(self):
        self.__is_running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point_start, point_end):
        self.point_start = point_start
        self.point_end = point_end

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point_start.x,
            self.point_start.y,
            self.point_end.x,
            self.point_end.y,
            fill=fill_color,
            width=2
        )
