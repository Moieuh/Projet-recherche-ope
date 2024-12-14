from Fonction import *

SOURCE = 0
r=0
while r==0:
    chemin = choisir_Test()
    m_cap = matrice_capaciter(chemin)
    m_cout = matrice_cout(chemin)
    print("\nMatrice de capacité:")
    print_matrice(m_cap)

    n = len(m_cap)
    arrivee = n - 1  # Exemple d'arrivée, peut être modifié selon les besoins
    flot = [[0] * n for _ in range(n)]  # Matrice de flot initiale (tout à 0)

    if m_cout is not None:
        print("\nMatrice de coût:")
        print_matrice(m_cout)

    if m_cout is None:
        choix = input(
            "Quel algorithme voulez-vous utiliser ?\n"
                "0 pour l'algorithme Pousser-Réétiqueter\n"
                "1 pour l'algorithme Ford-Fulkerson: "
            )

        if choix == "0":
            print("\nExécution de l'algorithme Pousser-Réétiqueter...")
            flot_maximal, matrice_finale = algorithme_pousser_reetiqueter(m_cap)
            afficher_resultats(flot_maximal, matrice_finale)
        elif choix == "1":
            print("\nExécution de l'algorithme Ford-Fulkerson...")
            flot = ford_fulkerson(m_cap, SOURCE, arrivee)
            print(f"Le flot maximum de la source {SOURCE} au puits {arrivee} est : {flot}")

    else:
        print("Exécution de l'algorithme flot à coût min")
        flot_min_cout(n,m_cap,m_cout,SOURCE,arrivee)
    print("\n")
    r=int(input("Voulez essayer un autre fichier?\n oui:0\n non:1 "))