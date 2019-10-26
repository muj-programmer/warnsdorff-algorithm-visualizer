import curses
from .cursor import Cursor
from typing import List
from time import sleep


def horizontal_line(stdscr, cursor: Cursor) -> None:
    '''
    horizontal boundry line
    '''
    cursor.set_x(1)
    stdscr.addstr(cursor.get_y(), cursor.get_x(), '-' * 29,
                  curses.color_pair(1))
    cursor.set_y(1)


def vertical_line(stdscr, cursor: Cursor, side: str) -> None:
    '''
    vertical boundry line
    '''
    if side == 'L':
        stdscr.addstr(cursor.get_y(), cursor.get_x(), '|',
                      curses.color_pair(1))
        cursor.set_x(1)
    elif side == 'R':
        stdscr.addstr(cursor.get_y(), cursor.get_x(), '|',
                      curses.color_pair(1))
        cursor.set_y(1)
    else:
        raise ValueError('invalid value for argument \'side\'')


def print_input_line(stdscr, cursor: Cursor) -> str:
    '''
    paint the input line for the user
    '''
    cursor.set_x(-cursor.get_x())
    cursor.set_y(-cursor.get_y())

    # ask for knight's starting position
    stdscr.addstr(cursor.get_y(), cursor.get_x(),
                  'knight\'s position (row, col):')
    cursor.set_x(29)

    # wait for user's input
    stdscr.addstr(cursor.get_y(), cursor.get_x(), ' ')
    input: str = ''

    curses.echo()
    while True:
        i = stdscr.getkey()

        # enter key pressed
        if ord(i) == 10:
            break

        input += i
    curses.noecho()

    return input


def get_progress(board) -> str:
    '''
    returns the progress of the algorithm
    '''
    visited_cell_count = 0
    total_cell_count = 64

    for row in range(8):
        visited_cell_count += board[row].count(1)

    progress = (visited_cell_count / total_cell_count) * 100

    return f'{progress}%'


def place_knight(input: str, board: List[List[int]]) -> None:
    '''
    places the knight on the chess board
    '''
    row, col = list(map(int, input.split(',')))
    board[row][col] = 2


def update_board(stdscr, cursor: Cursor, board: List[List[int]]) -> None:
    '''
    paint the updated board on the window
    '''
    cursor.reset_x()
    cursor.reset_y()
    print_board(stdscr, cursor, board, progress=True, sleep_value=0.5)


def print_progress_bar(stdscr, cursor: Cursor, board: List[List[int]]) -> None:
    '''
    paint the progress bar on the window
    '''
    cursor.set_x(-cursor.get_x())
    cursor.set_y(-cursor.get_y() + 1)
    stdscr.addstr(cursor.get_y(), cursor.get_x(), 'completed: ')
    stdscr.addstr(cursor.get_y(), cursor.get_x() + 11, ' ' * cursor.max_x)
    stdscr.addstr(cursor.get_y(),
                  cursor.get_x() + 11, get_progress(board),
                  curses.color_pair(5))


def print_board(stdscr,
                cursor: Cursor,
                board: List[List[int]],
                progress: bool = False,
                sleep_value: float = 0.5) -> None:
    '''
    paint the board on the window
    '''
    horizontal_line(stdscr, cursor)
    for row in range(8):
        cursor.reset_x()

        # print empty line
        if 0 < row <= 7:
            stdscr.addstr(cursor.get_y(), cursor.get_x(), '|' + ' ' * 29 + '|',
                          curses.color_pair(1))
            cursor.set_y(1)

        # print left border
        vertical_line(stdscr, cursor, side='L')

        for col in range(8):
            # cell is visited
            if board[row][col] == 1:
                stdscr.addstr(cursor.get_y(), cursor.get_x(),
                              str(board[row][col]), curses.color_pair(2))
            # knight's cell
            elif board[row][col] == 2:
                stdscr.addstr(cursor.get_y(), cursor.get_x(),
                              str(board[row][col]), curses.color_pair(3))
            # cell is unvisited
            else:
                stdscr.addstr(cursor.get_y(), cursor.get_x(),
                              str(board[row][col]), curses.color_pair(4))
            cursor.set_x(1)

            if col != 7:
                cursor.set_x(3)

        # print right border
        vertical_line(stdscr, cursor, side='R')

    cursor.reset_x()
    horizontal_line(stdscr, cursor)

    if progress:
        # print the progress bar
        print_progress_bar(stdscr, cursor, board)

    stdscr.refresh()
    sleep(sleep_value)