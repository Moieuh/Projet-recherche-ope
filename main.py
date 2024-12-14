from Fonction import *
chemin = choisir_Test()
m_cap = matrice_capaciter(chemin)
m_cout = matrice_cout(chemin)
print("\nMatrice de capacité:")
print_matrice(m_cap)
print("\nMatrice de cout:")
print_matrice(m_cout)

if m_cap is not None and m_cout is not None:
    n = len(m_cap)
    source = 0  # Exemple de source, peut être modifié selon les besoins
    arrivee =n-1 # Exemple d'arrivé, peut être modifié selon les besoins
    flot = [[0] * n for _ in range(n)]  # Matrice de flot initiale (tout à 0)

    print("\nExécution de l'algorithme de Bellman-Ford :")
    dist, parent = bellmanford(n, source, m_cap, m_cout, flot)
    print("\n Exécution de l'algorithme de Ford : ")
    flot = ford_fulkerson(m_cap, source, arrivee)
    print("Le flot maximum de la source", source, "au puits", arrivee, "est :", flot)
    print("\nRésultats finaux :")
    print(f"Distances : {dist}")
    print(f"Parents   : {parent}")

    
    flot_min_cout(n,m_cap,m_cout,source,arrivee)