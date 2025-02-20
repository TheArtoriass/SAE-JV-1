import pygame
import os

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                       CLASSE ENNEMIS
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)
taille_case = 39

class Ennemis:
    """
    Classe représentant un ennemi dans le jeu.
    """
    def __init__(self, nomE, forceE, vieE, agiliteE, x_departE, y_departE, image_path,taille_case):
        """
        Initialise une instance de la classe Ennemis.

        Args:
            nomE (str): Le nom de l'ennemi.
            forceE (int): La force de l'ennemi.
            vieE (int): Les points de vie de l'ennemi.
            agiliteE (int): L'agilité de l'ennemi.
            x_departE (int): La position en x de départ de l'ennemi sur le plateau.
            y_departE (int): La position en y de départ de l'ennemi sur le plateau.
            image_path (str): Le chemin de l'image de l'ennemi.
            taille_case (int): La taille en pixels d'une case sur le plateau.
        """
        self.nomE = nomE
        self.forceE = forceE
        self.vieE = vieE
        self.agiliteE = agiliteE
        self.x = x_departE
        self.y = y_departE
        self.image = pygame.image.load(image_path)                                      # Charger l'image du joueur
        self.image = pygame.transform.scale(self.image, (taille_case, taille_case))     # Redimensionner l'image
        
        self.taille_case = taille_case
        self.vieEMax = vieE
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    def dessiner(self, surface):
            """
            Dessine l'ennemi sur la surface donnée.

            Args:
                surface (pygame.Surface): La surface sur laquelle dessiner l'ennemi.
            """
            surface.blit(self.image, (self.x * self.taille_case, self.y * self.taille_case))
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
    def get_cases_occupees(self):
        """
        Renvoie une liste contenant les coordonnées de la case occupée par l'ennemi.

        Returns:
            list: Une liste contenant un tuple de deux entiers représentant les coordonnées de la case occupée par l'ennemi.
        """
        return [(self.x, self.y)]    

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                   Création d'une liste d'ennemis 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


liste_ennemis = [
    Ennemis("Rat infecté", 0, 6, 0, 2, 5, os.path.join(repertoire_script, 'img', 'ennemis', 'Rat_infecte.jpeg'), taille_case),
    Ennemis("Rat infecté", 0, 6, 0, 2, 8, os.path.join(repertoire_script, 'img', 'ennemis', 'Rat_infecte.jpeg'), taille_case),

    Ennemis("Loup infecté ", 0, 8, 0, 3, 15, os.path.join(repertoire_script, 'img', 'ennemis', 'loup.jpeg'), taille_case),
    Ennemis("Loup infecté ", 0, 8, 0, 8, 15, os.path.join(repertoire_script, 'img', 'ennemis', 'loup2.jpeg'), taille_case),
    Ennemis("Loup infecté ", 0, 8, 0, 8, 11, os.path.join(repertoire_script, 'img', 'ennemis', 'loup3.jpeg'), taille_case),

    Ennemis("Infecté", 0, 10, 0, 8, 4, os.path.join(repertoire_script, 'img', 'ennemis', 'Infecte.jpeg'), taille_case),
    Ennemis("Infecté", 0, 10, 0, 13, 3, os.path.join(repertoire_script, 'img', 'ennemis', 'Infecte.jpeg'), taille_case),
    Ennemis("Infecté", 0, 10, 0, 16, 3, os.path.join(repertoire_script, 'img', 'ennemis', 'Infecte.jpeg'), taille_case),

    Ennemis("Mutant ", 0, 13, 0, 16, 9, os.path.join(repertoire_script, 'img', 'ennemis', 'Mutant.jpeg'), taille_case),
    Ennemis("Mutant ", 0, 13, 0, 16, 13, os.path.join(repertoire_script, 'img', 'ennemis', 'Mutant.jpeg'), taille_case),
    Ennemis("Mutant ", 0, 13, 0, 16, 15, os.path.join(repertoire_script, 'img', 'ennemis', 'Mutant.jpeg'), taille_case),
]




