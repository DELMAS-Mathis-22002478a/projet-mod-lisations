import numpy as np
import random


width = 20
height = 20


EMPTY = 0
PERSON = 1
OBSTACLE = 2
EXIT = 3

grid = np.zeros((height, width), dtype=int)

exit_position = (height - 1, width - 1)
grid[exit_position] = EXIT



for _ in range(20):  # On place 20 obstacles
    x, y = random.randint(0, height - 1), random.randint(0, width - 1)
    grid[x, y] = OBSTACLE


for _ in range(30):  # On place 30 personnes
    while True:
        x, y = random.randint(0, height - 1), random.randint(0, width - 1)
        if grid[x, y] == EMPTY:  # On vérifie que la cellule est vide
            grid[x, y] = PERSON
            break



def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)



def move_people(grid, exit_position):
    new_grid = np.copy(grid)

    for i in range(height):
        for j in range(width):
            if grid[i, j] == PERSON:
                # Cherche la direction qui minimise la distance vers la sortie
                best_move = (i, j)
                best_distance = manhattan_distance(i, j, exit_position[0], exit_position[1])

                # Explorer les cellules voisines (haut, bas, gauche, droite)
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < height and 0 <= nj < width and grid[ni, nj] == EMPTY:
                        new_distance = manhattan_distance(ni, nj, exit_position[0], exit_position[1])
                        if new_distance < best_distance:
                            best_move = (ni, nj)
                            best_distance = new_distance


                if best_move != (i, j):
                    new_grid[i, j] = EMPTY
                    new_grid[best_move[0], best_move[1]] = PERSON

    return new_grid



def print_grid(grid):
    for row in grid:
        print(' '.join(str(cell) for cell in row))



print("Grille initiale :")
print_grid(grid)


for step in range(10):
    print(f"\nÉtape {step + 1} :")
    grid = move_people(grid, exit_position)
    print_grid(grid)
