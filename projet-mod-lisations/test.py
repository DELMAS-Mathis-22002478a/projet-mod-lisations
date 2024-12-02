import numpy as np
import matplotlib.pyplot as plt

# Paramètres du modèle
N = 100  # Nombre de personnes
L = 100  # Longueur du corridor
v_max = 1  # Vitesse maximale
rho = 0.5  # Densité de population

# Initialisation des positions et des vitesses
positions = np.random.uniform(0, L, N)
velocities = np.random.uniform(-v_max, v_max, N)

# Boucle de simulation
for t in range(100):
    # Mise à jour des positions et des vitesses
    for i in range(N):
        # Collision avec les murs
        if positions[i] < 0 or positions[i] > L:
            velocities[i] = -velocities[i]
        # Interaction avec les autres personnes
        for j in range(N):
            if i != j:
                distance = np.linalg.norm(positions[i] - positions[j])
                if distance < 0.5:
                    velocities[i] += (velocities[j] - velocities[i]) / distance
    # Mise à jour des positions
    positions += velocities

# Visualisation des résultats
plt.plot(positions)
plt.xlabel('Position')
plt.ylabel('Temps')
plt.show()