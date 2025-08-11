#!/usr/bin/env python3
"""Simple snack game using curses.

Use arrow keys to move around and collect snacks (*).
Press 'q' to exit the game.
"""

import curses
from random import randint


def main(stdscr: 'curses._CursesWindow') -> None:
    """Run the snack game."""
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(True)
    win.timeout(100)

    # Initial snake position (three blocks)
    x = sw // 4
    y = sh // 2
    snake = [
        [y, x],
        [y, x - 1],
        [y, x - 2],
    ]

    snack = [sh // 2, sw // 2]
    win.addch(snack[0], snack[1], "*")

    direction = curses.KEY_RIGHT

    while True:
        next_key = win.getch()
        if next_key == ord('q'):
            break
        direction = direction if next_key == -1 else next_key

        if direction == curses.KEY_DOWN:
            new_head = [snake[0][0] + 1, snake[0][1]]
        elif direction == curses.KEY_UP:
            new_head = [snake[0][0] - 1, snake[0][1]]
        elif direction == curses.KEY_LEFT:
            new_head = [snake[0][0], snake[0][1] - 1]
        elif direction == curses.KEY_RIGHT:
            new_head = [snake[0][0], snake[0][1] + 1]
        else:
            continue

        snake.insert(0, new_head)

        # Check for collision with borders or self
        if (
            snake[0][0] in (0, sh) or
            snake[0][1] in (0, sw) or
            snake[0] in snake[1:]
        ):
            msg = "Game Over!"
            win.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            win.refresh()
            win.getch()
            break

        # Check if snack eaten
        if snake[0] == snack:
            snack = None
            while snack is None:
                new_snack = [randint(1, sh - 1), randint(1, sw - 1)]
                snack = new_snack if new_snack not in snake else None
            win.addch(snack[0], snack[1], '*')
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')

        win.addch(snake[0][0], snake[0][1], '#')


if __name__ == "__main__":
    curses.wrapper(main)
