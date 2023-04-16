import random
import time

import cv2 as cv
import numpy as np

"""Game of life's settings"""
grid_size = 16, 32
rand_grid_coef = 3
screen_size_coefficient = 20
"""-----------------------"""


def create_grid(rows, columns):
    grid = []
    for row in range(rows):
        grid.append([])
        for column in range(columns):
            grid[row].append(1 if random.randint(
                0, rand_grid_coef) == rand_grid_coef else 0)
    return grid


def get_neighbours(grid, rows, columns):
    neighbours = 0
    for row in range(rows - 1, rows + 2):
        for column in range(columns - 1, columns + 2):
            if row == rows and column == columns:
                continue
            
            if row >= len(grid):
                row = 0

            if column >= len(grid[row]):
                column = 0

            if grid[row][column] == 1:
                neighbours += 1
    return neighbours


def update_cells(grid):
    new_grid = []
    for row in range(len(grid)):
        new_grid.append([])
        for column in range(len(grid[row])):
            neighbours = get_neighbours(grid, row, column)
            if grid[row][column] == 1 and 2 <= neighbours <= 3:
                new_grid[row].append(1)
            elif grid[row][column] == 0 and neighbours == 3:
                new_grid[row].append(1)
            else:
                new_grid[row].append(0)

    return new_grid


def randomness(grid):
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if random.randint(0, rand_grid_coef*5) == rand_grid_coef*5:
                grid[row][column] = 1

    return grid


def grid_to_screen(grid):
    '''Convert a grid into a cv2 screen'''
    screen = np.zeros((len(grid)*screen_size_coefficient,
                      len(grid[0])*screen_size_coefficient, 1), dtype=np.uint8)

    for row in range(len(grid)):
        for column in range(len(grid[row])):
            screen[row*screen_size_coefficient:(row+1)*screen_size_coefficient,
                   column*screen_size_coefficient:(column+1)*screen_size_coefficient] = 25

            if grid[row][column] == 1:
                screen[(row*screen_size_coefficient)+1:(row+1)*screen_size_coefficient,
                       (column*screen_size_coefficient)+1:(column+1)*screen_size_coefficient] = 255
            else:
                screen[(row*screen_size_coefficient)+1:(row+1)*screen_size_coefficient,
                       (column*screen_size_coefficient)+1:(column+1)*screen_size_coefficient] = 0

    return screen


def displplay_screen(screen):
    cv.imshow('screen', screen)
    cv.waitKey(1)


def main(grid):
    game_tick = 0
    while True:
        screen = grid_to_screen(grid)
        displplay_screen(screen)

        print(f'Game tick: {game_tick}')

        grid = update_cells(grid)
        if game_tick % 1000 == 0:
            grid = randomness(grid)
            print('Randomness!')
        time.sleep(0.1)

        game_tick += 1


if __name__ == '__main__':
    grid = create_grid(grid_size[0], grid_size[1])
    main(grid)
