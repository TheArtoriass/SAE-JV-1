import pygame
import os   


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                       CLASSE OBJET  
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)
taille_case = 39

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Objet:
    """
    Classe représentant un objet sur le plateau.
    """
    def __init__(self, nom, type_objet, bonus, x, y, image_path,taille_case):
        """
        Initialise un nouvel objet.

        Args:
            nom (str): Le nom de l'objet.
            type_objet (str): Le type de l'objet ('soins', 'arme' ou 'armure').
            bonus (int): Le bonus que l'objet confère au joueur.
            x (int): La position x de l'objet sur le plateau.
            y (int): La position y de l'objet sur le plateau.
            image_path (str): Le chemin d'accès à l'image de l'objet.
            taille_case (int): La taille d'une case sur le plateau.
        """
        self.nom = nom
        self.type_objet = type_objet
        self.bonus = bonus
        self.x = x
        self.y = y
        self.image_path = image_path
        self.image = pygame.image.load(image_path)  # Charger l'image du joueur
        self.image = pygame.transform.scale(self.image, (taille_case, taille_case))  
        self.taille_case = taille_case
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def dessiner(self, surface, taille_case):
        """
        Dessine l'objet sur la surface donnée.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner l'objet.
            taille_case (int): La taille d'une case sur le plateau.
        """
        image = pygame.image.load(self.image_path)
        image = pygame.transform.scale(image, (taille_case, taille_case))
        surface.blit(image, (self.x * taille_case, self.y * taille_case))
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                               Création d'une liste d'objets 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Création d'une liste d'objets avec des chemins d'accès aux images relatives

liste_objets = [
    Objet("bandage", "soins", 2, 6, 15, os.path.join(repertoire_script, 'img', 'objet', 'bandage.jpeg'), taille_case),
    Objet("trousse de soin", "soins", 4, 8, 8, os.path.join(repertoire_script, 'img', 'objet', 'kit.jpeg'), taille_case),
    Objet("pistolet", "arme", 6, 11, 15, os.path.join(repertoire_script, 'img', 'objet', 'pistolet.jpeg'), taille_case),
    Objet("gants de boxe", "arme", 2, 12, 3, os.path.join(repertoire_script, 'img', 'objet', 'gantsboxe.jpeg'), taille_case),
    Objet("médicaments", "soins", 3, 9, 3, os.path.join(repertoire_script, 'img', 'objet', 'medoc.jpeg'), taille_case),
    Objet("pelle", "arme", 3, 2, 9, os.path.join(repertoire_script, 'img', 'objet', 'pelle.jpeg'), taille_case),
    Objet("masque à gaz", "armure", 2, 16, 10, os.path.join(repertoire_script, 'img', 'objet', 'smoke.jpeg'), taille_case),
    Objet("casque", "armure", 5, 16, 4, os.path.join(repertoire_script, 'img', 'objet', 'casque.jpeg'), taille_case),
    Objet("grolles renforcées", "armure", 3, 2, 4, os.path.join(repertoire_script, 'img', 'objet', 'grolle.jpeg'), taille_case),
]
