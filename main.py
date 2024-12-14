import time
from Fonction import *

chemin = choisir_Test()
m_cap = matrice_capaciter(chemin)
m_cout = matrice_cout(chemin)

if m_cap is not None and m_cout is not None:
    n = len(m_cap)
    source = 0
    arrivee = n - 1
    flot = [[0] * n for _ in range(n)]

    # Mesurer le temps d'exécution pour Bellman-Ford
    print("\nExécution de l'algorithme de Bellman-Ford :")
    start_time = time.time()
    dist, parent = bellmanford(n, source, m_cap, m_cout, flot)
    end_time = time.time()
    print(f"Temps d'exécution de Bellman-Ford : {end_time - start_time:.6f} secondes")

    # Affichage des résultats
    print("\nRésultats finaux :")
    print(f"Distances : {dist}")
    print(f"Parents   : {parent}")

    # Mesurer le temps d'exécution pour le flot à coût minimum
    print("\nExécution de l'algorithme de flot à coût minimum :")
    start_time = time.time()
    flot_min_cout(n, m_cap, m_cout, source, arrivee)
    end_time = time.time()
    print(f"Temps d'exécution de Flot à Coût Minimum : {end_time - start_time:.6f} secondes")
