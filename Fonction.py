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


def bfs(graphe, sommet_initial, sommet_arrivee, predecesseur):  
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

def ford_fulkerson(graphe, sommet_initial, sommet_arrivee):  
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


# Algorithme Pousser-Réétiqueter

# Initialisation

def initialiser_matrice(matrice):

    # Initialiser les hauteurs, excédents et flots à 0
    n = len(matrice) 
    hauteur = [0] * n 
    excedent = [0] * n 
    flots = [[0] * n for _ in range(n)]

    source = 0              # La source est le sommet 0
    hauteur[source] = n     # La hauteur de la source est égale au nombre de sommets

    # Initialiser les flots sortant de la source
    for v in range(n):
        if matrice[source][v] > 0:
            flots[source][v] = matrice[source][v] 
            excedent[v] += matrice[source][v] 
            excedent[source] -= matrice[source][v] 

    return hauteur, excedent, flots

# Pousser

def pousser(u, v, matrice, flots, excedent):

    # Calcul de la capacité résiduelle
    capacite_residuelle = matrice[u][v] - flots[u][v]

    # Calcul du flot à pousser (le minimum entre l'excédent de u et la capacité résiduelle)
    flux = min(excedent[u], capacite_residuelle)

    # Mise à jour des flots et des excédants
    flots[u][v] += flux
    flots[v][u] -= flux
    excedent[u] -= flux
    excedent[v] += flux

# Réétiqueter 

def reetiqueter(u, matrice, flots, hauteur):

    n = len(matrice)
    hauteur_min = float('inf')

    # Trouver la hauteur minimale parmi les voisins accessibles
    for v in range(n):
        if matrice[u][v] - flots[u][v] > 0:  # Capacité résiduelle positive
            hauteur_min = min(hauteur_min, hauteur[v])

    # Mettre à jour la hauteur de u
    if hauteur_min < float('inf'):
        hauteur[u] = hauteur_min + 1

# Réalisation de l'algorithme pousser-réétiqueter

def algorithme_pousser_reetiqueter(matrice):

    n = len(matrice)    # Nombre de sommets
    source = 0
    puits = n - 1

    # Initialisation
    hauteur, excedent, flots = initialiser_matrice(matrice)

    # Liste des sommets excédentaires (hors source et puits)
    sommets_excedentaires = [i for i in range(n) if i != source and i != puits and excedent[i] > 0]

    while sommets_excedentaires:
        
        # Trier les sommets excédentaires par priorité : hauteur décroissante puis indice croissant
        sommets_excedentaires.sort(key=lambda x: (-hauteur[x], x))
        u = sommets_excedentaires.pop(0)    # Prendre le sommet avec la plus grande priorité
        action_effectuee = False

        # Obtenir les voisins triés avec priorité pour pousser
        voisins = list(range(n))
        voisins.sort(key=lambda v: (v != puits, v))     # Priorité des opérations dans l’algorithme Pousser-réétiqueter

        # Pousser le flot vers les voisins si possible
        for v in voisins:
            if matrice[u][v] - flots[u][v] > 0 and hauteur[u] > hauteur[v]:     # Capacité résiduelle et condition de hauteur
                pousser_matrice(u, v, matrice, flots, excedent)
                action_effectuee = True

                # Ajouter v aux sommets excédentaires s'il devient excédentaire
                if excedent[v] > 0 and v not in sommets_excedentaires and v != source and v != puits:
                    sommets_excedentaires.append(v)
                break # Sortie de la boucle

        # Réétiqueter si aucune poussée n'est possible
        if not action_effectuee:
            reetiqueter_matrice(u, matrice, flots, hauteur)
            sommets_excedentaires.append(u)     # Réajouter u après réétiquetage

    # Calculer le flot maximal
    flot_max = sum(flots[source][v] for v in range(n))

    #affichage de la valeur maximale du flot et de la matrice des flots
    return flot_max, flots

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

