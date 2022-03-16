from ville import Ville
from utilitaires import *
from tkinter import *
from affichage import *


def affiche_tournee(listeVAAFF):
    canv = Canvas(root, width=largeur, height=hauteur)

    canv.create_image(0, 0, anchor=NW, image=photo)

    canv.pack(expand=YES, fill="both")
    for i in range(0, len(listeVAAFF)):
        x, y = fromLatLong2pixels(listeVAAFF[i], listeVAAFF, largeur, hauteur)
        xSuiv, ySuiv = fromLatLong2pixels(listeVAAFF[(i+1)%len(listeVAAFF)], listeVAAFF, largeur, hauteur)
        y = hauteur-y
        ySuiv = hauteur - ySuiv
            
        canv.create_line(x, y, xSuiv, ySuiv)  
        canv.create_text(x, y, text=str(listeVAAFF[i].getNum()))
        canv.pack()

        





def plus_proche_voisin(listeV, ville):
    t= []
    t.append(ville)
    
    while len(listeV) > 1:
        _, suivant = plus_proche(listeV, ville)
        t.append(suivant)
        ville = suivant

    return t


def plus_proche_voisin_ameliore(listeVilles):
    listeDistances = []

    for v in listeVilles:
        listeV = listeVilles.copy()
        tournee = plus_proche_voisin(listeV, v)
        listeDistances.append([cout(tournee), tournee])
    
    tournee_min = listeDistances[listeDistances.index(min(listeDistances))][1]

    return tournee_min


def insertion_proche(listeV):

    # on cherche les deux villes les plus éloignées l'une de l'autre
    listeVillesIP = get_villes_plus_eloignees(listeV)
    
    # et on les supprime de la liste de villes
    if(listeVillesIP[0] in listeV and listeVillesIP[1] in listeV):
        listeV.remove(listeVillesIP[0])
        listeV.remove(listeVillesIP[1])
    
    # chaque itération permet de trouver la ville qui étend le moins la tournée
    for i in range(0, len(listeV)):
        distance_min = 9999999999
        index_min = -1
        ville = None
        # on va parcourir la liste de villes pour trouver la ville qui étend le moins la tournée
        for v in listeV:

            # on va chercher l'index auquel la ville ajoutera le moins de distance
            for i in range(0, len(listeVillesIP)):
                # on vérifie si la ville peut prendre la dernière place de la tournée
                if(i == len(listeVillesIP)-1):
                    distance_ajoutee = calculDistance(listeVillesIP[i], v) + calculDistance(v, listeVillesIP[0]) - calculDistance(listeVillesIP[i], listeVillesIP[0])
                # sinon, pour tous les autres éléments de la liste, on calcule la distance ajoutée
                else:
                    distance_ajoutee = calculDistance(listeVillesIP[i], v) + calculDistance(v, listeVillesIP[i+1]) - calculDistance(listeVillesIP[i], listeVillesIP[i+1])
                
                # si la nouvelle distance est mieux, alors on la prends.
                if(distance_ajoutee < distance_min):
                    distance_min = distance_ajoutee
                    index_min = i
                    ville = v
        
        # une fois que la ville et l'index minimum sont trouvés, on insère dans la nouvelle tournée
        listeVillesIP.insert(index_min+1, ville)
        # on enlève la ville de a liste de villes pour éviter qu'elle apparaisse plusieurs fois
        listeV.remove(ville)

    return listeVillesIP



def insertion_loin(listeV):

    # on cherche les deux villes les plus éloignées l'une de l'autre
    listeVillesIL = get_villes_plus_eloignees(listeV)
    
    # et on les supprime de la liste de villes
    if(listeVillesIL[0] in listeV and listeVillesIL[1] in listeV):
        listeV.remove(listeVillesIL[0])
        listeV.remove(listeVillesIL[1])
    
    # chaque itération permet de trouver la ville qui étend le moins la tournée
    for i in range(0, len(listeV)):
        distance_max = 0
        index_min = -1
        ville = None
        
        temp_index = -1
        temp_ville = None
        # on va parcourir la liste de villes pour trouver la ville qui étend le moins la tournée
        for v in listeV:

            distance_min = 9999999999
            # on va chercher l'index auquel la ville ajoutera le moins de distance
            for i in range(0, len(listeVillesIL)):
                # on vérifie si la ville peut prendre la dernière place de la tournée
                if(i == len(listeVillesIL)-1):
                    distance_ajoutee = calculDistance(listeVillesIL[i], v) + calculDistance(v, listeVillesIL[0]) - calculDistance(listeVillesIL[i], listeVillesIL[0])
                # sinon, pour tous les autres éléments de la liste, on calcule la distance ajoutée
                else:
                    distance_ajoutee = calculDistance(listeVillesIL[i], v) + calculDistance(v, listeVillesIL[i+1]) - calculDistance(listeVillesIL[i], listeVillesIL[i+1])
                
                # si la nouvelle distance est mieux, alors on la prends.
                if(distance_ajoutee < distance_min):
                    distance_min = distance_ajoutee
                    temp_index = i
                    temp_ville = v
            
            if(distance_min > distance_max and distance_min != 9999999999):
                distance_max = distance_min
                index_min = temp_index
                ville = temp_ville
                
        
        # une fois que la ville et l'index minimum sont trouvés, on insère dans la nouvelle tournée
        listeVillesIL.insert(index_min+1, ville)
        # on enlève la ville de a liste de villes pour éviter qu'elle apparaisse plusieurs fois
        listeV.remove(ville)

    return listeVillesIL



def recherche_locale(listeVL):
    t_courante = listeVL
    fini = False
    while not fini:
        fini = True
        cout_t_courante = cout(t_courante)
        t_voisin = exploration_successeurs_premier_dabord(t_courante)
        if(cout(t_voisin) < cout_t_courante):
            t_courante = t_voisin
            fini = False
    return t_courante



def exploration_successeurs_premier_dabord(t_courante):
    for i in range(0, len(t_courante)):
        if(calculDistance(t_courante[(i-1)%len(t_courante)], t_courante[i]) + calculDistance(t_courante[(i+1)%len(t_courante)], t_courante[(i+2)%len(t_courante)]) > calculDistance(t_courante[(i-1)%len(t_courante)], t_courante[(i+1)%len(t_courante)]) + calculDistance(t_courante[i], t_courante[(i+2)%len(t_courante)])):
            #swap les deux positions
            t_courante[i], t_courante[i+1] = t_courante[i+1], t_courante[i]
    return t_courante


def echange_sommets_quelconques(t_courante):
    fini = False
    while not fini:
        fini = True
        for i in range(0, len(t_courante)):
            for j in range(i+1, len(t_courante)):
                cout_temp = cout(t_courante)
                t_courante[i], t_courante[j] = t_courante[j], t_courante[i]
                if(cout(t_courante) > cout_temp):
                    t_courante[i], t_courante[j] = t_courante[j], t_courante[i]
                else:
                    fini = False
    return t_courante


def echange_2_opt(t_courante):
    fini = False
    while not fini:
        fini = True
        for i in range(0, len(t_courante)):
            for j in range(i+2, len(t_courante)):
                cout_temp = cout(t_courante)
                t_courante[i:j] = t_courante[i:j][::-1]
                if(cout(t_courante) > cout_temp):
                    t_courante[i:j] = t_courante[i:j][::-1]
                else:
                    fini = False
    return t_courante


if __name__ == "__main__":

    #CHARGEMENT DES DONNEES
    #============================================================#
    f = open("instances/top80.txt", "r")
    lines = f.readlines()
    listeVilles = []

    tourneeVilles = []

    hauteur = 754
    largeur = 686



    for x in lines:
        ville = x.split(" ")
        v = Ville(ville[0], ville[1], ville[2], ville[3])
        listeVilles.append(v)

    listeVillesCopie = listeVilles.copy()


    root = Tk(className='TP recherche opérationnelle')
    root.geometry("686x754")

    photo = PhotoImage(file="carte.png")
    
    #============================================================#

    
    
    # listeVillesCopie = listeVilles.copy()
    # distanceTotaleOrdre = cout(listeVillesCopie)
    # print(f"Distance totale parcourue ordre croissant: {distanceTotaleOrdre} km")
    # print(f"Chemin utilise dans l'ordre : {afficheTour(listeVilles)}\n\n")

    # print(f"Ville la plus proche de {listeVilles[0].getNom()} : {plus_proche(listeVilles, listeVilles[0])[1].getNom()}")

    # listeVillesCopie = listeVilles.copy()


    # tourneeAlea = tourAleatoire(listeVillesCopie)
    # distanceTotale = cout(tourneeAlea)
    # print(f"Distance totale parcourue aleatoire: {cout(tourneeAlea)} km")
    # print(f"Chemin utilise aleatoire : {afficheTour(tourneeAlea)}\n\n")




    # METHODES GLOUTONNES


    listeVillesCopie = listeVilles.copy()

    print("Ville 1 " + listeVillesCopie[0].getNom())
    tournee_glouton = plus_proche_voisin(listeVillesCopie, listeVilles[0])
    print(f"Chemin utilise dans glouton : {afficheTour(tournee_glouton)}")
    print(f"Distance totale parcourue glouton : {cout(tournee_glouton)} km\n\n")


    # listeVillesCopie = listeVilles.copy()

    # tournee_glouton_ameliore = plus_proche_voisin_ameliore(listeVillesCopie)
    # print(f"Chemin utilise dans glouton ameliore : {afficheTour(tournee_glouton_ameliore)}")
    # print(f"Distance totale parcourue glouton ameliore: {cout(tournee_glouton_ameliore)} km\n\n")

    
    # listeVillesCopie = listeVilles.copy()
    
    # listeVillesIP1 = insertion_proche(listeVillesCopie)
    # print(f"Chemin utilise dans insertion proche : {afficheTour(listeVillesIP1)}")
    # print(f"Distance totale parcourue insertion proche : {cout(listeVillesIP1)} km\n\n")


    # listeVillesCopie = listeVilles.copy()

    # listeVillesIL = insertion_loin(listeVillesCopie)
    # print(f"Chemin utilise dans insertion loin : {afficheTour(listeVillesIL)}")
    # print(f"Distance totale parcourue insertion loin : {cout(listeVillesIL)} km\n\n")
    

    # listeRechercheLocale = recherche_locale(tournee_glouton)
    # print(f"Chemin utilise dans recherche locale : {afficheTour(listeRechercheLocale)}")
    # print(f"Distance totale parcourue recherche locale : {cout(listeRechercheLocale)} km\n\n")
    
    # liste_sommets_qq = echange_sommets_quelconques(tournee_glouton)
    # print(f"Chemin utilise dans recherche sommets quelconques : {afficheTour(liste_sommets_qq)}")
    # print(f"Distance totale parcourue recherche sommets quelconques : {cout(liste_sommets_qq)} km\n\n")
    
    liste_echange_2_opt = echange_2_opt(tournee_glouton)
    print(f"Chemin utilise dans recherche sommets quelconques : {afficheTour(liste_echange_2_opt)}")
    print(f"Distance totale parcourue recherche sommets quelconques : {cout(liste_echange_2_opt)} km\n\n")

    affiche_tournee(liste_echange_2_opt)

    

    root.mainloop()