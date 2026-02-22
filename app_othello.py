#Programme réalisé par LIM Dany
#Création de la fenêtre :
from tkinter import*
fenetre=Tk()
fenetre.title("TNSI_LIM_Dany_jeu de Othello")
fenetre.config(height=600,width=600,bg="#F8B195")
Canevas=Canvas(fenetre,height=500,width=500,bg="#FDFD96")
Canevas.place(x=50,y=60)

########################################################################################################################

#Création des Labels :

texte_othello=Label(fenetre,text="Othello",font=("Courier",45,"underline"),bg="#BF3030",fg="white")

texte_regles=Label(fenetre,font=("Times",14,"bold"),bg="#FDFD96",text="Le but du jeu d’avoir à la fin le plus de jeton de sa couleur.\n"
"À chaque tour, le joueur peut, s’il le désire, poser un jeton \n de sa couleur  en respectant les règles suivantes, puis laisse \n"
"le tour à l’autre joueur. Les règles sont simples:\n• On ne peut placer d’un jeton de sa couleur,on peut \naussi passer son tour.\n"
"• Si on place un jeton, cela doit être de telle façon qu’au \nmoins un jeton de l’autre couleur se retrouve"
" aligné \n(verticalement,horizontalement ou en diagonale) entre le \nnouveau jeton posé et un autre jeton de la même couleur.")

texte_nbr_coup=Label(fenetre,font=("Times",14,"bold"),bg="#FDFD96",text="Nombre de coup :")

########################################################################################################################

#Placement des labels :

texte_othello.place(x=165,y=30)
texte_regles.place(x=53,y=150)

########################################################################################################################

#Importation de le classe Pile :

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

########################################################################################################################

#Création de la classe plateau :

class plateau:
    def __init__(self):
        #Initialisation à 0 des tours et à 2 du nombre de jetons noirs et blancs (de départ)
        self.platxt = [["" for c in range(8)] for l in range(8)] # pour les tests
        self.plajts = [[None for c in range(8)] for l in range(8)] # pour les jetons et le canevas
        self.liste_coup = Pile() # pour la liste des coups successifs
        self.tour = 0
        self.bouton_rejouer = Button(fenetre, text="Rejouer une nouvelle partie", command=self.rejouer,height=3, width=27, font=("Courier", 8, "italic"), fg="black", bg="#E4CDA7")
        self.comptage_noir = 2
        self.comptage_blanc = 2
    #Création de la méthode debut qui permet de lancer le jeu
    def debut(self):
        #Placement des jetons dans plajts et platxt
        self.plajts[4][3] = jeton(self,5,4,1)
        self.platxt[4][3] = "1"
        self.plajts[3][4] = jeton(self,4,5,1)
        self.platxt[3][4] = "1"
        self.plajts[3][3] = jeton(self,4,4,0)
        self.platxt[3][3] = "0"
        self.plajts[4][4] = jeton(self,5,5,0)
        self.platxt[4][4] = "0"
        #Placement du bouton pour rejouer et des boutons qui représentent les pièces / jetons que l'on peut jouer
        self.placer_bouton_piece_possible()
        self.bouton_rejouer.place(x=600,y=200)

    #Création de la méthode comptage_points qui permet de compter le nombre de jetons sur le plateau
    def comptage_points(self):
        for i in range(8):
            for j in range(8):
                if self.platxt[i][j]=="0":
                    self.comptage_noir = self.comptage_noir + 1
                    self.comptage_blanc = self.comptage_blanc - 1
                if self.platxt[i][j]=="1":
                    self.comptage_noir = self.comptage_noir - 1
                    self.comptage_blanc = self.comptage_blanc + 1
            return self.comptage_noir,self.comptage_blanc
    #Création de la méthode rejouer qui permet de rejouer la partie
    def rejouer(self):
        Canevas.delete('all')
        self.tour = 0
        creation_plateau()
        self.debut()
    """verifieplace prend donc x et y en paramètres représentant les coordonnées du jeton dont l'on souhaite voir 
    les possibilités de jeu (de saut),cette méthode retourne donc la liste direct_possible"""
    def verifieplace(self,x,y):
        #Erreur dans le code donné que je me suis permis de changer (self.platxt[x][y] != "":)
        if self.platxt[x][y] == "" :
            return []
        #Tous les couples représente ici les coups possibles sur le plateau
        possible = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0),(1,-1), (0,-1)]
        direct_possible = []
        for dir in possible:
            xx, yy = x+dir[0],y+dir[1]
            if 8>xx>=0 and 8>yy>=0:
                if self.platxt[xx][yy]==str(1-self.tour %2):
                    while 8>xx>=0 and 8>yy>=0 and self.platxt[xx][yy]==str(1-self.tour %2) :
                        xx = xx + dir[0]
                        yy = yy + dir[1]
                        #Autre partie du code que j'ai changé (and self.platxt[xx][yy]==__(self.tour%2)
                        if 8>xx>=0 and 8>yy>=0 and self.platxt[xx][yy]=="":
                            direct_possible.append(dir)
        return direct_possible

    #Méthode qui permet de placer tous les boutons qui représentent donc le jeton que le joueur noir ou blanc (dépendant du tour) peut jouer
    def placer_bouton_piece_possible(self):
        self.place_forget_all()
        for i in range(8):
            for j in range(8):
                #Création d'un jeton temporaire
                jeton_temp = self.plajts[i][j]
                #Si jeton_temp != None cela veut dire qu'il s'agit d'un jeton
                if jeton_temp != None:
                    #On vérifie s'il s'agit du tour noir
                    if self.tour % 2 == 0:
                        #Si le jeton_temp est de couleur noir alors on lui attribue un bouton
                        if jeton_temp.get_couleur() == 0:
                            coord_temp = jeton_temp.get_coord()
                            jeton_temp.get_bouton_piece_possible().place(x=coord_temp[0]*dim+70, y=coord_temp[1]*dim+70)
                    else:
                        #Et inversement
                        if jeton_temp.get_couleur() == 1:
                            coord_temp = jeton_temp.get_coord()
                            jeton_temp.get_bouton_piece_possible().place(x=coord_temp[0]*dim+70, y=coord_temp[1]*dim+70)

    #Méthode qui permet de créer "l'animation" de la prise de jeton,c'est-à-dire que cette méthode
    #sert donc à place_forget les jetons que le joueur ne veut pas utiliser et permet aussi de lui faire apparaître
    #ses possibilités de jeu
    def place(self,x,y):
        """Méthode place qui prend donc x et y en paramètre"""
        if not self.plajts[x][y].get_piece_choisi():
            for i in range(8):
                for j in range(8):
                    if i != x and j != y and self.plajts[i][j] != None:
                        #get_bouton_piece_possible qui renvoie un bouton dont le texte est "P"
                        self.plajts[i][j].get_bouton_piece_possible().place_forget()
            self.plajts[x][y].place()
            #piece_choisi=True puisqu'on a selectionné un jeton
            self.plajts[x][y].piece_choisi=True

        else:
            #piece_choisi=False puisqu'on a "laché ce jeton"
            self.plajts[x][y].piece_choisi=False
            self.placer_bouton_piece_possible()
            #Place_forget de tous les jetons non utilisés grace à une liste de boutons
            for c in self.plajts[x][y].get_liste_bouton_coup_possible():
                c.place_forget()
            self.plajts[x][y].liste_bouton_coup_possible = []

    #Méthode qui permet de place_forget tous les boutons
    def place_forget_all(self):
        for i in range(8):
            for j in range(8):
                e = self.plajts[i][j]
                if e != None:
                    e.bouton_piece_possible.place_forget()

dim = 50 # plateau dont les cases font 50pixels de côtés

#Création de la classe jeton
class jeton:
    def __init__(self, p,x=0, y=0, c=0):
        #Initialisation de l'attribut piece_choisi à False pour permettre "l'animation" de prise de jeton
        self.coord = x,y
        self.c = c
        self.des = Canevas.create_oval(x*dim+dim//20,y*dim+dim//20, (x+1)*dim-dim//20,(y+1)*dim-dim//20,fill=["black","white"][self.c])
        self.bouton_piece_possible = Button(fenetre, text="P",command=lambda: p.place(x-1,y-1))
        self.plateau = p
        self.affichage_nbr_jeton_noir = Label(fenetre, font=("Times", 14, "bold"), bg="#FDFD96", text=str(self.plateau.comptage_points()[1] + 1) + " jetons noirs sur le plateau !")
        self.affichage_nbr_jeton_blanc = Label(fenetre, font=("Times", 14, "bold"), bg="#FDFD96", text=str(self.plateau.comptage_points()[0] - 1) + " jeton blanc sur le plateau !")
        fenetre.update()
        self.liste_bouton_coup_possible= []
        self.piece_choisi = False
    def change(self):
        self.c = 1-self.c
        Canevas.itemconfig(self.des, fill=["black","white"][self.c])
        fenetre.update()
    #Méthode qui permet de retourner le jeton adverse et de jouer un coup valide
    def manger(self,x,y):
        #correspond au mouvement d'un jeton vers la droite
        if x > 0 and y == 0:
            for n in range(x):
                #On change ici de couleur le / les jetons qui ont été "sauté" / "mangé" par les jetons adverses, qui doivent donc être retournés
                self.plateau.plajts[self.coord[0]+n][self.coord[1]-1].change()
                self.plateau.platxt[self.coord[0]+n][self.coord[1]-1]=str(self.c)
                #On enlève tous les autres boutons pour empêcher des coups qui ne sont plus possibles
            for e in self.liste_bouton_coup_possible:
                e.place_forget()
            #On remet piece_choisi en False pour permettre la sélection de d'autres jetons par l'adversaire lors de son tour
            #On réinitialise self.liste_bouton_coup_possible à vide pour toujours place_forget() les possibilités qui n'ont pas été choisies par le joueur
            self.liste_bouton_coup_possible = []
            self.piece_choisi = False
            self.plateau.plajts[self.coord[0]+x+1][self.coord[1]]=jeton(self.plateau,self.get_coord()[0]+x+1,self.get_coord()[1],self.c)

        #correspond au mouvement d'un jeton vers le haut
        elif x == 0 and y < 0:
            #n in range(-1,y-1,-1) permet de régler le problème dû aux valeurs négatives de y comme y < 0,cela allait causer des problèmes lors du change() avec une boucle simple
            for n in range(-1,y-1,-1):
                self.plateau.plajts[self.coord[0]-1][self.coord[1]+n-1].change()
                self.plateau.platxt[self.coord[0]-1][self.coord[1]+n-1]=str(self.c)
            for e in self.liste_bouton_coup_possible:
                e.place_forget()
            self.liste_bouton_coup_possible = []
            self.piece_choisi = False
            self.plateau.plajts[self.coord[0]][self.coord[1]+y-1] = jeton(self.plateau, self.get_coord()[0], self.get_coord()[1]+y-1,self.c)

        # correspond au mouvement d'un jeton vers la gauche
        elif x < 0 and y==0:
            for n in range(-1,x-1,-1):
                self.plateau.plajts[self.coord[0]-1+n][self.coord[1]-1].change()
                self.plateau.platxt[self.coord[0]-1+n][self.coord[1]-1]=str(self.c)
            for e in self.liste_bouton_coup_possible:
                e.place_forget()
            self.liste_bouton_coup_possible = []
            self.piece_choisi = False
            self.plateau.plajts[self.coord[0] + x - 1][self.coord[1]] = jeton(self.plateau, self.get_coord()[0] + x - 1,self.get_coord()[1], self.c)

        #correspond au mouvement d'un jeton vers le bas
        elif x == 0 and y>0:
            for n in range(y):
                self.plateau.plajts[self.coord[0]-1][self.coord[1]+n].change()
                self.plateau.platxt[self.coord[0]-1][self.coord[1]+n]=str(self.c)
            for e in self.liste_bouton_coup_possible:
                e.place_forget()
            self.liste_bouton_coup_possible = []
            self.piece_choisi = False
            self.plateau.plajts[self.coord[0]][self.coord[1] + y + 1] = jeton(self.plateau, self.get_coord()[0],self.get_coord()[1] + y + 1, self.c)

        #correspond au mouvement d'un jeton vers en haut à gauche
        elif x < 0 and y <0:
            for n in range(-1,x-1,-1):
                self.plateau.plajts[self.coord[0]-1+n][self.coord[1]-1+n].change()
                self.plateau.platxt[self.coord[0]-1+n][self.coord[1]-1+n]=str(self.c)
            for e in self.liste_bouton_coup_possible:
                e.place_forget()
            self.liste_bouton_coup_possible = []
            self.piece_choisi = False
            self.plateau.plajts[self.coord[0] + x - 1][self.coord[1] + y - 1] = jeton(self.plateau,self.get_coord()[0] + x - 1,self.get_coord()[1] + y - 1,self.c)

        #correspond au mouvement d'un jeton vers en bas à droite
        elif x > 0 and y > 0:
            for n in range(y):
                self.plateau.plajts[self.coord[0] + n][self.coord[1] + n].change()
                self.plateau.platxt[self.coord[0] + n][self.coord[1] + n] = str(self.c)
            for e in self.liste_bouton_coup_possible:
                e.place_forget()
            self.liste_bouton_coup_possible = []
            self.piece_choisi = False
            self.plateau.plajts[self.coord[0] + x + 1][self.coord[1] + y + 1] = jeton(self.plateau, self.get_coord()[0] + x + 1,self.get_coord()[1] + y + 1, self.c)

        #correspond au mouvement d'un jeton vers en bas à gauche
        elif x < 0 and y> 0:
            for n in range(-1,x-1,-1):
                for m in range(y):
                    self.plateau.plajts[self.coord[0] - 1+n][self.coord[1] + m].change()
                    self.plateau.platxt[self.coord[0] - 1+n][self.coord[1] + m]=str(self.c)
            for e in self.liste_bouton_coup_possible:
                e.place_forget()
            self.liste_bouton_coup_possible = []
            self.piece_choisi = False
            self.plateau.plajts[self.coord[0] + x - 1][self.coord[1] + y + 1] = jeton(self.plateau,self.get_coord()[0] + x - 1,self.get_coord()[1] + y + 1, self.c)
        #correspond au mouvement d'un jeton vers en haut à droite
        elif x>0 and y<0:
            for n in range(x):
                for m in range(-1, y - 1, -1):
                    self.plateau.plajts[self.coord[0] + n][self.coord[1]-1 +m].change()
                    self.plateau.platxt[self.coord[0] + n][self.coord[1]-1 + m] = str(self.c)
            for e in self.liste_bouton_coup_possible:
                e.place_forget()
            self.liste_bouton_coup_possible = []
            self.piece_choisi = False
            self.plateau.plajts[self.coord[0] + x + 1][self.coord[1] + y - 1] = jeton(self.plateau,self.get_coord()[0] + x + 1,self.get_coord()[1] + y - 1,self.c)
        #On incrémente de 1 self.plateau.tour pour savoir le nombre de coup
        self.plateau.tour = self.plateau.tour + 1
        self.bouton_piece_possible.place_forget()
        self.plateau.placer_bouton_piece_possible()
        affichage_nbr_coup = Label(fenetre,font=("Times",14,"bold"),bg="#FDFD96",text=self.plateau.tour)
        affichage_nbr_coup.place(x=600,y=150)
        self.affichage_nbr_jeton_noir.place(x=600,y=300)
        self.affichage_nbr_jeton_blanc.place(x=600,y=400)

    #Création d'accesseurs utiles
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

    #Méthode place qui utilise verifieplace pour placer des boutons qui permettront aux joueurs de jouer le coup qu'ils
    # souhaitent,comme j'utilise des boutons, le changement de couleur se fait après appuie sur l'une des possibilités de jeu du jeton
    def place(self):
        if (jeu.verifieplace(self.get_coord()[0]-1,self.get_coord()[1]-1)) == []:
            print("rien")
        else:
            #Pour chaque coup possible (couple), je crée un bouton associé à ce coup
            for couple in jeu.verifieplace(self.get_coord()[0]-1,self.get_coord()[1]-1):
                bouton_temp = Button(Canevas,text="D",command=lambda couple=couple:self.manger(couple[0],couple[1]))
                #Si le coup possible est situé en bas du jeton
                if couple[0] == 0 and couple[1]>0 :
                    bouton_temp.place(x=(self.get_coord()[0]+couple[0])*dim+10,y=(self.get_coord()[1]+couple[1] + 1 )*dim+10)
                #Si le coup possible est situé à droite du jeton
                elif couple[0]>0 and couple[1] == 0 :
                    bouton_temp.place(x=(self.get_coord()[0] + couple[0] + 1)*dim+10, y=(self.get_coord()[1] + couple[1]) * dim+10)
                #Si le coup possible est situé en haut du jeton
                elif couple[0] == 0 and couple[1]<0:
                    bouton_temp.place(x=(self.get_coord()[0] + couple[0]) * dim+10,y=(self.get_coord()[1] + couple[1] - 1) * dim+10)
                #Si le coup possible est situé à gauche du jeton
                elif couple[0]<0 and couple[1] == 0:
                    bouton_temp.place(x=(self.get_coord()[0] + couple[0] - 1) * dim+10,y=(self.get_coord()[1] + couple[1]) * dim+10)
                #Si le coup possible est situé en haut à gauche du jeton
                elif couple[0] < 0 and couple[1] <0:
                    bouton_temp.place(x=(self.get_coord()[0] + couple[0] - 1) * dim+10,y=(self.get_coord()[1] + couple[1] - 1) * dim+10)
                #Si le coup possible est situé en haut à droite du jeton
                elif couple[0] > 0 and couple[1] < 0:
                    bouton_temp.place(x=(self.get_coord()[0] + couple[0] + 1) * dim+10,y=(self.get_coord()[1] + couple[1] - 1) * dim+10)
                #Si le coup possible est situé en bas à gauche
                elif couple[0] < 0 and couple[1] > 0:
                    bouton_temp.place(x=(self.get_coord()[0] + couple[0] - 1) * dim+10,y=(self.get_coord()[1] + couple[1] + 1) * dim+10)
                #Si le coup possible est situé en bas à droite du jeton
                else:
                    bouton_temp.place(x=(self.get_coord()[0] + couple[0] + 1) * dim+10,y=(self.get_coord()[1] + couple[1] + 1) * dim+10)
                self.liste_bouton_coup_possible.append(bouton_temp)

########################################################################################################################

#Lancement du jeu
jeu = plateau()
def jouer():
    texte_regles.place_forget()
    Bouton_demarrer.place_forget()
    Bouton_charger_partie_existante.place_forget()
    creation_plateau()
    jeu.debut()
    fenetre.config(width=850)
    texte_nbr_coup.place(x=600,y=100)

#fonction qui permet de créer le plateau 8x8
def creation_plateau():
    x1,y1,x2,y2 = 50,50,100,100
    rep = 0
    while x1 < 450 and y1 < 450 :
        Canevas.create_rectangle(x1,y1,x2,y2,outline="black",fill = "yellow")
        x1 = x1 + 50
        x2 = x2 + 50
        rep = rep + 1
        if rep == 8:
            y1 = y1 + 50
            y2 = y2 + 50
            x1 = 50
            x2 = 100
            rep = 0
#fonction pour lancer la sauvegarde
def charger_partie_existante():
    print("a")

########################################################################################################################

#Création et placement des boutons de l'accueil

Bouton_demarrer=Button(fenetre,text="Jouer une nouvelle partie",command=jouer,height=3,width=30,font=("Courier", 8, "italic"),fg="black",bg="#E4CDA7")
Bouton_demarrer.place(x=190,y=400)
Bouton_charger_partie_existante=Button(fenetre,text="Charger une partie existante",command=charger_partie_existante,height=3,width=30,font=("Courier", 8, "italic"),fg="black",bg="#E4CDA7")
Bouton_charger_partie_existante.place(x=190,y=470)

########################################################################################################################

fenetre.mainloop()