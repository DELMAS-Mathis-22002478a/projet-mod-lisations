import numpy as np
import tkinter as tk
import time

# Dimensions de la grille
width = 15
height = 15
cell_size = 35

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

obstacle_matrix = np.array([
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2]
])

def count_person(grid):
    count = 0
    for i in range(height):
        for j in range(width):
            if grid[i, j] == PERSON:
                count += 1
    return count

# Placer les obstacles
for i in range(height):
    for j in range(width):
        if obstacle_matrix[i, j] == 2:
            if (i, j) != exit_position:
                grid[i, j] = OBSTACLE
        elif obstacle_matrix[i, j] == 1:
            if (i, j) != exit_position:
                grid[i, j] = PERSON

# Distance Manhattan
def distance_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

people_exited = 0

def move_person(grid, end):
    # Nombre de personnes sorties
    global people_exited
    new_grid = np.copy(grid)
    moves = []
    paths = {}

    for i in range(height):
        for j in range(width):
            if grid[i, j] == PERSON:
                distances = {
                    'up': distance_manhattan(i - 1, j, end[0], end[1]),
                    'down': distance_manhattan(i + 1, j, end[0], end[1]),
                    'left': distance_manhattan(i, j - 1, end[0], end[1]),
                    'right': distance_manhattan(i, j + 1, end[0], end[1])
                }

                sorted_distances = sorted(distances, key=lambda x: distances[x])
                path_found = False

                for direction in sorted_distances:
                    new_i, new_j = i, j
                    if direction == 'up':
                        new_i -= 1
                    elif direction == 'down':
                        new_i += 1
                    elif direction == 'left':
                        new_j -= 1
                    elif direction == 'right':
                        new_j += 1

                    if 0 <= new_i < height and 0 <= new_j < width:
                        if grid[new_i, new_j] == EMPTY:
                            moves.append((i, j, new_i, new_j))
                            paths[(i, j)] = paths.get((i, j), []) + [(new_i, new_j)]
                            path_found = True
                            break
                        elif grid[new_i, new_j] == EXIT:
                            moves.append((i, j, new_i, new_j))
                            paths[(i, j)] = paths.get((i, j), []) + [(new_i, new_j)]
                            path_found = True
                            break

                if not path_found:
                    paths[(i, j)] = paths.get((i, j), []) + [(i, j)]  # Wait

    # Appliquer les mouvements
    for i, j, new_i, new_j in moves:
        if new_grid[new_i, new_j] == EMPTY:
            new_grid[i, j] = EMPTY
            new_grid[new_i, new_j] = PERSON
        elif new_grid[new_i, new_j] == EXIT:
            new_grid[i, j] = EMPTY
            people_exited += 1

    return new_grid, paths

def draw_grid(canvas, grid):
    global person_counter
    person_counter = 1
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
            # Si la case contient une personne, dessiner le numéro
            if grid[i, j] == PERSON:
                canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(person_counter), fill="white")
                person_counter += 1

# Mettre à jour la simulation
def update_simulation():
    global grid
    grid, paths = move_person(grid, exit_position)
    canvas.delete("all")
    draw_grid(canvas, grid)
    people_exited_label.config(text=f"Personnes sorties: {people_exited}")
    root.after(500, update_simulation)

# Fenêtre tkinter
root = tk.Tk()
root.title("Mouvement de Foule")

canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
canvas.pack()

people_exited_label = tk.Label(root, text=f"Personnes sorties: {people_exited}")
people_exited_label.pack()

people_count_label = tk.Label(root, text=f"Nombre de personnes: {count_person(grid)}")
people_count_label.pack()

draw_grid(canvas, grid)

root.after(200, update_simulation)
root.mainloop()