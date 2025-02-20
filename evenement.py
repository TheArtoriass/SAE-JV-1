import random
import pygame
from Objet import Objet, liste_objets
import os
import sys


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                    Systèmes de gestion d'événements
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)


# Définir le chemin personnalisé
chemin = [(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),(2,11)#biome1
          ,(2,12),(2,13),(2,14),(3,14),(3,15),(4,15),(5,15),(6,15),(7,15),(8,15),(9,15),(10,15),(11,15),(11,14),(11,13),(11,12),(11,11),(10,11),(8,11),(9,11),(8,10),(8,9),(8,8),(8,7)#biome2
          ,(8,6),(8,5),(8,4),(8,3),(9,3),(10,3),(11,3),(12,3),(13,3),(14,3),(15,3),(16,3),(16, 4), (16, 5)#biome3
          ,(16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (16, 12), (16, 13), (16, 14), (16, 15), (16, 16), (16, 17), (16, 18)]#biome4

hauteur_plateau = 20
largeur_plateau = 20
taille_case = 39
fenetre = pygame.display.set_mode((largeur_plateau * taille_case, hauteur_plateau * taille_case))


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                              Les événements
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def rencontre_amicale(joueur,ennemis):
    """
    Ajoute un objet aléatoire à la liste d'objets du joueur et affiche un événement de rencontre amicale.

    Args:
        joueur (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.
    """
    objet = random.choice(liste_objets)
    joueur.objets.append(objet)
    
    evenement = "Rencontre amicale"
    image_path = os.path.join(repertoire_script, 'img', 'evenement', 'rencontre_amicale2.jpeg')
    texte = f"Un ami vous a donné un {objet.nom} !"
    
    afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
    return f"Vous avez rencontré un ami qui vous a donné un {objet.nom} !"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def maladie(joueur,ennemis):
    """
    Enlève tous les objets du joueur, il perd et def maladie affiche un événement de maladie.

    Args:
        joueur (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.

    """
    joueur.enlever_tous_objets()
    joueur.est_vaincu()
    
    derniers_ennemis_battus = joueur.derniers_ennemis_battus
    if derniers_ennemis_battus:
        dernier_ennemi_battu = derniers_ennemis_battus[-1]
        joueur.x, joueur.y = dernier_ennemi_battu
    else:
        joueur.x, joueur.y = (2, 0) 
         
    evenement = "Maladie"
    image_path = os.path.join(repertoire_script, 'img', 'evenement', 'maladie2.jpeg')
    texte = f"Vous avez attrapé une maladie, vous etes mort !"
    afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
    return "Vous avez attrapé une maladie vous etes mort !"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def tresor_enfoui(joueur,ennemis):
    """
    Ajoute un objet "pistolet" à la liste d'objets du joueur et affiche un événement de trésor enfoui.

    Args:
        joueur (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.

    """
    objet = Objet("pistolet", "arme", 6, joueur.x, joueur.y, os.path.join(repertoire_script, 'img', 'objet', 'pistolet.jpeg'), 39)
    joueur.objets.append(objet)
    
    evenement = "Tresor enfoui"
    image_path = image_path = os.path.join(repertoire_script, 'img', 'evenement', 'tresor_enfoui2.jpeg')
    texte = f"Vous avez trouvé un pistolet enfoui dans le sol !"
    
    afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
    return "Vous avez trouvé un pistolet enfoui dans le sol !"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def vautour(joueur,ennemis):
    """
    Enlève tous les objets du joueur et ses stats pour les remettres à leur valeur depart, def vautour affiche un événement de vautour.

    Args:
        joueur (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.

    """
    joueur.enlever_tous_objets()
    joueur.est_vaincu()
    
    evenement = "Vautour"
    image_path = image_path = os.path.join(repertoire_script, 'img', 'evenement', 'vautour2.jpeg')
    texte = f"Un vautour vous a attaqué et vous a volé tous vos objets !"
    
    afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
    return "Un vautour vous a attaqué et vous a volé tous vos objets !"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def raccourci(joueur_actif,ennemis):
    """
    Déplace le joueur sur une case aléatoire du chemin et affiche un événement de raccourci.

    Args:
        joueur_actif (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.
    """
    positions_interdites = [(16, 18)] + [(ennemi.x, ennemi.y) for ennemi in ennemis]
    nouvelle_position = random.choice([pos for pos in chemin if pos not in positions_interdites])
    joueur_actif.x, joueur_actif.y = nouvelle_position
    
    evenement = "Raccourci"
    image_path = image_path = os.path.join(repertoire_script, 'img', 'evenement', 'raccourci2.jpeg')
    texte = f"Vous avez pris un autre chemin !"
    
    afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
    return "Vous avez pris un autre chemin !"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def blessure(joueur_actif,ennemis):
    """
    Enlève 4 points de vie au joueur et affiche un événement de blessure.

    Args:
        joueur_actif (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.
    """
    joueur_actif.vie -= 4
    
    if joueur_actif.vie <= 0:
            joueur_actif.enlever_tous_objets()
            joueur_actif.est_vaincu()
            derniers_ennemis_battus = joueur_actif.derniers_ennemis_battus
            
            if derniers_ennemis_battus:
                dernier_ennemi_battu = derniers_ennemis_battus[-1]
                joueur_actif.x, joueur_actif.y = dernier_ennemi_battu
            else:
                joueur_actif.x, joueur_actif.y = (2,0)
                
    evenement = "Blessure"
    image_path = image_path = os.path.join(repertoire_script, 'img', 'evenement', 'blessure2.jpeg')
    texte = f"Vous avez perdu de la vie  !"
    
    afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
    return f"Vous avez perdu 4 points de vie ! Il vous reste {joueur_actif.vie} points de vie."


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                    La classe CarteAleatoire 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class CarteAleatoire:
    def __init__(self, largeur, hauteur,image_path,taille_case,liste_objets):
        """
        Classe représentant une carte aléatoire pour un jeu.

        args:
            largeur (int): La largeur de la carte en nombre de cases.
            hauteur (int): La hauteur de la carte en nombre de cases.
            image_path (str): Le chemin d'accès à l'image de la carte.
            taille_case (int): La taille en pixels d'une case de la carte.
            liste_objets (list): Une liste d'objets à placer sur la carte.
        """
        
        self.largeur = largeur
        self.hauteur = hauteur
        if os.path.isfile(image_path):
            self.image = pygame.image.load(image_path)  # Charger l'image de l'événement
        else:
            self.image = None
              
        self.taille_case = taille_case
        self.objets = liste_objets  
        self.evenements = {
            "Rencontre amicale": rencontre_amicale,
            "Maladie": maladie, 
            "Trésor enfoui": tresor_enfoui,
            "Vautour": vautour, 
            "Raccourci": raccourci, 
            "Blessure": blessure
        }
        self.joueurs = []   # Ajouter un attribut joueurs pour stocker une liste de joueurs
        self.ennemis = []   # Ajouter une liste pour stocker les ennemis
        self.chemin = chemin
        self.occupe = {}    # Ajouter un dictionnaire pour stocker les événements placés
        self.carte = self.generer_carte()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def generer_carte(self):
        """
        Génère une carte aléatoire en plaçant des événements et des objets sur la carte.

        Returns:
            list: Une liste de tuples représentant les événements et les objets placés sur la carte.
        """
        carte = []
        evenements = list(self.evenements.keys())
        random.shuffle(evenements)      # Mélanger la liste des événements
        cases_occupees = [(ennemi.x, ennemi.y) for ennemi in self.ennemis] + \
                        [(objet.x, objet.y) for objet in self.objets] + \
                        [(16, 18), (2, 0)]  # Ajouter les coordonnées à éviter
                        
        for evenement in evenements:
            if evenement in self.occupe:    # Utiliser les coordonnées stockées si l'événement a déjà été placé
                x, y = self.occupe[evenement]
                image_path = self.get_image_path(evenement)
                carte.append((x, y, image_path, evenement))
                
            else:
                cases_libres = [(x, y) for x, y in self.chemin if (x, y) not in cases_occupees and not any(ennemi.x == x and ennemi.y == y for ennemi in self.ennemis)]
                if cases_libres:
                    
                    x, y = random.choice(cases_libres)
                    image_path = self.get_image_path(evenement)
                    cases_occupees.append((x, y))   # Ajouter la case occupée à la liste
                    carte.append((x, y, image_path, evenement))
                    self.occupe[evenement] = (x, y)     # Stocker les coordonnées de l'événement
                    
                else:
                    carte.append((None, None, None, evenement))
            # Ajouter les coordonnées des ennemis et des cases occupées par les ennemis à la liste des cases occupées
            cases_occupees += [(ennemi.x, ennemi.y) for ennemi in self.ennemis] + \
                            [(ennemi.x + dx, ennemi.y + dy) for ennemi in self.ennemis for dx, dy in ennemi.get_cases_occupees()] + \
                            [(16, 18), (2, 0),(2, 5), (2, 8),(3, 15), (8, 15), (8, 11),(8, 4), (13, 3), (16, 3),(16, 9), (16, 13), (16, 15)]  # Ajouter les coordonnées à éviter
        return carte
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Rend l'objet CarteAleatoire iterable
    def __iter__(self):
        """
        Renvoie un itérateur sur la carte.

        Returns:
            iter: Un itérateur sur la carte.
        """
        return iter(self.carte)
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #l'image de l'événement correspondant sur le plateau
    def get_image_path(self, evenement):
        """
        Renvoie le chemin d'accès à l'image correspondant à l'événement .

        Args:
            evenement (str): Le nom de l'événement.

        """
        if evenement == "Rencontre amicale":
            return os.path.join(repertoire_script, 'img', 'evenement', 'rencontre_amicale.jpeg')
        elif evenement == "Maladie":
            return os.path.join(repertoire_script, 'img', 'evenement', 'maladie.jpeg')
        elif evenement == "Trésor enfoui":
            return os.path.join(repertoire_script, 'img', 'evenement', 'tresor_enfoui.jpeg')
        elif evenement == "Vautour":
            return os.path.join(repertoire_script, 'img', 'evenement', 'vautour.jpeg')
        elif evenement == "Raccourci":
            return os.path.join(repertoire_script, 'img', 'evenement', 'raccourci.jpeg')
        elif evenement == "Blessure":
            return os.path.join(repertoire_script, 'img', 'evenement', 'blessure.jpeg')


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                   Affichage les événements sur le plateau
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def afficher_evenement(nom, image_path, texte, taille_fenetre):
    """
    Affiche un événement dans une fenêtre.

    Args:
        nom (str): Le nom de l'événement.
        image_path (str): Le chemin d'accès à l'image de l'événement.
        texte (str): Le texte à afficher avec l'événement.
        taille_fenetre (tuple): Un tuple contenant la largeur et la hauteur de la fenêtre.
    """
    pygame.init()
    chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
    font = pygame.font.Font(chemin_police, 20)
    fenetre_evenement = pygame.display.set_mode(taille_fenetre)
    pygame.display.set_caption(nom)

    # Charger l'image de fond
    image_fondflou = os.path.join(repertoire_script, 'img','interface',  'map_flou.png')
    background_image = pygame.image.load(image_fondflou)
    background_image = pygame.transform.scale(background_image, taille_fenetre)

    # Position de départ de l'image de fond
    x_background = 0

    # Vitesse de défilement
    background_speed = 3

    temps_affichage = 0     # Initialiser le temps d'affichage à 0

    while temps_affichage < 1500:   # Boucler pendant 1,5 seconde
        # Déplacer l'image de fond
        x_background -= background_speed

        # Si l'image est complètement défilée hors de l'écran, réinitialiser sa position
        if x_background <= -taille_fenetre[0]:
            x_background = 0

        # Dessiner l'image de fond avec répétition
        fenetre_evenement.blit(background_image, (x_background, 0))
        fenetre_evenement.blit(background_image, (x_background + taille_fenetre[0], 0))

        # Dessiner le texte et l'image de l'événement
        image = pygame.image.load(image_path)
        image_rect = image.get_rect()
        image_rect.center = (taille_fenetre[0] // 2, taille_fenetre[1] // 2.7)      # Descendre l'image
        
        texte_surface = font.render(texte, True, (255, 255, 255))
        texte_rect = texte_surface.get_rect()
        texte_rect.center = (taille_fenetre[0] // 2, taille_fenetre[1] // 1.2)      # Descendre le texte
        
        nom_surface = font.render(nom, True, (255, 255, 255))   # Créer une surface de texte pour le nom de l'événement
        nom_rect = nom_surface.get_rect()
        nom_rect.center = (taille_fenetre[0] // 2, taille_fenetre[1] // 1.3)    # Positionner le nom de l'événement
        
        fenetre_evenement.blit(image, image_rect)
        fenetre_evenement.blit(texte_surface, texte_rect)
        fenetre_evenement.blit(nom_surface, nom_rect)   # Mettre le nom de l'événement sur la fenêtre d'affichage

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.wait(10)
        temps_affichage += 10  # Ajouter 10 millisecondes au temps d'affichage à chaque boucle
