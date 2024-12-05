import numpy as np
import random
import tkinter as tk
from collections import deque

# Dimensions de la grille
width = 15
height = 15
cell_size = 20  # Taille de chaque cellule dans l'interface graphique

# États des cellules
EMPTY = 0
PERSON = 1
OBSTACLE = 2
EXIT = 3
exit_count = 0  # Compteur pour le nombre de personnes qui sortent

# Initialisation de la grille
grid = np.zeros((height, width), dtype=int)

# Position de la sortie (coin inférieur droit pour cet exemple)
exit_position = (height - 1, width - 8)
grid[exit_position] = EXIT

# Matrice des obstacles
obstacle_matrix = np.array([
    [0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# Placer les obstacles
for i in range(height):
    for j in range(width):
        if obstacle_matrix[i, j] == 2 and (i, j) != exit_position:
            grid[i, j] = OBSTACLE

# Ajouter des personnes aléatoirement dans la grille
for _ in range(30):  # On place 30 personnes
    while True:
        x, y = random.randint(0, height - 1), random.randint(0, width - 1)
        if grid[x, y] == EMPTY:  # On vérifie que la cellule est vide
            grid[x, y] = PERSON
            break

# BFS pour le chemin le plus court
def shortPath(grid, start, end):
    height, width = grid.shape
    queue = deque([(start, [])])  # (position actuelle, chemin)
    visited = set([start])

    while queue:
        (i, j), path = queue.popleft()

        # Si la destination est atteinte, retourner le chemin
        if (i, j) == end:
            return path + [(i, j)]
        # Explorer les déplacements possibles
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_i, new_j = i + di, j + dj
            # Vérification des limites et des cases traversables
            if 0 <= new_i < height and 0 <= new_j < width and (new_i, new_j) not in visited:
                if grid[new_i, new_j] in {EMPTY, EXIT}:
                    queue.append(((new_i, new_j), path + [(i, j)]))
                    visited.add((new_i, new_j))

    return None  # Pas de chemin trouvé

# Déplacer les personnes
def move_person(grid, end):
    global exit_count
    new_grid = np.copy(grid)
    for i in range(height):
        for j in range(width):
            if grid[i, j] == PERSON:
                path = shortPath(grid, (i, j), end)
                if path and len(path) > 1:
                    new_i, new_j = path[1]
                    if grid[new_i, new_j] == EMPTY:
                        new_grid[i, j] = EMPTY
                        new_grid[new_i, new_j] = PERSON
                    elif grid[new_i, new_j] == EXIT:
                        new_grid[i, j] = EMPTY
                        exit_count += 1

    return new_grid

# Interface graphique
def draw_grid(canvas, grid):
    for i in range(height):
        for j in range(width):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if grid[i, j] == EMPTY:
                color = "white"
            elif grid[i, j] == PERSON:
                color = "blue"
            elif grid[i, j] == OBSTACLE:
                color = "black"
            elif grid[i, j] == EXIT:
                color = "green"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

def update_simulation():
    global grid, exit_count
    canvas.delete("all")
    draw_grid(canvas, grid)
    grid = move_person(grid, exit_position)
    exit_label.config(text=f"Personnes sorties : {exit_count}")
    if np.any(grid == PERSON):  # Continue si des personnes restent
        root.after(200, update_simulation)

root = tk.Tk()
root.title("Simulation de foule")
canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
canvas.pack()
exit_label = tk.Label(root, text=f"Personnes sorties : {exit_count}")
exit_label.pack()

draw_grid(canvas, grid)
root.after(500, update_simulation)
root.mainloop()
