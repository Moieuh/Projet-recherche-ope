from Fonction import *
chemin = choisir_Test()
matrice_cap = matrice_capaciter(chemin)
matrice_cout = matrice_cout(chemin)
print("\nMatrice de capaciter:")
print_matrice(matrice_cap)
print("\nMatrice de cout:")
print_matrice(matrice_cout)

if matrice_cap is not None and matrice_cout is not None:
    n = len(matrice_cap)
    source = 0  # Exemple de source, peut être modifié selon les besoins
    flot = [[0] * n for _ in range(n)]  # Matrice de flot initiale (tout à 0)

    print("\nExécution de l'algorithme de Bellman-Ford :")
    dist, parent = bellmanford(n, source, matrice_cap, matrice_cout, flot)

    print("\nRésultats finaux :")
    print(f"Distances : {dist}")
    print(f"Parents   : {parent}")