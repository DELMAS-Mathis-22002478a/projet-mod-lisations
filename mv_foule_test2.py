import numpy as np
import random
import tkinter as tk
import heapq

# Dimensions de la grille
width = 15
height = 15
cell_size = 20  # Taille de chaque cellule dans l'interface graphique

# États des cellules
EMPTY = 0
PERSON = 1
OBSTACLE = 2
EXIT = 3
nb = 0
exit_count = 0  # Compteur pour le nombre de personnes qui sortent

# Initialisation de la grille
grid = np.zeros((height, width), dtype=int)

# Position de la sortie (on choisit le coin inférieur droit pour cet exemple)
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
        if obstacle_matrix[i, j] == 2:  # Changez cette ligne
            # On évite de placer un obstacle sur la sortie
            if (i, j) != exit_position:
                grid[i, j] = OBSTACLE

# Ajouter des personnes aléatoirement dans la grille
for i in range(30):  # On place 30 personnes
    while True:
        x, y = random.randint(0, 10 - 1), random.randint(0, 10 - 1)
        if grid[x, y] == EMPTY:  # On vérifie que la cellule est vide
            grid[x, y] = PERSON
            nb = i
            break

def distance_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(grid, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: distance_manhattan(start[0], start[1], end[0], end[1])}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            if 0 <= neighbor[0] < height and 0 <= neighbor[1] < width and grid[neighbor[0], neighbor[1]] != OBSTACLE:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + distance_manhattan(neighbor[0], neighbor[1], end[0], end[1])
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def move_person(grid, end):
    global nb, exit_count
    new_grid = np.copy(grid)
    moves = []

    for i in range(height):
        for j in range(width):
            if grid[i, j] == PERSON:
                path = a_star(grid, (i, j), end)
                if path:
                    new_i, new_j = path[0]
                    if grid[new_i, new_j] == EMPTY:
                        moves.append((i, j, new_i, new_j))
                    elif grid[new_i, new_j] == EXIT:
                        moves.append((i, j, new_i, new_j))

    for i, j, new_i, new_j in moves:
        if new_grid[new_i, new_j] == EMPTY:
            new_grid[i, j] = EMPTY
            new_grid[new_i, new_j] = PERSON
        elif new_grid[new_i, new_j] == EXIT:
            new_grid[i, j] = EMPTY
            exit_count += 1

    return new_grid, False

# Fonction pour dessiner la grille dans l'interface tkinter
def draw_grid(canvas, grid):
    for i in range(height):
        for j in range(width):
            x1 = j * cell_size
            y1 = i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            if grid[i, j] == EMPTY:
                color = "white"
            elif grid[i, j] == PERSON:
                color = "blue"
            elif grid[i, j] == OBSTACLE:
                color = "black"
            elif grid[i, j] == EXIT:
                color = "green"

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

# Fonction pour mettre à jour la simulation
def update_simulation():
    global grid, exit_count

    canvas.delete("all")
    draw_grid(canvas, grid)
    grid, person_exited = move_person(grid, exit_position)
    exit_label.config(text=f"Personne sortie: {exit_count}")
    root.after(200, update_simulation)

# Création de la fenêtre tkinter
root = tk.Tk()
root.title("Mouvement de foule")

canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
canvas.pack()

exit_label = tk.Label(root, text=f"Exit Count: {exit_count}")
exit_label.pack()

draw_grid(canvas, grid)

# Démarrer la simulation
root.after(500, update_simulation)

# Lancer la boucle principale de tkinter
root.mainloop()