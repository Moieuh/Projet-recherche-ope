from collections import deque

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
                if capacite[u][v]-flot[u][v] > 0 and dist[u] + cout[u][v] < dist[v]:
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



from collections import deque

def bfs(m_cap, sommet_initial, sommet_arrivee, predecesseur):  
    visités = [False] * len(m_cap)  # Marque les sommets visités
    file = deque([sommet_initial])   # File initialisée avec le sommet source
    visités[sommet_initial] = True   # Marque le sommet source comme visité
    predecesseur[sommet_initial] = -1 # Aucun prédécesseur pour le sommet source

    print("\n=== BFS ===")
    while file:  # Parcourt les sommets dans la file
        sommet_courant = file.popleft()     # Défile le sommet courant
        print(f"Sommet courant : {sommet_courant}")
        for voisin, capacité in enumerate(m_cap[sommet_courant]):  # Parcourt les voisins
            if not visités[voisin] and capacité > 0:  # Si voisin non visité et capacité > 0
                file.append(voisin)  # Ajoute le voisin à la file
                predecesseur[voisin] = sommet_courant  # Met à jour le prédécesseur
                visités[voisin] = True  # Marque le voisin comme visité
                print(f"  Voisin trouvé : {voisin}, Capacité restante : {capacité}")
                if voisin == sommet_arrivee:  # Si on atteint le puits
                    print("  Chemin trouvé jusqu'au puits.")
                    return True  # Chemin trouvé
    return False  # Aucun chemin trouvé

def ford_fulkerson(m_cap, sommet_initial, sommet_arrivee):  
    graphe_complementaire = [ligne[:] for ligne in m_cap]  # Copie le graphe pour capacités restantes
    predecesseur = [-1] * len(m_cap)                       # Tableau pour stocker les prédécesseurs
    flot_max = 0  # Initialisation du flot maximal

    while bfs(graphe_complementaire, sommet_initial, sommet_arrivee, predecesseur):
        flot_chemin = float('Inf')  # Flot minimal sur le chemin trouvé
        sommet_actuel = sommet_arrivee

        print("\n=== Calcul du flot minimal sur le chemin trouvé ===")
        # Détermine le flot minimal du chemin
        while sommet_actuel != sommet_initial:
            parent = predecesseur[sommet_actuel]  # Récupère le prédécesseur
            flot_chemin = min(flot_chemin, graphe_complementaire[parent][sommet_actuel])  # Met à jour le flot minimal
            print(f"  Arc {parent} -> {sommet_actuel}, Capacité : {graphe_complementaire[parent][sommet_actuel]}")
            sommet_actuel = parent  # Remonte au sommet précédent

        print(f"Flot minimal trouvé : {flot_chemin}")

        # Met à jour les capacités restantes dans le graphe complémentaire
        print("\n=== Mise à jour des capacités résiduelles ===")
        sommet_actuel = sommet_arrivee
        while sommet_actuel != sommet_initial:
            parent = predecesseur[sommet_actuel]  # Récupère le prédécesseur
            print(f"  Mise à jour : Arc {parent} -> {sommet_actuel}, Réduction de {flot_chemin}")
            graphe_complementaire[parent][sommet_actuel] -= flot_chemin  # Réduit la capacité dans le sens du chemin
            graphe_complementaire[sommet_actuel][parent] += flot_chemin  # Augmente la capacité dans le sens inverse
            sommet_actuel = parent  # Remonte au sommet précédent

        flot_max += flot_chemin  # Ajoute le flot trouvé au flot maximal total
        print(f"Flot maximal actuel : {flot_max}")

    print("\n=== Résultat final ===")
    print(f"Flot maximum : {flot_max}")
    return flot_max  # Retourne le flot maximal





# Algorithme Pousser-Réétiqueter

def pousser(u, v, capacite, preflots, excedents, hauteurs):
    """Effectue une opération "pousser" entre deux sommets."""
    if (
        excedents[u] > 0
        and capacite[u][v] - preflots[u][v] > 0
        and hauteurs[u] - hauteurs[v] == 1
    ):
        quantite = min(
            excedents[u],
            capacite[u][v] - preflots[u][v],
        )
        preflots[u][v] += quantite
        preflots[v][u] -= quantite
        excedents[u] -= quantite
        excedents[v] += quantite
        return True
    return False

def reetiqueter(u, capacite, preflots, excedents, hauteurs):
    """Réétiquette un sommet en augmentant sa hauteur."""
    min_hauteur = float("inf")
    for voisin in range(len(capacite[u])):
        if capacite[u][voisin] - preflots[u][voisin] > 0:
            min_hauteur = min(min_hauteur, hauteurs[voisin])
    if excedents[u] > 0 and min_hauteur < float("inf"):
        hauteurs[u] = min_hauteur + 1
        return True
    return False

def algorithme_pousser_reetiqueter(matrice):
    """Implémente l'algorithme pousser-réétiqueter sur une matrice de capacité."""
    n = len(matrice)
    source, puits = 0, n - 1

    # Initialisations
    hauteurs = [0] * n
    hauteurs[source] = n
    excedents = [0] * n
    preflots = [[0] * n for _ in range(n)]

    # Initialisation des pré-flots depuis la source
    for voisin in range(n):
        if matrice[source][voisin] > 0:
            preflots[source][voisin] = matrice[source][voisin]
            preflots[voisin][source] = -matrice[source][voisin]
            excedents[voisin] = matrice[source][voisin]
            excedents[source] -= matrice[source][voisin]

    # Boucle principale
    while True:
        # Trouver les sommets excédentaires (hors source et puits)
        sommets_excedentaires = [
            sommet
            for sommet in range(n)
            if excedents[sommet] > 0 and sommet != source and sommet != puits
        ]

        if not sommets_excedentaires:
            break

        # Choisir le sommet excédentaire avec la plus grande hauteur
        u = max(sommets_excedentaires, key=lambda x: hauteurs[x])

        # Essayer de pousser le flot
        poussee = False
        for voisin in range(n):
            if pousser(u, voisin, matrice, preflots, excedents, hauteurs):
                poussee = True
                break

        # Si la poussée n'a pas été possible, réétiqueter
        if not poussee:
            reetiqueter(u, matrice, preflots, excedents, hauteurs)

    # Calcul du flot maximal
    flot_maximal = sum(preflots[source][voisin] for voisin in range(n))

    return flot_maximal, preflots

def afficher_resultats(flot_maximal, matrice_finale):
    """Affiche les résultats formatés comme dans l'exemple fourni."""
    print("Flot maximal:", flot_maximal)
    print("Matrice finale des flots:")
    print("   ", " ".join(f"{i:>3}" for i in range(len(matrice_finale))))
    for i, ligne in enumerate(matrice_finale):
        print(f"{i:>3}", " ".join(f"{val:>3}" for val in ligne))










# Algorithme pour résoudre le flot à coût minimal.

def flot_min_cout(n, capacite, cout, source, arrivee):
    """
    Résout le problème de flot à coût minimal en utilisant Bellman-Ford et F-F.
    """
    flot_voulu = int(input("Entrez la valeur du flot voulu : "))
    flot_actuel = 0
    cout_total = 0
    dernier_chemin = []  # Stocke uniquement le dernier chemin trouvé
    flot_par_arc = []  # Stocke le flot final par arc dans le chemin
    flot = [[0] * n for _ in range(n)]  # Suivre le flot
    capacite_residuelle = [ligne[:] for ligne in capacite]  # Copie des capacités

    while flot_actuel < flot_voulu:
        # Utilisation de Bellman-Ford pour trouver le chemin de coût minimal
        dist, parent = bellmanford(n, source, capacite_residuelle, cout, flot)

        # Vérifier si aucun chemin n'existe
        if dist[arrivee] == float('inf'):
            print("Aucun chemin disponible pour atteindre le flot voulu.")
            break

        # Reconstruction du chemin depuis la table parent
        chemin = []
        sommet_actuel = arrivee
        while sommet_actuel != source:
            sommet_parent = parent[sommet_actuel]
            chemin.append((sommet_parent, sommet_actuel))
            sommet_actuel = sommet_parent
        chemin.reverse()
        dernier_chemin = chemin  # Stocker uniquement le chemin actuel

        # Recherche du flot minimal sur le chemin trouvé
        flot_chemin = float('inf')
        sommet_actuel = arrivee
        while sommet_actuel != source:
            sommet_parent = parent[sommet_actuel]
            flot_chemin = min(flot_chemin, capacite[sommet_parent][sommet_actuel] - flot[sommet_parent][sommet_actuel])
            sommet_actuel = sommet_parent

        # Limiter le flot ajouté pour ne pas dépasser le flot voulu
        flot_chemin = min(flot_chemin, flot_voulu - flot_actuel)

        # Mise à jour des flots et calcul des coûts
        sommet_actuel = arrivee
        while sommet_actuel != source:
            sommet_parent = parent[sommet_actuel]
            flot[sommet_parent][sommet_actuel] += flot_chemin
            flot[sommet_actuel][sommet_parent] -= flot_chemin
            cout_total += flot_chemin * cout[sommet_parent][sommet_actuel]
            sommet_actuel = sommet_parent

        # Mise à jour des valeurs pour le chemin final (flot et coût)
        flot_par_arc = [(u, v, flot[u][v], cout[u][v]) for u, v in dernier_chemin]

        # Mise à jour du flot total
        flot_actuel += flot_chemin

    # Affichage final des résultats
    print("\n===== Résultat final =====")
    print(f"Flot total : {flot_actuel}")
    print(f"Coût total minimal : {cout_total}")
    if dernier_chemin:
        print("Chemin final utilisé avec flots et coûts :")
        for u, v, f, c in flot_par_arc:
            print(f"Arc {u}->{v} : {f} unités de flot, coût par unité : {c}")
    else:
        print("Aucun chemin n'a été trouvé.")
    print("===========================")

    return flot_actuel, cout_total

