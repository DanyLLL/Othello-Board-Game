from tkinter import *

fenetre = Tk()
fenetre.title("TNSI_LIM_Dany_jeu de Othello")
fenetre.config(height=600, width=850, bg="#F8B195")
Canevas = Canvas(fenetre, height=500, width=500, bg="#FDFD96")
Canevas.place(x=50, y=60)

texte_othello = Label(fenetre, text="Othello", font=("Courier", 45, "underline"), bg="#BF3030", fg="white")

texte_regles = Label(fenetre, font=("Times", 14, "bold"), bg="#FDFD96",
                     text="Le but du jeu d’avoir à la fin le plus de jeton de sa couleur.\n"
                          "À chaque tour, le joueur peut, s’il le désire, poser un jeton \n de sa couleur  en respectant les règles suivantes, puis laisse \n"
                          "le tour à l’autre joueur. Les règles sont simples:\n• On ne peut placer d’un jeton de sa couleur,on peut \naussi passer son tour.\n"
                          "• Si on place un jeton, cela doit être de telle façon qu’au \nmoins un jeton de l’autre couleur se retrouve"
                          " aligné \n(verticalement,horizontalement ou en diagonale) entre le \nnouveau jeton posé et un autre jeton de la même couleur.")

texte_nbr_coup = Label(fenetre, font=("Times", 14, "bold"), bg="#FDFD96", text="Nombre de coup :")

texte_othello.place(x=165, y=30)
texte_regles.place(x=53, y=150)


class Pile:
    def __init__(self):
        self.valeurs = []

    def est_vide(self):
        return self.valeurs == []

    def empile(self, valeur):
        self.valeurs.append(valeur)

    def depile(self):
        if self.valeurs: return self.valeurs.pop()

    def __str__(self):
        ch = ''
        for x in self.valeurs:
            ch = "| " + str(x) + " |" + "\n" + ch
        return ch + "⎺⎺⎺⎺⎺\n"


class plateau:
    def __init__(self):
        self.platxt = [["" for c in range(8)] for l in range(8)]
        self.plajts = [[None for c in range(8)] for l in range(8)]
        self.liste_coup = Pile()
        self.tour = 0
        self.bouton_rejouer = Button(fenetre, text="Rejouer une nouvelle partie", command=self.rejouer, height=3,
                                     width=27, font=("Courier", 8, "italic"), fg="black", bg="#E4CDA7")
        self.comptage_noir = 2
        self.comptage_blanc = 2

    def debut(self):
        self.plajts[4][3] = jeton(self, 4, 3, 1)
        self.platxt[4][3] = "1"
        self.plajts[3][4] = jeton(self, 3, 4, 1)
        self.platxt[3][4] = "1"
        self.plajts[3][3] = jeton(self, 3, 3, 0)
        self.platxt[3][3] = "0"
        self.plajts[4][4] = jeton(self, 4, 4, 0)
        self.platxt[4][4] = "0"
        self.placer_bouton_piece_possible()
        self.bouton_rejouer.place(x=600, y=200)
        self.mettre_a_jour_labels()

    def comptage_points(self):
        n = 0
        b = 0
        for i in range(8):
            for j in range(8):
                if self.platxt[i][j] == "0":
                    n += 1
                if self.platxt[i][j] == "1":
                    b += 1
        self.comptage_noir = n
        self.comptage_blanc = b
        return self.comptage_noir, self.comptage_blanc

    def rejouer(self):
        Canevas.delete('all')
        for i in range(8):
            for j in range(8):
                e = self.plajts[i][j]
                if e != None:
                    e.bouton_piece_possible.destroy()
                    for btn in e.liste_bouton_coup_possible:
                        btn.destroy()
        self.tour = 0
        self.platxt = [["" for c in range(8)] for l in range(8)]
        self.plajts = [[None for c in range(8)] for l in range(8)]
        creation_plateau()
        self.debut()

    def verifieplace(self, x_source, y_source):
        couleur_joueur = self.platxt[x_source][y_source]
        if couleur_joueur == "": return []
        couleur_adverse = str(1 - int(couleur_joueur))

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        destinations = []

        for dx, dy in directions:
            x_scan, y_scan = x_source + dx, y_source + dy
            trouve_adverse = False

            while 0 <= x_scan < 8 and 0 <= y_scan < 8 and self.platxt[x_scan][y_scan] == couleur_adverse:
                trouve_adverse = True
                x_scan += dx
                y_scan += dy

            if trouve_adverse and 0 <= x_scan < 8 and 0 <= y_scan < 8 and self.platxt[x_scan][y_scan] == "":
                destinations.append((x_scan, y_scan, dx, dy))

        return destinations

    def placer_bouton_piece_possible(self):
        self.place_forget_all()
        joueur_courant = self.tour % 2
        a_des_coups = False

        for i in range(8):
            for j in range(8):
                jeton_temp = self.plajts[i][j]
                if jeton_temp is not None and jeton_temp.get_couleur() == joueur_courant:
                    if self.verifieplace(i, j):
                        cx = i * 50 + 50 + 15
                        cy = j * 50 + 50 + 15
                        jeton_temp.get_bouton_piece_possible().place(x=cx, y=cy)
                        a_des_coups = True

        if not a_des_coups:
            adversaire = (self.tour + 1) % 2
            a_des_coups_adversaire = False
            for i in range(8):
                for j in range(8):
                    jeton_temp = self.plajts[i][j]
                    if jeton_temp is not None and jeton_temp.get_couleur() == adversaire:
                        if self.verifieplace(i, j):
                            a_des_coups_adversaire = True
                            break
                if a_des_coups_adversaire: break

            if a_des_coups_adversaire:
                self.tour += 1
                self.mettre_a_jour_labels()
                self.placer_bouton_piece_possible()
            else:
                texte_nbr_coup.config(text="Fin de partie !")

    def place(self, x, y):
        jeton_selectionne = self.plajts[x][y]
        if not jeton_selectionne.get_piece_choisi():
            self.place_forget_all()
            cx = x * 50 + 50 + 15
            cy = y * 50 + 50 + 15
            jeton_selectionne.get_bouton_piece_possible().place(x=cx, y=cy)
            jeton_selectionne.place()
            jeton_selectionne.piece_choisi = True
        else:
            self.annuler_selection(x, y)

    def annuler_selection(self, x, y):
        jeton_selectionne = self.plajts[x][y]
        if jeton_selectionne:
            jeton_selectionne.piece_choisi = False
            for c in jeton_selectionne.get_liste_bouton_coup_possible():
                c.destroy()
            jeton_selectionne.liste_bouton_coup_possible = []
            self.placer_bouton_piece_possible()

    def place_forget_all(self):
        for i in range(8):
            for j in range(8):
                e = self.plajts[i][j]
                if e != None:
                    e.bouton_piece_possible.place_forget()

    def mettre_a_jour_labels(self):
        noirs, blancs = self.comptage_points()
        tour_texte = "Noir" if self.tour % 2 == 0 else "Blanc"
        texte_nbr_coup.config(text=f"Tour : {tour_texte} (Coup {self.tour})")
        if hasattr(self, 'affichage_nbr_jeton_noir'):
            self.affichage_nbr_jeton_noir.config(text=str(noirs) + " jetons noirs sur le plateau !")
            self.affichage_nbr_jeton_blanc.config(text=str(blancs) + " jetons blancs sur le plateau !")
        fenetre.update()


dim = 50


class jeton:
    def __init__(self, p, x=0, y=0, c=0):
        self.coord = x, y
        self.c = c
        cx = x * dim + 50
        cy = y * dim + 50
        self.des = Canevas.create_oval(cx + 5, cy + 5, cx + 45, cy + 45, fill=["black", "white"][self.c])
        self.bouton_piece_possible = Button(Canevas, text="P", command=lambda: p.place(x, y), bg="lightblue")
        self.plateau = p

        if not hasattr(self.plateau, 'affichage_nbr_jeton_noir'):
            self.plateau.affichage_nbr_jeton_noir = Label(fenetre, font=("Times", 14, "bold"), bg="#FDFD96", text="")
            self.plateau.affichage_nbr_jeton_blanc = Label(fenetre, font=("Times", 14, "bold"), bg="#FDFD96", text="")
            self.plateau.affichage_nbr_jeton_noir.place(x=600, y=300)
            self.plateau.affichage_nbr_jeton_blanc.place(x=600, y=400)

        self.liste_bouton_coup_possible = []
        self.piece_choisi = False

    def change(self):
        self.c = 1 - self.c
        Canevas.itemconfig(self.des, fill=["black", "white"][self.c])
        self.plateau.platxt[self.coord[0]][self.coord[1]] = str(self.c)

    def manger(self, x_dest, y_dest, dx, dy):
        x_source, y_source = self.coord

        self.plateau.plajts[x_dest][y_dest] = jeton(self.plateau, x_dest, y_dest, self.c)
        self.plateau.platxt[x_dest][y_dest] = str(self.c)

        x_scan, y_scan = x_source + dx, y_source + dy
        while (x_scan, y_scan) != (x_dest, y_dest):
            self.plateau.plajts[x_scan][y_scan].change()
            x_scan += dx
            y_scan += dy

        for btn in self.liste_bouton_coup_possible:
            btn.destroy()
        self.liste_bouton_coup_possible = []
        self.piece_choisi = False

        self.plateau.tour += 1
        self.plateau.mettre_a_jour_labels()
        self.plateau.placer_bouton_piece_possible()

    def get_couleur(self):
        return self.c

    def get_bouton_piece_possible(self):
        return self.bouton_piece_possible

    def get_liste_bouton_coup_possible(self):
        return self.liste_bouton_coup_possible

    def get_coord(self):
        return self.coord

    def get_piece_choisi(self):
        return self.piece_choisi

    def place(self):
        x_source, y_source = self.coord
        coups = jeu.verifieplace(x_source, y_source)
        if coups:
            for x_dest, y_dest, dx, dy in coups:
                bouton_temp = Button(Canevas, text="D", bg="lightgreen",
                                     command=lambda x_d=x_dest, y_d=y_dest, d_x=dx, d_y=dy: self.manger(x_d, y_d, d_x,d_y))
                cx_dest = x_dest * dim + 50 + 15
                cy_dest = y_dest * dim + 50 + 15
                bouton_temp.place(x=cx_dest, y=cy_dest)
                self.liste_bouton_coup_possible.append(bouton_temp)


jeu = plateau()


def jouer():
    texte_regles.place_forget()
    Bouton_demarrer.place_forget()
    Bouton_charger_partie_existante.place_forget()
    creation_plateau()
    jeu.debut()
    texte_nbr_coup.place(x=600, y=100)


def creation_plateau():
    for i in range(8):
        for j in range(8):
            x1, y1 = i * 50 + 50, j * 50 + 50
            x2, y2 = x1 + 50, y1 + 50
            Canevas.create_rectangle(x1, y1, x2, y2, outline="black", fill="yellow")


def charger_partie_existante():
    print("Fonctionnalité non implémentée")


Bouton_demarrer = Button(fenetre, text="Jouer une nouvelle partie", command=jouer, height=3, width=30,font=("Courier", 8, "italic"), fg="black", bg="#E4CDA7")
Bouton_demarrer.place(x=190, y=400)
Bouton_charger_partie_existante = Button(fenetre, text="Charger une partie existante", command=charger_partie_existante,height=3, width=30, font=("Courier", 8, "italic"), fg="black", bg="#E4CDA7")
Bouton_charger_partie_existante.place(x=190, y=470)

fenetre.mainloop()