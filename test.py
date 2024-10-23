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

# Initialisation de la grille
grid = np.zeros((height, width), dtype=int)

# Position de la sortie (on choisit le coin inférieur droit pour cet exemple)
exit_position = (height - 1, width - 8)
grid[exit_position] = EXIT

# Matrice des obstacles
obstacle_matrix = np.array([
    [0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0]
])

# Placer les obstacles
for i in range(height):
    for j in range(width):
        if obstacle_matrix[i, j] == 2:
            # On évite de placer un obstacle sur la sortie
            if (i, j) != exit_position:
                grid[i, j] = OBSTACLE

# Ajouter des personnes aléatoirement dans la grille
for _ in range(30):  # On place 30 personnes
    while True:
        x, y = random.randint(0, height - 1), random.randint(0, width - 1)
        if grid[x, y] == EMPTY:  # On vérifie que la cellule est vide
            grid[x, y] = PERSON
            break

# Fonction pour calculer la distance de Manhattan
def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# Fonction pour trouver le chemin le plus court avec A*
def a_star_search(grid, start, goal):
    def heuristic(a, b):
        return manhattan_distance(a[0], a[1], b[0], b[1])

    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1
            if 0 <= neighbor[0] < grid.shape[0]:
                if 0 <= neighbor[1] < grid.shape[1]:
                    if grid[neighbor[0]][neighbor[1]] == OBSTACLE:
                        tentative_g_score += 10  # Penalize obstacles
                    if neighbor in close_set:
                        continue
                    if tentative_g_score < gscore.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_g_score
                        fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False

# Fonction pour déplacer les personnes
def move_people(grid, exit_position):
    new_grid = np.copy(grid)  # Crée une nouvelle grille pour enregistrer les déplacements
    person_exited = False  # Flag to track if a person has exited

    for i in range(height):
        for j in range(width):
            if grid[i, j] == PERSON:
                path = a_star_search(grid, (i, j), exit_position)
                if path:
                    next_move = path[-1]
                    new_grid[i, j] = EMPTY
                    if next_move == exit_position:
                        if not person_exited:  # Allow only one person to exit
                            person_exited = True
                    else:
                        new_grid[next_move[0], next_move[1]] = PERSON

    return new_grid

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
    global grid
    grid = move_people(grid, exit_position)
    canvas.delete("all")  # Efface le contenu actuel du canvas
    draw_grid(canvas, grid)
    root.after(500, update_simulation)  # Appelle cette fonction après 500 ms pour créer une animation

# Création de la fenêtre tkinter
root = tk.Tk()
root.title("Mouvement de foule")

canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
canvas.pack()

# Dessiner la grille initiale
draw_grid(canvas, grid)

# Démarrer la simulation
root.after(500, update_simulation)  # Lancer la première mise à jour après 500 ms

# Lancer la boucle principale de tkinter
root.mainloop()