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

def pousser(u, v, capacite, flot, excedents, hauteurs):
    """Effectue une opération "pousser" entre deux sommets."""
    if (
        excedents[u] > 0
        and capacite[u][v] - flot[u][v] > 0
        and hauteurs[u] - hauteurs[v] == 1
    ):
        quantite = min(
            excedents[u],
            capacite[u][v] - flot[u][v],
        )
        flot[u][v] += quantite
        flot[v][u] -= quantite
        excedents[u] -= quantite
        excedents[v] += quantite
        print(f"On pousse {quantite} de {u} vers {v}")
        return True
    return False

def reetiqueter(u, capacite, flot, excedents, hauteurs):
    """Réétiquette un sommet en augmentant sa hauteur."""
    min_hauteur = float("inf")
    for voisin in range(len(capacite[u])):
        if capacite[u][voisin] - flot[u][voisin] > 0:
            min_hauteur = min(min_hauteur, hauteurs[voisin])
    if excedents[u] > 0 and min_hauteur < float("inf"):
        hauteurs[u] = min_hauteur + 1
        return True
    print(f"On réétiquete le sommet {u} de hauteur {hauteurs[u]} à {min_hauteur + 1}")
    return False

def algorithme_pousser_reetiqueter(matrice):
    """Implémente l'algorithme pousser-réétiqueter sur une matrice de capacité."""
    n = len(matrice)
    source, puits = 0, n - 1

    # Initialisations
    hauteurs = [0] * n
    hauteurs[source] = n
    excedents = [0] * n
    flot = [[0] * n for _ in range(n)]

    # Initialisation des pré-flots depuis la source
    for voisin in range(n):
        if matrice[source][voisin] > 0:
            flot[source][voisin] = matrice[source][voisin]
            flot[voisin][source] = -matrice[source][voisin]
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
            if pousser(u, voisin, matrice, flot, excedents, hauteurs):
                poussee = True
                print("on pousse de ")
                break

        # Si la poussée n'a pas été possible, réétiqueter
        if not poussee:
            reetiqueter(u, matrice, flot, excedents, hauteurs)

    # Calcul du flot maximal
    flot_maximal = sum(flot[source][voisin] for voisin in range(n))

    return flot_maximal, flot

import random
import time
import matplotlib.pyplot as plt

def generer_probleme_flots(n):
    capacite = [[0] * n for _ in range(n)]
    cout = [[0] * n for _ in range(n)]

    # Remplir la matrice de capacité
    for _ in range(int(n * (n - 1) / 2)):
        i, j = random.sample(range(n), 2)
        capacite[i][j] = random.randint(1, 100)

    # Remplir la matrice de coût
    for i in range(n):
        for j in range(n):
            if capacite[i][j] > 0:
                cout[i][j] = random.randint(1, 100)

    return capacite, cout

def mesurer_temps_execution(algorithme, *args):
    debut = time.perf_counter()
    algorithme(*args)
    fin = time.perf_counter()
    return fin - debut

def analyser_algorithmes(valeurs_n, repetitions=100):
    resultats_ff = {n: [] for n in valeurs_n}
    resultats_pr = {n: [] for n in valeurs_n}
    resultats_min = {n: [] for n in valeurs_n}

    for n in valeurs_n:
        print(f"Analyse pour n={n}...")
        for _ in range(repetitions):
            capacite, cout = generer_probleme_flots(n)
            source, puits = 0, n - 1

            # Mesurer Ford-Fulkerson
            temps_ff = mesurer_temps_execution(ford_fulkerson, capacite, source, puits)
            resultats_ff[n].append(temps_ff)

            # Mesurer Pousser-Réétiqueter
            temps_pr = mesurer_temps_execution(algorithme_pousser_reetiqueter, capacite)
            resultats_pr[n].append(temps_pr)

            # Mesurer Flot à Coût Minimal
            temps_min = mesurer_temps_execution(flot_min_cout, n, capacite, cout, source, puits)
            resultats_min[n].append(temps_min)

    return resultats_ff, resultats_pr, resultats_min

def tracer_nuages(resultats, titre):
    for n, temps in resultats.items():
        plt.scatter([n] * len(temps), temps, label=f"n={n}", alpha=0.5)
    plt.xlabel("Nombre de sommets (n)")
    plt.ylabel("Temps d'exécution (s)")
    plt.title(titre)
    plt.legend()
    plt.show()

def tracer_enveloppes(resultats, titre):
    enveloppes = {n: max(temps) for n, temps in resultats.items()}
    plt.plot(enveloppes.keys(), enveloppes.values(), marker="o", label="Enveloppe supérieure")
    plt.xlabel("Nombre de sommets (n)")
    plt.ylabel("Temps d'exécution maximal (s)")
    plt.title(titre)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Valeurs de n à tester
    valeurs_n = [10, 20, 40, 100, 400, 1000]
    repetitions = 100

    # Analyse des trois algorithmes
    resultats_ff, resultats_pr, resultats_min = analyser_algorithmes(valeurs_n, repetitions)

    # Tracés des nuages de points
    tracer_nuages(resultats_ff, "Ford-Fulkerson : Nuage de points")
    tracer_nuages(resultats_pr, "Pousser-Réétiqueter : Nuage de points")
    tracer_nuages(resultats_min, "Flot à Coût Minimal : Nuage de points")

    # Tracés des enveloppes
    tracer_enveloppes(resultats_ff, "Ford-Fulkerson : Enveloppe supérieure")
    tracer_enveloppes(resultats_pr, "Pousser-Réétiqueter : Enveloppe supérieure")
    tracer_enveloppes(resultats_min, "Flot à Coût Minimal : Enveloppe supérieure")

