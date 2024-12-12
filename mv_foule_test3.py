import numpy as np
import random
import tkinter as tk
from collections import deque
import heapq

# Dimensions de la grille
width = 15
height = 15
cell_size = 30

# États des cellules
EMPTY = 0
PERSON = 1
OBSTACLE = 2
EXIT = 3
exit_count = 0


# Initialisation de la grille
grid = np.zeros((height, width), dtype=int)

# Position de la sortie (coin inférieur droit pour cet exemple)
exit_position = (height - 2, width - 1)
grid[exit_position] = EXIT

# Matrice des obstacles
obstacle_matrix = np.array([
    [0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
    [0, 2, 2, 0, 2, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
    [0, 2, 2, 0, 2, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
    [0, 2, 2, 0, 2, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
    [0, 2, 2, 0, 2, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
    [0, 2, 2, 0, 2, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
])

# Placer les obstacles
for i in range(height):
    for j in range(width):
        if obstacle_matrix[i, j] == 2 and (i, j) != exit_position:
            grid[i, j] = OBSTACLE
        elif obstacle_matrix[i, j] == 1 and (i, j) != exit_position:
            grid[i, j] = PERSON


# Compter les personnes

def count_person(grid):
    count = 0
    for i in range(height):
        for j in range(width):
            if grid[i, j] == PERSON:
                count += 1
    return count

# Distance Manhattan
def distance_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# Le plus court chemin avec A*
def shortPath(grid, start, end):
    height, width = grid.shape
    queue = [(0, start, [])]
    visited = set([start])

    while queue:
        cost, (i, j), path = heapq.heappop(queue)
        if (i, j) == end:
            return path + [(i, j)]

        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < height and 0 <= new_j < width and grid[new_i, new_j] != OBSTACLE and (new_i, new_j) not in visited:
                new_path = path + [(i, j)]
                new_cost = cost + 1 + distance_manhattan(new_i, new_j, end[0], end[1])
                heapq.heappush(queue, (new_cost, (new_i, new_j), new_path))
                visited.add((new_i, new_j))
    return None



# Déplacer les personnes dans la grille
def move_person(grid):
    global exit_count
    new_grid = np.copy(grid)
    for i in range(height):
        for j in range(width):
            if grid[i, j] == PERSON:
                path = shortPath(grid, (i, j), exit_position)
                if len(path) > 1:
                    new_i, new_j = path[1]
                    if new_grid[new_i, new_j] == EMPTY:
                        new_grid[i, j]= EMPTY
                        new_grid[new_i, new_j]= PERSON
                    elif new_grid[new_i, new_j] == EXIT:
                        new_grid[i, j] = EMPTY
                        exit_count += 1
    return new_grid

# Interface graphique
def draw_grid(canvas, grid):
    global person_counter
    person_counter = 1
    for i in range(height):
        for j in range(width):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if grid[i, j] == EMPTY:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="")
            elif grid[i, j] == OBSTACLE:
                canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="")
            elif grid[i, j] == EXIT:
                canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="")
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="")


            if grid[i, j] == PERSON:
                # Dessiner un ovale centré dans la case
                oval_x1 = x1 + 5  # Un petit décalage pour l'ovale
                oval_y1 = y1 + 5
                oval_x2 = x2 - 5
                oval_y2 = y2 - 5
                canvas.create_oval(oval_x1, oval_y1, oval_x2, oval_y2, fill="blue", outline="")

                # Dessiner le numéro de la personne
                canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(person_counter), fill="white")
                person_counter += 1

def update_simulation():
    global grid, exit_count
    canvas.delete("all")
    draw_grid(canvas, grid)
    grid = move_person(grid)  # Augmenter la probabilité de collision
    exit_label.config(text=f"Personnes sorties : {exit_count}")
    root.after(240, update_simulation)  # Réduire l'intervalle de temps

root = tk.Tk()
root.title("Simulation de foule")
canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
canvas.pack()
exit_label = tk.Label(root, text=f"Personnes sorties : {exit_count}")
exit_label.pack()

count_label = tk.Label(root, text=f"Nombre de personnes : {count_person(grid)}")
count_label.pack()

draw_grid(canvas, grid)
root.after(500, update_simulation)
root.mainloop()