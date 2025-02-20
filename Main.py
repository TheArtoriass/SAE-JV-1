import pygame
from Plateau import Plateau, chemin
import random
import sys
from Interface import choisir_personnages, afficher_resultat_de , message_interface, end_game , pause
from Ennemis import liste_ennemis 
from Combat import combat
from Objet import liste_objets

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#   2023-2024
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def lancer_de():
    """
    Lance un dé à 6 faces.
    """
    return random.randint(1, 6)

if __name__ == "__main__":
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                           INITIALISATION
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    pygame.init()

    largeur_plateau = 20
    hauteur_plateau = 20
    taille_case = 39

    joueurs = choisir_personnages()
   
    BLANC = (255, 255, 255)
    plateau = Plateau(largeur_plateau, hauteur_plateau, taille_case)

    plateau.joueurs.extend(joueurs)
    
    for ennemi in liste_ennemis:
        plateau.ajouter_ennemi(ennemi)
        
    for objet in liste_objets:
        plateau.ajouter_objet(objet)
        
    fenetre = pygame.display.set_mode((largeur_plateau * taille_case, hauteur_plateau * taille_case))

    
    joueur_actif = joueurs[0]
    
    joueur_index = 0
    de_restant = 0
    tour_complet = False
    message = ""
    continuer = True
    
    pause_active = False
        
    pygame.mixer.init()
    #On lance la musique du jeu
    pygame.mixer.music.load("musique_jeu.mp3")
    #On met la musique en boucle
    pygame.mixer.music.play(-1)
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                           BOUCLE PRINCIPALE
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    while continuer:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evenement.type == pygame.KEYDOWN:
                # Si le joueur appuie sur la touche espace et qu'il n'a pas encore lancé le dé et que le tour n'est pas complet
                if evenement.key == pygame.K_SPACE and de_restant == 0 and not tour_complet:
                    #On lance le dé et on affiche le résultat
                    resultat_de = lancer_de()
                    afficher_resultat_de(resultat_de)
                    #pygame.time.wait(2000) # Pause de 2 secondes pour voir la valeur du dé
                    de_restant = resultat_de
                    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                              DEPLACEMENT 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                # Si le joueur a encore des cases à parcourir et que le tour n'est pas complet
                elif de_restant > 0 and not tour_complet:
                    if evenement.key == pygame.K_LEFT:
                        if (joueur_actif.x - 1, joueur_actif.y) in chemin:
                            joueur_actif.deplacer('gauche')
                            de_restant -= 1
                    elif evenement.key == pygame.K_RIGHT:
                        if (joueur_actif.x + 1, joueur_actif.y) in chemin:
                            joueur_actif.deplacer('droite')
                            de_restant -= 1
                    elif evenement.key == pygame.K_UP:
                        if (joueur_actif.x, joueur_actif.y - 1) in chemin:
                            joueur_actif.deplacer('haut')
                            de_restant -= 1
                    elif evenement.key == pygame.K_DOWN:
                        if (joueur_actif.x, joueur_actif.y + 1) in chemin:
                            joueur_actif.deplacer('bas')
                            de_restant -= 1
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                           On regarde quand le Dé arrive à zéro s'il y a un objet ou un evenement
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                    if de_restant == 0:
                        # Vérifier si le joueur actuel est sur une case contenant un objet
                        for objet in plateau.objets:
                            if objet.x == joueur_actif.x and objet.y == joueur_actif.y:
                                joueur_actif.prendre_objet(objet)
                                plateau.enlever_objet(objet)
                                
                                    
                        # Vérifier si le joueur actuel est sur un événement
                        for evenement in plateau.carte:
                            if joueur_actif.x == evenement[0] and joueur_actif.y == evenement[1]:
                                evenement_nom = evenement[3]
                                evenement_methode = plateau.evenements[evenement_nom]
                                evenement_methode(joueur_actif,plateau.ennemis)
                                pygame.display.flip()
                                break

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                           Le combat si on croise un ennemi
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
       
                    if joueur_actif.peut_combattre:
                        for ennemi in plateau.ennemis:
                            if joueur_actif.x == ennemi.x and joueur_actif.y == ennemi.y:
                                
                                combat(joueur_actif, ennemi, fenetre,joueur_index)
                                
                                joueur_actif.position_precedente = (joueur_actif.x, joueur_actif.y)
                                    
                                if joueur_actif.vie > 0:
                                    joueur_actif.remaining_moves = 0
                                    break
                                else:
                                    joueur_actif.x, joueur_actif.y = joueur_actif.position_precedente
                                    joueur_actif.remaining_moves = 0
                                    break
                                
                    #SI on arrive sur les coordonnées (16,18) alors le joueur actif à gagné
                    if joueur_actif.x == 16 and joueur_actif.y == 18:
                        
                        end_game(joueur_index)
                        pygame.mixer.music.stop()
                        
                    #On passe au joueur suivant
                    if de_restant == 0:
                        joueur_index = (joueur_index + 1) % len(joueurs)
                        joueur_actif = joueurs[joueur_index]
                        if joueur_index == 0:
                            tour_complet = True
                            
                # Si le joueur appuie sur la touche échap, on met le jeu en pause
                elif evenement.key == pygame.K_ESCAPE:
                    pause_active = True
                                   
        # Si la pause est active, on affiche l'écran de pause
        if pause_active:
            continuer = pause(fenetre)
            pause_active = False
        else:
            if tour_complet:
                tour_complet = False
            
        fenetre.fill(BLANC)
        fenetre.blit(plateau.dessiner(), (0, 0))
        #On affiche les différentes indications sur la fenêtre pygame
        message_interface(joueur_index,de_restant)

pygame.quit()
