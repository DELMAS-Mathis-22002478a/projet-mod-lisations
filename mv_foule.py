import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

def distance_manhattan(x1,x2,y1,y2):
    result = abs(x2-x1) + abs(y2-y1)
    return result

def move_people(grid, exit_position):
    new_grid = np.copy(grid)
    for i in range(height):
        for j in range(width):
            if grid[i, j] == PERSON:
                exit_position = (i, j)
                move_distance = distance_manhattan(i, j, exit_position[0], exit_position[1])
                for wi, hj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + wi, j + hj
                    if 0 <= ni < height and 0 <= nj < width and grid[ni, nj] == EMPTY:
                        new_distance = distance_manhattan(ni,nj,exit_position[0], exit_position[1])
                        if new_distance < move_distance:
                            exit_position = (ni, nj)
                            move_distance = new_distance
            if exit_position != (i,j):
                new_grid[i, j] = EMPTY
                new_grid[exit_position[0], exit_position[1]] = PERSON

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
    
# Fonction pour animer la simulation
def animate_simulation():
    fig, ax = plt.subplots()
    cmap = plt.cm.get_cmap('viridis', 4)
    img = ax.imshow(grid, cmap=cmap, vmin=0, vmax=3)
    ax.set_xticks([])
    ax.set_yticks([])

    def update(frame):
        global grid
        grid = move_people(grid, exit_position)
        img.set_array(grid)
        return [img]

    ani = animation.FuncAnimation(fig, update, frames=10, interval=500, blit=True)
    plt.colorbar(img, ticks=[0, 1, 2, 3], label='Cell States')
    plt.show()

# Afficher la simulation animée
animate_simulation()
