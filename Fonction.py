def choisir_Test():
    # Demande à l'utilisateur de choisir un numéro de test et retourne le chemin du fichier correspondant
    x = int(input("Entrer le numero du Test que vous voulez afficher : "))
    fichier = f"Test/Test{x}.txt"
    print(fichier)
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

            # Affichage de la matrice tronquée avec s, alphabet, et t
            print("\nVoici la matrice de capaciter:")
            print_matrice(matrice_capaciter)

    except Exception as e:
        print(f"Erreur lors de la lecture ou du traitement du fichier {chemin_fichier} : {e}")

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

                print("\nVoici la matrice des coûts :")
                print_matrice(matrice_cout)
            else:
                print("\nPas assez de lignes pour une matrice des coûts.")

    except Exception as e:
        print(f"Erreur lors de la lecture ou du traitement du fichier {chemin_fichier} : {e}")

def print_matrice(matrice):
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

