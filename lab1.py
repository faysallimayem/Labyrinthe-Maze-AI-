import random
import matplotlib.pyplot as plt
import numpy as np 
from collections import deque
from pyamaze import maze,agent


class Pile:
    
    def __init__(self):
        self.lst = []

    def est_vide(self):
       return self.lst == []

    def empiler(self, x):
        self.lst.append(x)

    def depiler(self):
        if self.est_vide():
            raise ValueError("Pile vide")
        return self.lst.pop()


class Case:
    def __init__(self):
        self.N = False
        self.W = False
        self.S = False
        self.E = False


class Labyrinthe:
    def __init__(self, p, q):
        self.nb_lignes = p
        self.nb_colonnes = q
        self.tab = [[Case() for j in range(q)] for i in range(p)]
        self.graph = {}  

    def creer(self):
        pile = Pile()
        dejavu = [[False for j in range(self.nb_colonnes)] for i in range(self.nb_lignes)]
        i, j = random.randint(0, self.nb_lignes - 1), random.randint(0, self.nb_colonnes - 1)
        pile.empiler((i, j))
        dejavu[i][j] = True
        while not pile.est_vide():
            (i, j) = pile.depiler()
            v = []
            if j < self.nb_colonnes - 1 and not dejavu[i][j + 1]:
                v.append('E')
            if i > 0 and not dejavu[i - 1][j]:
                v.append('N')
            if j > 0 and not dejavu[i][j - 1]:
                v.append('W')
            if i < self.nb_lignes - 1 and not dejavu[i + 1][j]:
                v.append('S')
            if len(v) > 1:
                pile.empiler((i, j))
            if len(v) > 0:
                c = v[random.randint(0, len(v) - 1)]
                if c == 'N':
                    self.tab[i][j].N = True
                    self.tab[i - 1][j].S = True
                    dejavu[i - 1][j] = True
                    pile.empiler((i - 1, j))
                elif c == 'W':
                    self.tab[i][j].W = True
                    self.tab[i][j - 1].E = True
                    dejavu[i][j - 1] = True
                    pile.empiler((i, j - 1))
                elif c == 'S':
                    self.tab[i][j].S = True
                    self.tab[i + 1][j].N = True
                    dejavu[i + 1][j] = True
                    pile.empiler((i + 1, j))
                else:
                    self.tab[i][j].E = True
                    self.tab[i][j + 1].W = True
                    dejavu[i][j + 1] = True
                    pile.empiler((i, j + 1))

                
                if (i, j) not in self.graph:
                    self.graph[(i, j)] = set()
                if c == 'N':
                    self.graph[(i, j)].add((i - 1, j))
                elif c == 'W':
                    self.graph[(i, j)].add((i, j - 1))
                elif c == 'S':
                    self.graph[(i, j)].add((i + 1, j))
                else:
                    self.graph[(i, j)].add((i, j + 1))

    def ajouterNoeud(self, node):
        
        if node not in self.graph:
            self.graph[node] = set()

    def ajouterArc(self, node1, node2):
        
        if node1 in self.graph and node2 in self.graph:
            self.graph[node1].add(node2)

    def listerNoeuds(self):
        
        return list(self.graph.keys())

    def listerArcs(self):
        
        arcs = []
        for node in self.graph:
            for neighbor in self.graph[node]:
                arcs.append((node, neighbor))
        return arcs

    def afficherGraphe(self):
      
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        
        for node in self.graph:
            ax.plot(node[1], -node[0], '.', markersize=8)  
            for neighbor in self.graph[node]:
                ax.plot([node[1], neighbor[1]], [-node[0], -neighbor[0]], 'b-')  

        ax.set_xlim(0, self.nb_colonnes)
        ax.set_ylim(-self.nb_lignes, 0)  
        ax.set_xticks(np.arange(0, self.nb_colonnes + 1, 1))
        ax.set_yticks(np.arange(0, -self.nb_lignes - 1, -1))
        ax.grid(True)
        ax.axis('on')

    plt.show()

    def afficherLabyrinthe(self):
        
        cell_size = 1.0  
        wall_width = 0.9  

       
        fig, ax = plt.subplots()
        ax.set_aspect('equal')  

        
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                if not self.tab[i][j].N:
                    ax.plot([j, j + 1], [self.nb_lignes - i, self.nb_lignes - i], 'black', linewidth=wall_width)  
                if not self.tab[i][j].W:
                    ax.plot([j, j], [self.nb_lignes - i, self.nb_lignes - (i + 1)], 'black', linewidth=wall_width)  
                if not self.tab[i][j].S and i == self.nb_lignes - 1:
                    ax.plot([j, j + 1], [self.nb_lignes - (i + 1), self.nb_lignes - (i + 1)], 'black', linewidth=wall_width)  
                if not self.tab[i][j].E and j == self.nb_colonnes - 1:
                    ax.plot([j + 1, j + 1], [self.nb_lignes - i, self.nb_lignes - (i + 1)], 'black', linewidth=wall_width) 

        
        ax.set_xlim(-0.5, self.nb_colonnes - 0.5)
        ax.set_ylim(-0.5, self.nb_lignes- 0.5)
        ax.axis('off')  

        
        plt.show()
    

    def successeurs(self, etat_courant, explores, accessibles):
        

        
        successeurs_valides = []

        
        i, j = etat_courant

        
        if self.tab[i][j].N and (i - 1, j) not in explores and (i - 1, j) not in accessibles:
            successeurs_valides.append((i - 1, j))
        if self.tab[i][j].W and (i, j - 1) not in explores and (i, j - 1) not in accessibles:
            successeurs_valides.append((i, j - 1))
        if self.tab[i][j].S and (i + 1, j) not in explores and (i + 1, j) not in accessibles:
            successeurs_valides.append((i + 1, j))
        if self.tab[i][j].E and (i, j + 1) not in explores and (i, j + 1) not in accessibles:
            successeurs_valides.append((i, j + 1))

        return successeurs_valides

    

    def VerifEtat(self, etat, explores, accessibles):
        
        if etat in explores or etat in accessibles:
            return True
        else:
            return False

    def recherche_profondeur(self, etat_initial, etat_final):
        

        
        pile = deque()
        pile.append(etat_initial)
        explores = {}
        accessibles = {etat_initial: 1}  
        chemin_trouve = []

        while pile:
            etat_courant = pile.pop()
            
            if etat_courant == etat_final:
                chemin_trouve = self.reconstruire_chemin(explores, etat_initial, etat_final)
                return chemin_trouve  
            
            successeurs = self.successeurs(etat_courant, explores, accessibles)

            
            for successeur in successeurs:
                if successeur not in explores and successeur not in accessibles:
                    pile.append(successeur)
                    accessibles[successeur] = len(accessibles) + 1  

            
            explores[etat_courant] = True

        return chemin_trouve  

    def reconstruire_chemin(self, explores, etat_initial, etat_final):
        """ Reconstruit le chemin trouvé à partir des états explorés """

        chemin = []
        etat = etat_final

        while etat != etat_initial:
            chemin.append(etat)
            if etat in explores:
                etat = explores[etat]
            else:
            
                break

        chemin.append(etat_initial)
        chemin.reverse()  
        return chemin



    def recherche_profondeur_iterative_limite(self, etat_initial, etat_final, max_profondeur):
        

        for profondeur_max in range(max_profondeur + 1):
            if self._dfs_limite(etat_initial, etat_final, profondeur_max):
                return True  

        return False  

    def _dfs_limite(self, etat_courant, etat_final, profondeur_max):
        

        pile = deque([(etat_courant, 0)])  
        explores = set()  

        while pile:
            etat, profondeur = pile.pop()

            
            if etat == etat_final:
                return True  

            
            if profondeur < profondeur_max:
                
                successeurs = self.successeurs(etat)

                
                for successeur in successeurs:
                    if successeur not in explores:
                        pile.append((successeur, profondeur + 1))
                        explores.add(successeur)

        return False  

    def recherche_bidirectionnelle(self, etat_initial, etat_final):
        

        
        file_depart = deque([etat_initial])  
        file_arrivee = deque([etat_final])   
        explores_depart = set()              
        explores_arrivee = set()             

        while file_depart and file_arrivee:
           
            if self._explorer_direction(file_depart, explores_depart, explores_arrivee):
                return True  

           
            if self._explorer_direction(file_arrivee, explores_arrivee, explores_depart):
                return True  

        return False  

    def _explorer_direction(self, file, explores_source, explores_cible):
        

        etat_courant = file.popleft()

        
        if etat_courant in explores_cible:
            return True  

        
        successeurs = self.successeurs(etat_courant)

        
        for successeur in successeurs:
            if successeur not in explores_source:
                file.append(successeur)
                explores_source.add(successeur)

        return False  




    def successeurs1(self, etat):
        
        i, j = etat
        successeurs = []
        if self.tab[i][j].N:
            successeurs.append((i - 1, j))
        if self.tab[i][j].W:
            successeurs.append((i, j - 1))
        if self.tab[i][j].S:
            successeurs.append((i + 1, j))
        if self.tab[i][j].E:
            successeurs.append((i, j + 1))

    def afficher_chemin(self, chemin, etat_initial, etat_final):
        
        labyrinthe_chemin = [[self._get_tile_representation(i, j) for j in range(self.nb_colonnes)] for i in range(self.nb_lignes)]

        
        for etat in chemin:
            i, j = etat
            labyrinthe_chemin[i][j] = 'X'  

        labyrinthe_chemin[etat_initial[0]][etat_initial[1]] = 'D'

        labyrinthe_chemin[etat_final[0]][etat_final[1]] = 'A'

        
        cell_size = 1.0  
        wall_width = 0.9  

        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                if 'N' in labyrinthe_chemin[i][j]:
                    ax.plot([j, j + 1], [self.nb_lignes - i, self.nb_lignes - i], 'black', linewidth=wall_width)  
                if 'W' in labyrinthe_chemin[i][j]:
                    ax.plot([j, j], [self.nb_lignes - i, self.nb_lignes - (i + 1)], 'black', linewidth=wall_width)  
                if 'S' in labyrinthe_chemin[i][j] and i == self.nb_lignes - 1:
                    ax.plot([j, j + 1], [self.nb_lignes - (i + 1), self.nb_lignes - (i + 1)], 'black', linewidth=wall_width)  
                if 'E' in labyrinthe_chemin[i][j] and j == self.nb_colonnes - 1:
                    ax.plot([j + 1, j + 1], [self.nb_lignes - i, self.nb_lignes - (i + 1)], 'black', linewidth=wall_width)  

                if labyrinthe_chemin[i][j] == 'X':
                    ax.fill([j, j + 1, j + 1, j], [self.nb_lignes - i, self.nb_lignes - i, self.nb_lignes - (i + 1), self.nb_lignes - (i + 1)], 'yellow')  
                elif labyrinthe_chemin[i][j] == 'D':
                    ax.fill([j, j + 1, j + 1, j], [self.nb_lignes - i, self.nb_lignes - i, self.nb_lignes - (i + 1), self.nb_lignes - (i + 1)], 'green')  
                elif labyrinthe_chemin[i][j] == 'A':
                    ax.fill([j, j + 1, j + 1, j], [self.nb_lignes - i, self.nb_lignes - i, self.nb_lignes - (i + 1), self.nb_lignes - (i + 1)], 'red')  

        ax.set_xlim(-0.5, self.nb_colonnes - 0.5)
        ax.set_ylim(-0.5, self.nb_lignes - 0.5)
        ax.axis('off')

        plt.show()

    def _get_tile_representation(self, i, j):
        

        tile = ""

        if not self.tab[i][j].N:
            tile += 'N'
        if not self.tab[i][j].W:
            tile += 'W'
        if not self.tab[i][j].S and i == self.nb_lignes - 1:
            tile += 'S'
        if not self.tab[i][j].E and j == self.nb_colonnes - 1:
            tile += 'E'

        return tile


p = 10
q = 10


labyrinthe = Labyrinthe(p, q)
labyrinthe.creer()
etat_initial = (0, 0)
etat_final = (p - 1, q - 1)
chemin_trouve = labyrinthe.recherche_profondeur(etat_initial, etat_final)
if chemin_trouve:
    print("Chemin trouvé !")
    labyrinthe.afficher_chemin(chemin_trouve, etat_initial, etat_final)
    m=maze(10,10)
    m.CreateMaze(theme="light")
    a=agent(m,footprints=True,shape="Point")
    m.tracePath({a:m.path})
    m.run()
else:
    print("Aucun chemin trouvé.")
labyrinthe.afficherGraphe()
labyrinthe.afficherLabyrinthe()
labyrinthe.ajouterNoeud((1, 1))
labyrinthe.ajouterArc((1, 1), (2, 2))
    
print("Liste des nœuds du graphe :")
print(labyrinthe.listerNoeuds())


print("Liste des arcs du graphe :")
print(labyrinthe.listerArcs())


