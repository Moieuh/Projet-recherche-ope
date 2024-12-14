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
