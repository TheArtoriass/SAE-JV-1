import pygame
import os 


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                           CLASSE JOUEUR   
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Définir le chemin personnalisé
chemin = [(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),(2,11)#biome1
          ,(2,12),(2,13),(2,14),(3,14),(3,15),(4,15),(5,15),(6,15),(7,15),(8,15),(9,15),(10,15),(11,15),(11,14),(11,13),(11,12),(11,11),(10,11),(8,11),(9,11),(8,10),(8,9),(8,8),(8,7)#biome2
          ,(8,6),(8,5),(8,4),(8,3),(9,3),(10,3),(11,3),(12,3),(13,3),(14,3),(15,3),(16,3),(16, 4), (16, 5)#biome3
          ,(16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (16, 12), (16, 13), (16, 14), (16, 15), (16, 16), (16, 17), (16, 18)]#biome4

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Joueur:
    """
    Classe représentant un joueur dans le jeu.
    """
    def __init__(self, nom, force, vie, agilite, x_depart, y_depart, image_path,taille_case):
        """
        Initialise un joueur avec ses caractéristiques.

        Args:
            nom (str): Le nom du joueur.
            force (int): La force du joueur.
            vie (int): Les points de vie du joueur.
            agilite (int): L'agilité du joueur.
            x_depart (int): La position horizontale de départ du joueur.
            y_depart (int): La position verticale de départ du joueur.
            image_path (str): Le chemin vers l'image représentant le joueur.
            taille_case (int): La taille en pixels d'une case sur le plateau.
        """
        self.nom = nom
        self.force = force
        self.vie = vie
        self.vie_max = vie
        
        self.agilite = agilite
        self.x = x_depart
        self.y = y_depart
        self.image = pygame.image.load(image_path)  # Charger l'image du joueur
        self.image = pygame.transform.scale(self.image, (taille_case, taille_case))  
        self.taille_case = taille_case
        
        self.remaining_moves = 0            # Nombre de déplacements restants
        
        self.direction_precedente = None
        self.position_precedente = None
        self.peut_combattre = True
        self.dernier_ennemi_battu = None    # Coordonnées du dernier ennemi battu 
        
        self.derniers_ennemis_battus = []   # Liste des coordonnées des derniers ennemis battus
        self.objets = []                    # Liste des objets possédés par le joueur
        
        self.force_base = force             
        self.vie_base = vie
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def deplacer(self, direction):
        """
        Déplace le joueur dans une direction donnée.

        Args:
            direction (str): La direction du déplacement ('gauche', 'droite', 'haut', 'bas').
        """
        # Vérifier si le déplacement est possible sur le chemin
        if direction == 'gauche':
            # Vérifier si la case à gauche du joueur est dans le chemin
            if (self.x - 1, self.y) in chemin:
                # Déplacer le joueur vers la gauche
                self.x -= 1
        elif direction == 'droite':
            # Vérifier si la case à droite du joueur est dans le chemin
            if (self.x + 1, self.y) in chemin:
                # Déplacer le joueur vers la droite
                self.x += 1
        elif direction == 'haut':
            # Vérifier si la case en haut du joueur est dans le chemin
            if (self.x, self.y - 1) in chemin:
                # Déplacer le joueur vers le haut
                self.y -= 1
        elif direction == 'bas':
            # Vérifier si la case en bas du joueur est dans le chemin
            if (self.x, self.y + 1) in chemin:
                # Déplacer le joueur vers le bas
                self.y += 1
                
        # Décrémenter le nombre de déplacements restants  
        self.remaining_moves -= 1
        self.direction_precedente = direction
        self.position_precedente = (self.x, self.y)
          
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
           
    def dessiner(self, surface, taille_case,num_joueur):
        """
        Dessine le joueur sur la surface donnée à sa position actuelle avec son numéro et son dernier objet (s'il en a un).

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner le joueur.
            taille_case (int): La taille d'une case en pixels.
            num_joueur (int): Le numéro du joueur à afficher.
        """
        # Afficher l'image du joueur à sa position actuelle
        surface.blit(self.image, (self.x * taille_case, self.y * taille_case))
        
        # Définir la police et la couleur du texte
        chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
        font = pygame.font.Font(chemin_police, 17)
        white = (255, 255, 255)
        
        # Afficher le numéro du joueur au-dessus de son image
        text_surface = font.render(f"J{num_joueur}", True, white)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.x * taille_case + taille_case // 2, self.y * taille_case + 10)
        surface.blit(text_surface, text_rect)
        
        # Afficher le dernier objet ajouté au joueur, s'il en a un
        if self.objets:
            objet = self.objets[-1]
            font = pygame.font.Font(chemin_police, 10)
            
            if objet.type_objet == "soins" or objet.type_objet == "armure" :
                text_surface = font.render(f"+{objet.bonus} vie ({objet.nom})", True, white)
            elif objet.type_objet == "arme":
                text_surface = font.render(f"+{objet.bonus} force ({objet.nom})", True, white)
                
            text_rect = text_surface.get_rect()
            text_rect.midtop = (self.x * taille_case + taille_case // 2, self.y * taille_case + 30)
            surface.blit(text_surface, text_rect)
            

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def prendre_objet(self, objet):
        """
        Ajoute un objet à l'inventaire du joueur et applique ses effets.

        Args:
            objet (Objet): L'objet à ajouter à l'inventaire du joueur.
        """
        # Ajouter l'objet à l'inventaire du joueur
        self.objets.append(objet)
        
        # Si l'objet est de type "soins", augmenter la vie du joueur
        if objet.type_objet == 'soins':
            self.vie += objet.bonus
            if self.vie > self.vie_max:
                self.vie = self.vie_max
                
        # Si l'objet est de type "armure", augmenter la vie maximale et la vie du joueur
        elif objet.type_objet == 'armure':
            self.vie_max += objet.bonus
            self.vie += objet.bonus
            
        # Si l'objet est de type "arme", augmenter la force du joueur
        elif objet.type_objet == 'arme':
            self.force += objet.bonus
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def est_vaincu(self):
        """
        Réinitialise les statistiques du joueur et le replace à sa position précédente s'il est vaincu.
        """
        self.reset_stats()
        self.x, self.y = self.position_precedente
        if self.vie <= 0:
            self.peut_combattre = False
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def ajouter_objet(self, objet):
        """
        Ajoute un objet au joueur.

        Args:
            objet (Objet): L'objet à ajouter.
        """
        if self.objets:
            self.objets.pop()
        self.objets.append(objet)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def enlever_tous_objets(self):
        """
        Enlève tous les objets du joueur.
        """
        self.objets = []

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def reset_stats(self):
        """
        Réinitialise les statistiques du joueur à leurs valeurs par défaut.
        """
        self.force = self.force_base
        self.vie_max = self.vie_base
        self.vie = self.vie_max
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                   Création des classes de joueurs 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
class Joueur1(Joueur):
    """
    Classe représentant un joueur de la classe Force.
    """
    def __init__(self, x_depart, y_depart,taille_case):
        """
        Args:
            x_depart (int): La position horizontale de départ du joueur sur le plateau.
            y_depart (int): La position verticale de départ du joueur sur le plateau.
            taille_case (int): La taille d'une case du plateau.
        """
        super().__init__('Force', 4, 12, 3, x_depart, y_depart, os.path.join(repertoire_script, 'img', 'personne', 'Joueur1.jpeg'),taille_case)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Joueur2(Joueur):
    """
    Classe représentant un joueur de la classe Vie.
    """
    def __init__(self, x_depart, y_depart,taille_case):
        """
        Args:
            x_depart (int): La position horizontale de départ du joueur sur le plateau.
            y_depart (int): La position verticale de départ du joueur sur le plateau.
            taille_case (int): La taille d'une case du plateau.
        """
        super().__init__('Vie', 3, 15, 2, x_depart, y_depart,  os.path.join(repertoire_script, 'img', 'personne', 'Joueur2.jpeg'),taille_case)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Joueur3(Joueur):
    """
    Classe représentant un joueur de la classe Polyvalent.
    """
    def __init__(self, x_depart, y_depart,taille_case):
        """
        Args:
            x_depart (int): La position horizontale de départ du joueur sur le plateau.
            y_depart (int): La position verticale de départ du joueur sur le plateau.
            taille_case (int): La taille d'une case du plateau.
        """
        super().__init__('Polyvalent', 6, 8, 6, x_depart, y_depart, os.path.join(repertoire_script, 'img', 'personne', 'Joueur3.jpeg'),taille_case)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Joueur4(Joueur):
    """
    Classe représentant un joueur de la classe Agilité.
    """
    def __init__(self, x_depart, y_depart,taille_case):
        """
        Args:
            x_depart (int): La position horizontale de départ du joueur sur le plateau.
            y_depart (int): La position verticale de départ du joueur sur le plateau.
            taille_case (int): La taille d'une case du plateau.
        """
        super().__init__('Agilité', 3, 12, 4, x_depart, y_depart,  os.path.join(repertoire_script, 'img', 'personne', 'Joueur4.jpeg'),taille_case)