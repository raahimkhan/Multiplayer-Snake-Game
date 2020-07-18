import curses
from Constants import *


class Renderer:
    def __init__(self, height, width):
        self.stdscr = curses.initscr()
        self.h, self.w = height, width
        self.stdscr = curses.newwin(self.h, self.w, 0, 0)
        self.stdscr.keypad(True)
        self.stdscr.timeout(100)
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

    def refresh_window(self):
        self.stdscr.clear()
        self.stdscr.border(0)

    def take_input(self):
        return self.stdscr.getch()

    def draw_items(self, items_arr):
        for item in items_arr:          
            self.stdscr.addstr(item[0],item[1],SNAKE_SEGMENT)

        self.stdscr.refresh()


    def destroy(self):
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
