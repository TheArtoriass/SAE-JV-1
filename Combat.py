import pygame
import random
import os


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                    Systèmes de gestion de combat
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)

def combat(joueur_actif, ennemi, fenetre,joueur_index):
    """
    Lance un combat entre le joueur actif et un ennemi donné.

    Args:
        joueur_actif (Personnage): Le personnage du joueur actif.
        ennemi (Ennemi): L'ennemi à combattre.
        fenetre (pygame.Surface): La surface de la fenêtre du jeu.
        joueur_index (int): L'index du joueur actif dans la liste des joueurs.
    """
    
    # Vérifier si l'ennemi a déjà été vaincu
    if (ennemi.x, ennemi.y) in joueur_actif.derniers_ennemis_battus:
        return
    
    # Initialisation des variables pour l'affichage
    largeur_plateau = 20
    hauteur_plateau = 20
    taille_case = 39
    
    chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
    ma_police = pygame.font.Font(chemin_police, 28)
    blanc = (255, 255, 255)

    # Affichage du texte pour choisir le type d'attaque
    text_ligne1 = ma_police.render("Quel type d'attaque voulez-vous faire ?", True, blanc)
    text_ligne2 = ma_police.render("(normal/lente/rapide)", True, blanc)

    rect_ligne1 = text_ligne1.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case // 2 - 20))
    rect_ligne2 = text_ligne2.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case // 2 + 20))

    fenetre.blit(text_ligne1, rect_ligne1)
    fenetre.blit(text_ligne2, rect_ligne2)

    pygame.display.flip()

    type_attaque = ""

    
    # Boucle pour choisir le type d'attaque
    while type_attaque not in ["normal", "lente", "rapide"]:
        for evenement in pygame.event.get():
            if evenement.type == pygame.KEYDOWN:
                if evenement.unicode in ["n", "N"]:
                    type_attaque = "normal"
                elif evenement.unicode in ["l", "L"]:
                    type_attaque = "lente"
                elif evenement.unicode in ["r", "R"]:
                    type_attaque = "rapide"

    # Effacer l'écran et afficher le combat
    fenetre.fill((255, 255, 255))
    pygame.display.flip()
    
    # Boucle de combat
    while joueur_actif.vie > 0 and ennemi.vieE > 0:
        joueur_de = random.randint(1, 8)
        ennemi_de = random.randint(1, 8)


        # Si le joueur a un plus grand dé que l'ennemi
        if joueur_de > ennemi_de:
            if type_attaque == "normal":
                degats = joueur_de
            elif type_attaque == "lente":
                degats = joueur_de + joueur_actif.force
                if ennemi_de > joueur_de:
                    degats = ennemi_de + joueur_actif.agilite
            elif type_attaque == "rapide":
                degats = joueur_de - joueur_actif.force
                if ennemi_de > joueur_de:
                    degats = ennemi_de - joueur_actif.agilite
            ennemi.vieE -= degats
        # Si les dés sont égaux
        elif joueur_de == ennemi_de:
            pass
        # Si l'ennemi a un plus grand dé que le joueur
        else:
            if type_attaque == "normal":
                degats = ennemi_de
            elif type_attaque == "lente":
                degats = ennemi_de + joueur_actif.agilite
                if degats - joueur_actif.force < 1:
                    degats = 1
            elif type_attaque == "rapide":
                degats = ennemi_de - joueur_actif.agilite
                if degats < 1:
                    degats = 1
            joueur_actif.vie -= degats
        joueur_actif.remaining_moves = 0
                    
                        
        # Si le joueur n'a plus de vie
        if joueur_actif.vie <= 0:
            joueur_actif.enlever_tous_objets()
            message = f"Le joueur {joueur_index+1} est vaincu !" 
            joueur_actif.est_vaincu()
            derniers_ennemis_battus = joueur_actif.derniers_ennemis_battus
            if derniers_ennemis_battus:
                dernier_ennemi_battu = derniers_ennemis_battus[-1]
                joueur_actif.x, joueur_actif.y = dernier_ennemi_battu
            else:
                joueur_actif.x, joueur_actif.y = (2,0)
            break
        
        # Si l'ennemi n'a plus de vie
        elif ennemi.vieE <= 0:
            message = f"L'ennemi {ennemi.nomE} est vaincu !"
            joueur_actif.derniers_ennemis_battus.append((ennemi.x, ennemi.y))
            ennemi.vieE = ennemi.vieEMax
            break

    
    # Afficher le message à la fin du combat
    image_path = os.path.join(repertoire_script, 'img','interface', 'fond_flou_combat.jpeg')
    background = pygame.image.load(image_path)
    background = pygame.transform.scale(background, (780, 780))

    fenetre.blit(background, (0, 0))    
    chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
    ma_police = pygame.font.Font(chemin_police, 36)
    blanc = (255, 255, 255)

    texte_message = ma_police.render(message, True, blanc)
    rect_texte = texte_message.get_rect()
    rect_texte.center = fenetre.get_rect().center
    fenetre.blit(texte_message, rect_texte)

    pygame.display.flip()
    pygame.time.delay(1500)


   