def choisir_Test():
    # Demande à l'utilisateur de choisir un numéro de test et retourne le chemin du fichier correspondant
    x = int(input("Entrer le numero du Test que vous voulez afficher : "))
    fichier = f"Test/Test{x}.txt"
    return fichier

def matrice_capaciter(chemin_fichier):
    try:
        with open(chemin_fichier, 'r') as file:
            lines = file.readlines()
            n = int(lines[0].strip())  # Nombre de lignes et colonnes à conserver

            # Transformation en une matrice d'entiers
            matrice_complete = [
                [int(val) for val in line.split()]
                for line in lines[1:]
            ]

            # Tronquer la matrice à n lignes et n colonnes
            matrice_capaciter = [ligne[:n] for ligne in matrice_complete[:n]]

            return matrice_capaciter

    except Exception as e:
        print(f"Erreur lors de la lecture ou du traitement du fichier {chemin_fichier} : {e}")
        return None

def matrice_cout(chemin_fichier):
    try:
        with open(chemin_fichier, 'r') as file:
            lines = file.readlines()
            n = int(lines[0].strip())  # Nombre de lignes pour la première matrice

            # Transformation en une matrice d'entiers
            matrice_complete = [
                [int(val) for val in line.split()]
                for line in lines[1:]
            ]

            if len(matrice_complete) > n:
                # Matrice à partir de la ligne n
                matrice_cout = matrice_complete[n:]
                return matrice_cout
            else:
                print("\nPas assez de lignes pour une matrice des coûts.")
                return None

    except Exception as e:
        print(f"Erreur lors de la lecture ou du traitement du fichier {chemin_fichier} : {e}")
        return None

def print_matrice(matrice):
    if matrice is None:
        print("Matrice vide ou invalide.")
        return

    # Générer les en-têtes : s, alphabet, t
    taille = len(matrice)
    alphabet = [chr(i) for i in range(65, 91)]  # Lettres A-Z

    if taille < 2:
        print("Erreur : La matrice doit avoir une taille d'au moins 2.")
        return

    if taille > len(alphabet) + 2:
        print(f"Erreur : La taille de la matrice ({taille}) excède le nombre maximum supporté (28).")
        return

    # Construire les noms de lignes et colonnes
    headers = ['s'] + alphabet[:taille - 2] + ['t']

    # Afficher les en-têtes des colonnes
    print("    " + " ".join(f"{h:>3}" for h in headers))
    for i, ligne in enumerate(matrice):
        # Afficher chaque ligne avec son nom correspondant
        print(f"{headers[i]:>3} " + " ".join(f"{x:>3}" for x in ligne))

def bellmanford(n, source, capacite, cout, flot):
  
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[source] = 0  # Distance à la source est initialisée à 0

    print("\n===== Initialisation =====")
    print("Distances initiales :", dist)
    print("Parents initiaux   :", parent)
    print("==========================\n")

    for iteration in range(n - 1):
        print(f"--- Itération {iteration + 1} ---")
        updated = False  # Indicateur pour suivre si une mise à jour a été effectuée

        for u in range(n):
            for v in range(n):
                if capacite[u][v] > 0 and dist[u] + cout[u][v] < dist[v]:
                    dist[v] = dist[u] + cout[u][v]
                    parent[v] = u
                    updated = True

        print("  Distances :", dist)
        print("  Parents   :", parent)

        if not updated:  # Si aucune mise à jour, on peut arrêter
            print("\nAucune mise à jour effectuée. L'algorithme s'arrête ici.\n")
            break

    print("\n===== Résultats finaux =====")
    print("Distances finales :", dist)
    print("Parents finaux   :", parent)
    print("============================\n")

    return dist, parent

def bfs(graphe, sommet_initial, sommet_arrivee, predecesseur):#Recherche en largeur pour un chemin de flux maximal.
    visités = [False] * len(graphe)  # Marque les sommets visités
    file = deque([sommet_initial])   # File initialisée avec le sommet source
    visités[sommet_initial] = True   # Marque le sommet source comme visité
    predecesseur[sommet_initial] = -1 # Aucun prédécesseur pour le sommet source

    while file:  # Parcourt les sommets dans la file
        sommet_courant = file.popleft()     # Défile le sommet courant
        for voisin, capacité in enumerate(graphe[sommet_courant]):  # Parcourt les voisins
            if not visités[voisin] and capacité > 0:                # Si voisin non visité et capacité > 0
                file.append(voisin)            # Ajoute le voisin à la file
                predecesseur[voisin] = sommet_courant  # Met à jour le prédécesseur
                visités[voisin] = True         # Marque le voisin comme visité
                if voisin == sommet_arrivee:   # Si on atteint le puits
                    return True                # Chemin trouvé
    return False  # Aucun chemin trouvé

def ford_fulkerson(graphe, sommet_initial, sommet_arrivee):  #Algorithme de Ford-Fulkerson pour calculer le flot maximal.
    graphe_complementaire = [ligne[:] for ligne in graphe]  # Copie le graphe pour capacités restantes
    predecesseur = [-1] * len(graphe)                       # Tableau pour stocker les prédécesseurs
    flot_max = 0                                            # Initialisation du flot maximal

    # Tant qu'on trouve un chemin de flux maximal dans le graphe complémentaire
    while bfs(graphe_complementaire, sommet_initial, sommet_arrivee, predecesseur):
        flot_chemin = float('Inf')  # Flot minimal sur le chemin trouvé
        sommet_actuel = sommet_arrivee

        # Détermine le flot minimal du chemin
        while sommet_actuel != sommet_initial:
            parent = predecesseur[sommet_actuel]  # Récupère le prédécesseur
            flot_chemin = min(flot_chemin, graphe_complementaire[parent][sommet_actuel])  # Met à jour le flot minimal
            sommet_actuel = parent  # Remonte au sommet précédent

        # Met à jour les capacités restantes dans le graphe complémentaire
        sommet_actuel = sommet_arrivee
        while sommet_actuel != sommet_initial:
            parent = predecesseur[sommet_actuel]  # Récupère le prédécesseur
            graphe_complementaire[parent][sommet_actuel] -= flot_chemin  # Réduit la capacité dans le sens du chemin
            graphe_complementaire[sommet_actuel][parent] += flot_chemin  # Augmente la capacité dans le sens inverse
            sommet_actuel = parent  # Remonte au sommet précédent

        flot_max += flot_chemin  # Ajoute le flot trouvé au flot maximal total

    return flot_max  # Retourne le flot maximal

def creation_matrice(nb_sommet):
    C = [[0 for _ in range(nb_sommet)] for _ in range(nb_sommet)]    # Crée une matrice nb_sommet x nb_sommet remplie de 0
    nbr_couples = (nb_sommet * nb_sommet) // 2                        # Détermine le nombre d’arcs (la moitié des paires possibles)

    for _ in range(nbr_couples):
        while True:
            a, b = random.randint(0, nb_sommet - 1), random.randint(0, nb_sommet - 1)  # Choix aléatoire de deux sommets
            if a != b and C[a][b] == 0:                                               # Vérifie pas de boucle ni d'arc existant
                C[a][b] = random.randint(1, 100)                                      # Assigne une capacité entre 1 et 100
                break
    return C
def etudier_complexite():
    tailles = [10, 20, 40, 60, 100]  # Tailles des graphes à tester
    repetitions = 100                # 100 répétitions pour chaque taille
    resultats = []                   # Liste pour stocker (taille, temps moyen)

    for nb_sommet in tailles:  # Pour chaque taille de graphe
        temps = []             # Liste pour stocker les temps d'exécution
        for _ in range(repetitions):  # 100 répétitions
            graphe = creation_matrice(nb_sommet)   # Crée un graphe aléatoire
            start_time = time.time()               # Début du chronométrage
            ford_fulkerson(graphe, 0, nb_sommet - 1)  # Calcule le flot maximal
            temps.append(time.time() - start_time)     # Enregistre le temps d'exécution
        moyenne_temps = sum(temps) / repetitions   # Calcule le temps moyen
        resultats.append((nb_sommet, moyenne_temps))   # Stocke (taille, temps moyen)
        print(f"Taille: {nb_sommet}, Temps moyen: {moyenne_temps:.5f}s")  # Affiche les résultats

    # Affichage des résultats sous forme de graphique
    x, y = zip(*resultats)        # Sépare les tailles et les temps moyens
    plt.plot(x, y, marker='o')    # Trace le graphique
    plt.xlabel("Taille du graphe (nb_sommet)")  # Étiquette axe X
    plt.ylabel("Temps d'exécution moyen (s)")   # Étiquette axe Y
    plt.title("Complexité de Ford-Fulkerson")   # Titre du graphique
    plt.grid(True)               # Ajoute une grille
    plt.show()                   # Affiche le graphique