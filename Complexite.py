import random
import time
import numpy as np
import matplotlib.pyplot as plt

def creation_matrice(nb_sommet):
    """
    Génère une matrice de graphes aléatoires avec des capacités aléatoires entre les sommets.
    """
    C = [[0 for _ in range(nb_sommet)] for _ in range(nb_sommet)]
    nbr_couples = (nb_sommet * nb_sommet) // 2

    for _ in range(nbr_couples):
        while True:
            a, b = random.randint(0, nb_sommet - 1), random.randint(0, nb_sommet - 1)
            if a != b and C[a][b] == 0:
                C[a][b] = random.randint(1, 100)
                break
    return C

def ford_fulkerson(graphe, source, puit):
    """
    Simulation de l'algorithme de Ford-Fulkerson (remplacez par une implémentation réelle).
    """
    time.sleep(0.01)  # Simule un délai d'exécution
    return random.randint(1, 100)

def pousse_reetiquetage(graphe, source, puit):
    """
    Simulation de l'algorithme de poussée-réétiquetage.
    """
    time.sleep(0.015)  # Simule un délai d'exécution légèrement plus long
    return random.randint(1, 100)

def flot_a_cout_min(graphe, source, puit):
    """
    Simulation de l'algorithme du flot à coût minimal.
    """
    time.sleep(0.02)  # Simule un délai d'exécution encore plus long
    return random.randint(1, 100)

def etudier_complexite():
    """
    Étudie les temps d'exécution de plusieurs algorithmes pour différentes tailles de graphes.
    """
    tailles = [10, 20, 40, 100, 400, 1000, 4000, 10000]  # Tailles des graphes à tester
    repetitions = 100  # 100 répétitions pour chaque taille

    # Stockage des temps d'exécution
    execution_times = {
        "Ford-Fulkerson": [],
        "Poussée-Réétiquetage": [],
        "Flot à coût min": []
    }

    for nb_sommet in tailles:
        print(f"Calcul pour taille n = {nb_sommet}...")
        times_ff, times_pr, times_min = [], [], []

        for _ in range(repetitions):
            graphe = creation_matrice(nb_sommet)
            source, puit = 0, nb_sommet - 1

            # Ford-Fulkerson
            start_time = time.perf_counter()
            ford_fulkerson(graphe, source, puit)
            times_ff.append(time.perf_counter() - start_time)

            # Poussée-Réétiquetage
            start_time = time.perf_counter()
            pousse_reetiquetage(graphe, source, puit)
            times_pr.append(time.perf_counter() - start_time)

            # Flot à coût min
            start_time = time.perf_counter()
            flot_a_cout_min(graphe, source, puit)
            times_min.append(time.perf_counter() - start_time)

        execution_times["Ford-Fulkerson"].append(times_ff)
        execution_times["Poussée-Réétiquetage"].append(times_pr)
        execution_times["Flot à coût min"].append(times_min)

    return tailles, execution_times

def plot_execution_times(n_values, execution_times, algorithm_names):
    """
    Trace les nuages de points des temps d'exécution pour chaque algorithme.
    """
    for algo in algorithm_names:
        plt.figure()
        for n, times in zip(n_values, execution_times[algo]):
            plt.scatter([n] * len(times), times, alpha=0.5)
        plt.xlabel("Taille du graphe (n)")
        plt.ylabel("Temps d'exécution (s)")
        plt.title(f"Nuage de points pour {algo}")
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
        plt.show()

def plot_worst_case(n_values, execution_times, algorithm_names):
    """
    Trace les complexités dans le pire des cas pour chaque algorithme.
    """
    for algo in algorithm_names:
        worst_case_times = [np.max(times) for times in execution_times[algo]]
        plt.plot(n_values, worst_case_times, marker='o', label=algo)
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps d'exécution maximal (s)")
    plt.title("Complexité dans le pire des cas")
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.show()

# Étude des complexités
n_values, execution_times = etudier_complexite()

# Trace les nuages de points
plot_execution_times(n_values, execution_times, ["Ford-Fulkerson", "Poussée-Réétiquetage", "Flot à coût min"])

# Trace les complexités dans le pire des cas
plot_worst_case(n_values, execution_times, ["Ford-Fulkerson", "Poussée-Réétiquetage", "Flot à coût min"])
