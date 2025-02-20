import pygame
from Joueur import Joueur1, Joueur2, Joueur3, Joueur4
import tkinter.simpledialog
import sys
import os


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                               Systèmes de gestion des interfaces qui n'ont pas de lien trés rapproché avec les autres fichiers
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


hauteur_plateau = 20
largeur_plateau = 20

LARGEUR_ECRAN = 780
HAUTEUR_ECRAN = 780

taille_case = 39
fenetre = pygame.display.set_mode((largeur_plateau * taille_case, hauteur_plateau * taille_case))

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def afficher_resultat_de(resultat_de):
    """
    Affiche le résultat d'un lancer de dé dans la fenêtre Pygame.

    Args:
        resultat_de (int): Le résultat du lancer de dé.
    """
    
    taille_fenetre = (largeur_plateau * taille_case, hauteur_plateau * taille_case)
    fenetre_evenement = pygame.display.set_mode(taille_fenetre)
    
    # Définition de la police de caractères pour le texte
    chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
    font = pygame.font.Font(chemin_police, 120)
    NOIR = (0, 0, 0)
    texte = font.render(f"{resultat_de}", True, NOIR)

    # Charger l'image de fond
    image_fondflou = os.path.join(repertoire_script, 'img','interface',  'map_flou.png')
    background_image = pygame.image.load(image_fondflou)
    background_image = pygame.transform.scale(background_image, taille_fenetre)

    # Charger l'image du dé
    image_fond_de = os.path.join(repertoire_script, 'img','interface', 'interface_de.jpeg')
    dice_image = pygame.image.load(image_fond_de).convert_alpha()
    dice_image = pygame.transform.scale(dice_image, (dice_image.get_width() * 1.5, dice_image.get_height() * 1.5))

    # Position de départ de l'image de fond
    x_background = 0

    # Vitesse de défilement
    background_speed = 1.5

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

        # Dessiner l'image du dé
        fenetre_evenement.blit(dice_image, (fenetre_evenement.get_width() // 2 - dice_image.get_width() // 2, fenetre_evenement.get_height() // 2 - dice_image.get_height() // 2))
        
        # Centrer le texte sur l'écran
        texte_rect = texte.get_rect(center=(fenetre_evenement.get_width() // 2, fenetre_evenement.get_height() // 2 + 150))
        fenetre_evenement.blit(texte, texte_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        temps_affichage += 10   # Ajouter 10 millisecondes au temps d'affichage à chaque boucle

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                
def choisir_classe():
    """
    Affiche les statistiques des classes de personnages ( stats_perso ) et demande à l'utilisateur de choisir une classe.

    Returns:
        La classe de personnage choisie par l'utilisateur.
    """
    
    Force = '           force: 4, vie: 12, agilite: 3'
    Vie = '              force: 3, vie: 15, agilite: 2'
    Polyvalent = '  force: 6 , vie: 8 , agilite: 6'
    Agilité = '         force: 3, vie: 12, agilite: 4'
    
    classe = tkinter.simpledialog.askinteger("Choix de classe", "Choisissez la classe de votre personnage \n \n 1  - Force:" + Force + "\n 2 - Vie:  " + Vie + "\n 3 - Polyvalent: " + Polyvalent + "\n 4 - Agilité: " + Agilité + "\n ", minvalue=1, maxvalue=4)
    if classe == 1:
        return Joueur1
    elif classe == 2:
        return Joueur2
    elif classe == 3:
        return Joueur3
    elif classe == 4:
        return Joueur4
    else:
        return pygame.quit() ,sys.exit()   # Quitter le jeu
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
def choisir_personnages():
    """
    Demande à l'utilisateur de choisir le nombre de joueur , pour aprés choisir sa classe.

    Returns:
        Une liste de la classe Joueur correspondant aux personnages choisis.
    """
    
    # Charger l'image de fond
    image_fond = pygame.image.load(os.path.join(repertoire_script, 'img','interface',  'map_flou.png'))

    # Redimensionner l'image de fond pour qu'elle corresponde à la taille de la fenêtre
    image_fond = pygame.transform.scale(image_fond, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

    # Afficher l'image de fond
    fenetre.blit(image_fond, (0, 0))
    pygame.display.flip()
    
    
    nombre_joueurs = tkinter.simpledialog.askinteger("Nombre de joueurs", "Entrez le nombre de joueurs (entre 1 et 4):", minvalue=1, maxvalue=4)
    if nombre_joueurs is None:              # Si l'utilisateur a appuyé sur "Cancel"
        return  pygame.quit() ,sys.exit()   # Quitter le jeu
    joueurs = []

    for i in range(nombre_joueurs):
        classe = choisir_classe()
        if classe is not None:
            x_depart = 2
            y_depart = 0
            joueur = classe(x_depart, y_depart, taille_case)
            joueurs.append(joueur)

    return joueurs
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def message_interface(joueur_index,de_restant):
    """
    Affiche l'interface de jeu avec les informations du joueur actuel et le nombre de déplacements restants.

    Args:
        joueur_index (int): L'index du joueur actuel.
        de_restant (int): Le nombre de déplacements restants pour le joueur actuel.
    """
    
    Jaune = (255, 255, 0)
    blanc_cassé = (223, 242, 255)
    
    # Afficher le joueur actuel en haut de la fenêtre
    chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
    font = pygame.font.Font(chemin_police, 36)
    message_joueur = font.render(f"Joueur {joueur_index+1} joue", True, Jaune)
    message_joueur_rect = message_joueur.get_rect(center=(largeur_plateau * taille_case // 2, 50))
    fenetre.blit(message_joueur, message_joueur_rect)
    
    
    # Afficher un message "Appuyez sur ESPACE pour lancer le dé" juste au-dessus du texte "Joueur n joue"
    chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
    font = pygame.font.Font(chemin_police, 20)
    message = font.render("Appuyez sur ESPACE pour lancer le dé", True, blanc_cassé)
    message_rect = message.get_rect(center=(largeur_plateau * taille_case // 2, 100))
    fenetre.blit(message, message_rect)

    
    # Afficher des emojis flèches
    emoji_gauche = font.render("←", True, blanc_cassé)
    emoji_gauche_rect = emoji_gauche.get_rect(center=(largeur_plateau * taille_case // 2 - 50, hauteur_plateau * taille_case - 60))
    fenetre.blit(emoji_gauche, emoji_gauche_rect)

    emoji_droite = font.render("→", True, blanc_cassé)
    emoji_droite_rect = emoji_droite.get_rect(center=(largeur_plateau * taille_case // 2 + 50, hauteur_plateau * taille_case - 60))
    fenetre.blit(emoji_droite, emoji_droite_rect)

    emoji_haut = font.render("↑", True, blanc_cassé)
    emoji_haut_rect = emoji_haut.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case - 80))
    fenetre.blit(emoji_haut, emoji_haut_rect)

    emoji_bas = font.render("↓", True, blanc_cassé)
    emoji_bas_rect = emoji_bas.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case - 40))
    fenetre.blit(emoji_bas, emoji_bas_rect)
    
    # Afficher le nombre de de_restant au-dessus des flèches
    de_restant_surface = font.render(str(de_restant), True, blanc_cassé)
    de_restant_rect = de_restant_surface.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case - 110))
    fenetre.blit(de_restant_surface, de_restant_rect)
    
    # Afficher le texte "Emplacements restants" au-dessus du nombre de de_restant
    emplacement_restant_surface = font.render("Emplacements restants", True, blanc_cassé)
    emplacement_restant_rect = emplacement_restant_surface.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case - 130))
    fenetre.blit(emplacement_restant_surface, emplacement_restant_rect)


    # Afficher un message "Déplacez-vous avec les flèches directionnelles" juste au-dessus du texte "Joueur n joue"
    chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
    font = pygame.font.Font(chemin_police, 15)
    message = font.render("Déplacez-vous avec les flèches directionnelles", True,  blanc_cassé)
    message_rect = message.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case - 20))
    fenetre.blit(message, message_rect)

    pygame.display.flip()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def end_game(joueur_index):
    """
    Affiche un message de fin de jeu indiquant le joueur gagnant avec une image de trophé.

    Args:
        joueur_index (int): L'index du joueur gagnant.
    """
    
    chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
    font = pygame.font.Font(chemin_police, 36)
    Jaune = (255, 255, 0)
    message = font.render(f"Le joueur {joueur_index+1} a gagné !", True, Jaune)
    message_rect = message.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case // 2))
    
    # Chargement de l'image
    chemin_image = os.path.join(repertoire_script, 'img','interface',  'trophe.png')
    image = pygame.image.load(chemin_image)
    image_rect = image.get_rect()
    
    # Positionnement de l'image
    image_rect.move_ip((largeur_plateau * taille_case // 2 - image_rect.width // 2, message_rect.top - image_rect.height + 60 ))
    
    fenetre.fill((255, 255, 255))
    fenetre.blit(image, image_rect)
    fenetre.blit(message, message_rect)
    
    pygame.display.flip()
    pygame.time.wait(3000) # Pause de 3 secondes pour voir le message
    pygame.quit()
    sys.exit()
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def pause(fenetre, paused=False):
    """
    Met le jeu en pause et affiche un écran avec deux boutons "Reprendre" et "Quitter".
    Args:
        fenetre: la fenêtre Pygame sur laquelle afficher l'écran de pause
        paused: un booléen indiquant si le jeu est déjà en pause ou non
    """
    # On crée un écran sombre pour mettre le jeu en pause
    ecran_pause = pygame.Surface(fenetre.get_size())
    ecran_pause.set_alpha(128)  # 128 est la transparence de l'écran de pause
    ecran_pause.fill((0, 0, 0)) # On remplit l'écran de pause avec du noir
    fenetre.blit(ecran_pause, (0, 0))

    # On crée les boutons "Reprendre" et "Quitter"
    font = pygame.font.Font(os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf'), 36)
    blanc = (255, 255, 255)
    texte_reprendre = font.render("Reprendre", True, blanc)
    texte_quitter = font.render("Quitter", True, blanc)
    rect_reprendre = texte_reprendre.get_rect(center=fenetre.get_rect().center)
    rect_quitter = texte_quitter.get_rect(center=(fenetre.get_rect().centerx, fenetre.get_rect().centery + 50))

    # On affiche les boutons sur l'écran de pause
    fenetre.blit(texte_reprendre, rect_reprendre)
    fenetre.blit(texte_quitter, rect_quitter)

    # On affiche le nom du jeu en haut de la fenêtre
    rouge =  (255, 0, 0)
    font = pygame.font.Font(os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf'), 50)
    nom_jeu = font.render("The Last Path", True, rouge)
    rect_nom_jeu = nom_jeu.get_rect(center=(fenetre.get_rect().centerx, fenetre.get_rect().centery - 100))
    fenetre.blit(nom_jeu, rect_nom_jeu)

    pygame.display.flip()

    # On attend que l'utilisateur clique sur un bouton ou appuie sur la touche "Escape"
    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE and not paused:
                paused = True
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE and paused:
                pass
            elif evenement.type == pygame.MOUSEBUTTONDOWN:
                if rect_reprendre.collidepoint(evenement.pos):
                    return True
                elif rect_quitter.collidepoint(evenement.pos):
                    pygame.quit()
                    sys.exit()                                                                          
