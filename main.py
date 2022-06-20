from random import *
import pygame
from pygame.locals import *

n_joueurs = 3
arrivee = 21
mode_test = False

pygame.init()
pygame.display.init()
largeur = 1200
hauteur = 240+80* n_joueurs
ecran = pygame.display.set_mode((largeur, hauteur))

asset_path = "./assets/"
j1 = pygame.image.load(asset_path + "j1.png")
j1 = pygame.transform.scale(j1, (32, 32))
pygame.display.set_icon(j1)
pygame.display.set_caption("Dico-régate")
dico = open(asset_path + "dico.txt")
mots = set([m[:-1] for m in dico])

n_occ = dict()
alphabet = "abcdefghijklmnopqrstuvwxyz"
for lettre in alphabet:
    n_occ[lettre] = 0

for mot in mots:
    for lettre in mot:
        if lettre in n_occ:
            n_occ[lettre] += 1

loop = True

COULEUR_TEXTE = (63,73,100)
CIEL = (153, 217, 234)
OCEAN = (63,73,204)
font = pygame.font.SysFont(None, 24)

def afficher_texte(texte, ligne, alignement, couleur):
    img = font.render(texte, True, couleur)
    y = 42 * ligne + 10
    if alignement == "g":
        x = 10
    elif alignement == "c":
        x = (largeur - img.get_width())//2
    else:
        x = largeur - img.get_width() - 10
    ecran.blit(img, (x,y))

def afficher_bateaux():
    pygame.draw.rect(ecran, OCEAN, pygame.Rect(0, 200, largeur, 40 + 80 * n_joueurs))
    bouee = pygame.image.load(asset_path + "bouee.png")
    bouee = pygame.transform.scale(bouee, (32, 32))
    ecran.blit(bouee, ((50 * arrivee - 15), 200))
    for i_joueur in range(n_joueurs):
        bateau = pygame.image.load(asset_path + "j" + str(i_joueur+1) + ".png")
        bateau = pygame.transform.scale(bateau, (64, 64))
        ecran.blit(bateau, (50 * pos[i_joueur],220 + 80 * i_joueur))
    ecran.blit(bouee, ((50 * arrivee - 15), 200 + 80 * n_joueurs))

def tour_joueur(joueur_actuel):
    fin_tour = pygame.time.get_ticks() + 15000
    
    equilibre = False
    while not equilibre:
        avance = []
        recule = []
        for lettre in alphabet:
            if random()<1/3:
                avance.append(lettre)
            elif random()<0.5:
                recule.append(lettre)
        if 900000 < sum([n_occ[l] for l in recule]) < sum([n_occ[l] for l in avance]) < 1000000:
            equilibre = True
    essai = ''
    av_invalide = ""
    valide = False
    pos_init = pos[joueur_actuel]
    debut_animation = -1
    decalage = 0
    duree_animation = 1000
    
    while True:
        ecran.fill(CIEL)
        acensi = pygame.image.load(asset_path + "logo.png")
        acensi = pygame.transform.scale(acensi, (192, 192))
        ecran.blit(acensi, (700,-20))
        if not valide:
            timer = fin_tour - pygame.time.get_ticks()
        afficher_texte("Tour actuel : ", 0, "g", COULEUR_TEXTE)
        bateau = pygame.image.load(asset_path + "j" + str(joueur_actuel+1) + ".png")
        bateau = pygame.transform.scale(bateau, (32, 32))
        ecran.blit(bateau, (110,3))
        afficher_texte("Temps restant : " + str(timer//1000), 0, "d", COULEUR_TEXTE)
        afficher_texte("Vents favorables : " + ''.join(avance), 1, "d", COULEUR_TEXTE)
        afficher_texte("Vents contraires : " + ''.join(recule), 2, "d", COULEUR_TEXTE)
        afficher_texte(av_invalide, 3, "g", COULEUR_TEXTE)
        afficher_bateaux()
        
        if timer<0:
            timer = 0
            if essai in mots or mode_test:
                valide = True
            else:
                if essai!="":
                    av_invalide = "Le mot \"" + essai + "\" n'est pas dans le dictionnaire."
                essai = ""
                valide = True
        
        if valide:
            if debut_animation == -1:
                debut_animation = pygame.time.get_ticks()
                for lettre in essai:
                    if lettre in avance:
                        decalage += 1
                    if lettre in recule and pos[joueur_actuel] + decalage>0:
                        decalage -= 1
                    if pos[joueur_actuel] + decalage == arrivee:
                        break
            l = (pygame.time.get_ticks() - debut_animation) / duree_animation
            pos[joueur_actuel] = pos_init + decalage * l
            if l>1:
                pos[joueur_actuel] = pos_init + decalage
                return
            
        
        for event in pygame.event.get():
            if(event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                global loop
                loop = False
                return
            if event.type == pygame.KEYDOWN and not valide:
                if event.key == pygame.K_BACKSPACE:
                    essai = essai[:-1]
                elif event.key == pygame.K_RETURN:
                    if essai in mots or mode_test:
                        valide = True
                    else:
                        av_invalide = "Le mot \"" + essai + "\" n'est pas dans le dictionnaire."
                        essai = ""
                else:
                    essai += event.unicode
        afficher_texte(essai, 2, "c", COULEUR_TEXTE)
        pygame.display.flip()

def afficher_classement():
    while True:
        ecran.fill(CIEL)
        acensi = pygame.image.load(asset_path + "logo.png")
        acensi = pygame.transform.scale(acensi, (192, 192))
        ecran.blit(acensi, (700,-20))
        afficher_texte("Résultats : ", 0, "g", COULEUR_TEXTE)
        afficher_texte("Appuyez sur entrée pour rejouer.", 2.5, "d", COULEUR_TEXTE)
        afficher_texte("Entrez un chiffre de 2 à 5 pour changer le nombre de joueurs.", 3.5, "d", COULEUR_TEXTE)
        global pos
        pos = [-5] * n_joueurs
        afficher_bateaux()
        bateau1 = pygame.image.load(asset_path + "j" + str(classement[0]+1) + ".png")
        bateau1 = pygame.transform.scale(bateau1, (112, 112))
        ecran.blit(bateau1, (400,112))
        medaille = pygame.transform.scale(pygame.image.load(asset_path + "medal_gold.png"), (64,64))
        ecran.blit(medaille, (426,250))
        bateau2 = pygame.image.load(asset_path + "j" + str(classement[1]+1) + ".png")
        bateau2 = pygame.transform.scale(bateau2, (96, 96))
        ecran.blit(bateau2, (300,140))
        medaille = pygame.transform.scale(pygame.image.load(asset_path + "medal_silver.png"), (64,64))
        ecran.blit(medaille, (318,250))
        if len(classement)>=3:
            bateau3 = pygame.image.load(asset_path + "j" + str(classement[2]+1) + ".png")
            bateau3 = pygame.transform.scale(bateau3, (80, 80))
            ecran.blit(bateau3, (520,150))
            medaille = pygame.transform.scale(pygame.image.load(asset_path + "medal_bronze.png"), (64,64))
            ecran.blit(medaille, (530,250))
        
        for event in pygame.event.get():
            if(event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                global loop
                loop = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    set_n_joueurs(2)
                if event.key == pygame.K_3:
                    set_n_joueurs(3)
                if event.key == pygame.K_4:
                    set_n_joueurs(4)
                if event.key == pygame.K_5:
                    set_n_joueurs(5)
                if event.key == pygame.K_RETURN:
                    return
        pygame.display.flip()

def ecran_titre():
    while True:
        ecran.fill(CIEL)
        acensi = pygame.image.load(asset_path + "logo.png")
        acensi = pygame.transform.scale(acensi, (192, 192))
        ecran.blit(acensi, (700,-20))
        afficher_texte("Règles de la dico-régate : ", 0, "g", COULEUR_TEXTE)
        afficher_texte("Les joueurs jouent à tour de rôle.", 0.75, "g", COULEUR_TEXTE)
        afficher_texte("À chaque tour vous disposez de 15 secondes pour choisir un mot de la langue française.", 1.45, "g", COULEUR_TEXTE)
        afficher_texte("Certaines lettres sont associées à des vents favorables, votre bateau ira plus vite si vous les utilisez.", 2.25, "g", COULEUR_TEXTE)
        afficher_texte("D'autres sont associées à des vents contraires, et ralentiront (voire feront reculer) votre bateau.", 3, "g", COULEUR_TEXTE)
        afficher_texte("Le but est d'atteindre la ligne d'arrivée (entre les deux bouées jaunes) plus vite que les autres.", 3.75, "g", COULEUR_TEXTE)
        afficher_texte("Appuyez sur un chiffre entre 2 et 5", 2, "d", COULEUR_TEXTE)
        afficher_texte("pour régler le nombre de joueurs.", 2.7, "d", COULEUR_TEXTE)
        afficher_texte("Appuyez sur entrée pour commencer.", 3.8, "d", COULEUR_TEXTE)
        afficher_bateaux()
        
        for event in pygame.event.get():
            if(event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                global loop
                loop = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    set_n_joueurs(2)
                if event.key == pygame.K_3:
                    set_n_joueurs(3)
                if event.key == pygame.K_4:
                    set_n_joueurs(4)
                if event.key == pygame.K_5:
                    set_n_joueurs(5)
                if event.key == pygame.K_RETURN:
                    return
        pygame.display.flip()

def set_n_joueurs(n):
    global n_joueurs
    n_joueurs = n
    global hauteur
    hauteur = 240+80* n_joueurs
    global ecran
    ecran = pygame.display.set_mode((largeur, hauteur))
    global pos
    pos = [2 + (4*i)//n_joueurs for i in range(n_joueurs)]

set_n_joueurs(4)

ecran_titre()
set_n_joueurs(n_joueurs)

joueur_actuel = 0
debut_tour = 0
classement = []

while loop:
    tour_joueur(joueur_actuel)
    if pos[joueur_actuel]==arrivee:
        classement.append(joueur_actuel)
    joueur_actuel = (joueur_actuel+1)%n_joueurs
    while joueur_actuel in classement:
        joueur_actuel = (joueur_actuel+1)%n_joueurs
    if len(classement)==n_joueurs-1:
        classement.append(joueur_actuel)
        afficher_classement()
        set_n_joueurs(n_joueurs)
        classement = []
        joueur_actuel = 0
        debut_tour = 0
pygame.quit()
