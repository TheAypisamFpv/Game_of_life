import random
import time
import numpy as np
import cv2 as cv


def create_grid(rows, columns):
    coef = 3
    grid = []
    for row in range(rows):
        grid.append([])
        for column in range(columns):
            grid[row].append(1 if random.randint(0, coef) == coef else 0)
    return grid


def get_neighbours(grid, row, column):
    neighbours = 0
    for r in range(row - 1, row + 2):
        for c in range(column - 1, column + 2):
            if r == row and c == column:
                continue
            if r >= len(grid):
                r = 0
            if c >= len(grid[r]):
                c = 0
            if grid[r][c] == 1:
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
            if random.randint(0, 50) == 50:
                grid[row][column] = 1
    return grid


def grid_to_screen(grid):
    '''Convert a grid into a cv2 screen'''
    screen_size_coefficient = 25
    screen = np.zeros((len(grid)*screen_size_coefficient,
                      len(grid[0])*screen_size_coefficient, 1), dtype=np.uint8)
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column] == 1:
                screen[row*screen_size_coefficient:(row+1)*screen_size_coefficient,
                       column*screen_size_coefficient:(column+1)*screen_size_coefficient] = 255
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
    grid = create_grid(50, 50)
    main(grid)
