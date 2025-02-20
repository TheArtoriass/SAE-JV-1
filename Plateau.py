import pygame
import os
from Objet import liste_objets
from evenement import CarteAleatoire
from evenement import  rencontre_amicale, maladie, tresor_enfoui, vautour, raccourci, blessure

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                       CLASSE PLATEAU  
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Définir le chemin personnalisé
chemin = [(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),(2,11)#biome1
          ,(2,12),(2,13),(2,14),(3,14),(3,15),(4,15),(5,15),(6,15),(7,15),(8,15),(9,15),(10,15),(11,15),(11,14),(11,13),(11,12),(11,11),(10,11),(8,11),(9,11),(8,10),(8,9),(8,8),(8,7)#biome2
          ,(8,6),(8,5),(8,4),(8,3),(9,3),(10,3),(11,3),(12,3),(13,3),(14,3),(15,3),(16,3),(16, 4), (16, 5)#biome3
          ,(16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (16, 12), (16, 13), (16, 14), (16, 15), (16, 16), (16, 17), (16, 18)]#biome4

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Plateau:
    def __init__(self, largeur, hauteur, taille_case):
        """
        Initialise un nouveau plateau de jeu.

        Args:
            largeur (int): La largeur du plateau en nombre de cases.
            hauteur (int): La hauteur du plateau en nombre de cases.
            taille_case (int): La taille d'une case en pixels.
        """
        
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_case = taille_case
        self.grille = [[None for _ in range(largeur)] for _ in range(hauteur)]
        self.surface = pygame.Surface((largeur * taille_case, hauteur * taille_case))
        
        self.joueurs = []   # Ajouter une liste pour stocker les joueurs
        self.ennemis = []   # Ajouter une liste pour stocker les ennemis
        self.objets = []    # Ajouter une liste pour stocker les objets
        self.carte = CarteAleatoire(largeur, hauteur, taille_case, chemin, liste_objets)
        
        self.evenements = {
            "Rencontre amicale": rencontre_amicale, 
            "Maladie": maladie, 
            "Trésor enfoui": tresor_enfoui,
            "Vautour": vautour, 
            "Raccourci": raccourci, 
            "Blessure": blessure
            
        }
        self.liste_objets = liste_objets
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_case(self, x, y):
        """
        Renvoie la case à la position (x, y) sur le plateau.

        Args:
            x (int): La position x de la case.
            y (int): La position y de la case.
        """
        return self.grille[y][x]

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def dessiner(self):
        """
        Dessine le plateau.
        """
        self.surface.fill((255, 255, 255))
        
        # Charger l'image de la carte et la redimensionner pour qu'elle s'adapte au plateau
        image_path = os.path.join(repertoire_script, 'img','interface', 'map.png')
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (self.largeur * self.taille_case, self.hauteur * self.taille_case))
        
        # Dessiner l'image redimensionnée sur la surface du plateau
        self.surface.blit(image, (0, 0))
        
        # Dessiner le chemin sur la surface du plateau
        for x, y in chemin:
            pygame.draw.rect(self.surface, (0, 0, 0), (x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case), 1)
        
        # Dessiner les événements sur la surface du plateau
        carte = self.carte.generer_carte()
        for x, y, image_path, evenement in carte:
            if evenement and (x, y) not in [(ennemi.x, ennemi.y) for ennemi in self.ennemis]:
                image = pygame.image.load(self.carte.get_image_path(evenement))
                image = pygame.transform.scale(image, (self.taille_case, self.taille_case))
                self.surface.blit(image, (x * self.taille_case, y * self.taille_case))
        
        # Dessiner les joueurs sur la surface du plateau
        for i, joueur in enumerate(self.joueurs):
            joueur.dessiner(self.surface, self.taille_case, i + 1)
            
        # Dessiner les ennemis sur la surface du plateau
        for ennemi in self.ennemis:
            ennemi.dessiner(self.surface)
        
        # Dessiner les objets sur la surface du plateau
        for objet in self.objets:
            x, y = objet.x * self.taille_case, objet.y * self.taille_case
            image = pygame.image.load(objet.image_path)
            image = pygame.transform.scale(image, (self.taille_case, self.taille_case))
            self.surface.blit(image, (x, y))
            
        

        return self.surface
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def ajouter_ennemi(self, ennemi):
        """
        Ajoute un ennemi à la liste des ennemis sur le plateau.

        Args:
            ennemi (Ennemis): L'ennemi à ajouter.
        """
        self.ennemis.append(ennemi)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def ajouter_objet(self, objet):
        """
        Ajoute un objet à la liste des objets sur le plateau.

        Args:
            objet (Objet): L'objet à ajouter.
        """
        self.objets.append(objet)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def enlever_objet(self, objet):
        """
        Enlève un objet de la liste des objets sur le plateau.

        Args:
            objet (Objet): L'objet à enlever.
        """
        self.objets.remove(objet)
