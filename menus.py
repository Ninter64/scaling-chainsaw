import pygame
import Weapon
import Player
import random

pygame.mixer.init()
GUNSIZE = 4
gunImages = pygame.transform.scale(pygame.image.load('sprites/ui/reloads/gun/gunbarrel.png'), (56*GUNSIZE,59*GUNSIZE))
#J'ai choisi le nom bOOlet avec deux o volontairement car je résèrve le mot correctement écris à quelques exception comme celle ci car j'utilise ce sprite dans plusieurs scripts (Organisation)
bulletImage = [pygame.transform.scale(pygame.image.load('sprites/ui/reloads/gun/shell.png'), (16*GUNSIZE,16*GUNSIZE)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/gun/boolet.png'), (16*GUNSIZE,16*GUNSIZE)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/gun/empty.png'), (23*GUNSIZE/2,46*GUNSIZE/2)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/gun/boolet_ui.png'), (23*GUNSIZE/2,46*GUNSIZE/2))]
gunSounds=[pygame.mixer.Sound("sons/player/gun/window_open.mp3"),
           pygame.mixer.Sound("sons/player/gun/window_close.wav"),
           pygame.mixer.Sound("sons/player/gun/shellin.wav"),
           pygame.mixer.Sound("sons/player/gun/unload1.wav"),
           pygame.mixer.Sound("sons/player/gun/unload2.wav"),
           pygame.mixer.Sound("sons/player/gun/shot.wav"),
           pygame.mixer.Sound("sons/player/gun/empty.wav")]

shotgunImages = pygame.transform.scale(pygame.image.load('sprites/ui/reloads/shotgun/shotgunbarrel.png'), (59*GUNSIZE,36*GUNSIZE))
slugImage = [pygame.transform.scale(pygame.image.load('sprites/ui/reloads/shotgun/slugshell.png'), (23*GUNSIZE,23*GUNSIZE)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/shotgun/slug.png'), (23*GUNSIZE,23*GUNSIZE)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/shotgun/empty.png'), (23*GUNSIZE/2,46*GUNSIZE/2)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/shotgun/slug_ui.png'), (23*GUNSIZE/2,56*GUNSIZE/2))]

gunSounds=[pygame.mixer.Sound("sons/player/gun/window_open.mp3"),
           pygame.mixer.Sound("sons/player/gun/window_close.wav"),
           pygame.mixer.Sound("sons/player/gun/shellin.wav"),
           pygame.mixer.Sound("sons/player/gun/unload1.wav"),
           pygame.mixer.Sound("sons/player/gun/unload2.wav"),
           pygame.mixer.Sound("sons/player/gun/shot.wav"),
           pygame.mixer.Sound("sons/player/gun/empty.wav")]
shotgunSounds=[pygame.mixer.Sound("sons/player/shotgun/window_open.wav"),
               pygame.mixer.Sound("sons/player/shotgun/window_close.wav"),
               pygame.mixer.Sound("sons/player/shotgun/shellin.wav"),
               pygame.mixer.Sound("sons/player/shotgun/unload1.wav"),
               pygame.mixer.Sound("sons/player/shotgun/unload2.wav"),
               pygame.mixer.Sound("sons/player/shotgun/shot.wav"),
               pygame.mixer.Sound("sons/player/shotgun/doubleshot.wav"),
               pygame.mixer.Sound("sons/player/shotgun/empty.wav")]
#en parlant d'enfer...

ammoDefaultPos = (450,650)
pistol = Weapon.Pistol
shotgun = Weapon.Shotgun

class Reloads:
    def __init__(self):
        #gun vars
        self.gunImage = gunImages
        self.gunShellImage = bulletImage[3]
        self.gunPos = (650,500)
        self.booletPos = ammoDefaultPos
        self.chambershellImage = [bulletImage[pistol.gunAmmo[0]],
                                  bulletImage[pistol.gunAmmo[1]],
                                  bulletImage[pistol.gunAmmo[2]],
                                  bulletImage[pistol.gunAmmo[3]],
                                  bulletImage[pistol.gunAmmo[4]],
                                  bulletImage[pistol.gunAmmo[5]]]
        self.chambershellPos = [(730,510),(795,547),(795,627),(730,665),(665,627),(665,547)]
        self.gunActive = None
        #shotgun vars
        self.shotgunImage = shotgunImages
        self.shotgunShellImage = slugImage[3]
        self.shotgunPos = (650,500)
        self.slugPos = ammoDefaultPos
        self.barrelshellImage = [slugImage[shotgun.shotgunAmmo[0]],slugImage[shotgun.shotgunAmmo[1]]]
        self.barrelshellPos = [(662,520),(782,520)]
        self.shotgunActive = None


#Je Devienne Fou ma parole... Les contrôles fonctionnent mais ont peu de répondant, je pense que c'est la méthode par laquelle on passe les contrôles qui fais des siennes à cause de python qui est lent... ou de mon optimisation... ça doit surement être Python !
       
    #Gun 
    def reload_Gun(self, screen, events):
        mouse_pos = pygame.mouse.get_pos()
        if events.type == pygame.MOUSEBUTTONDOWN:
            if events.button == 1:
                
                if self.booletPos[0] <= mouse_pos[0] <= self.booletPos[0]+50 and self.booletPos[1] <= mouse_pos[1] <= self.booletPos[1]+50:
                    self.gunActive = True
                    self.gunShellImage = bulletImage[1]
                for count in range(6):
                    if self.chambershellPos[count][0] <= mouse_pos[0] <= self.chambershellPos[count][0]+50 and self.chambershellPos[count][1] <= mouse_pos[1] <= self.chambershellPos[count][1]+50:
                        if pistol.gunAmmo[count]==0:
                                gunSounds[random.randint(3,4)].play()
                                pistol.gunAmmo[count] = 2
                             

        if events.type == pygame.MOUSEBUTTONUP:
            if events.button == 1:
                self.gunShellImage = bulletImage[3]
                self.booletPos = ammoDefaultPos
                if self.gunActive:
                    for count in range(6):
                        print(count)
                        if self.chambershellPos[count][0] <= mouse_pos[0] <= self.chambershellPos[count][0]+50 and self.chambershellPos[count][1] <= mouse_pos[1] <= self.chambershellPos[count][1]+50:
                            if pistol.gunAmmo[count]== 2:
                                gunSounds[2].play()
                                pistol.gunAmmo[count] = 1
                self.gunActive = None

        if events.type == pygame.MOUSEMOTION:
            if self.gunActive:
                 self.booletPos = (mouse_pos[0]-25,mouse_pos[1]-25)
                
    def render_Gun(self, surface):    
        surface.blit(gunImages, self.gunPos)
        surface.blit(self.gunShellImage, self.booletPos)
        self.chambershellImage = [bulletImage[pistol.gunAmmo[0]],
                                  bulletImage[pistol.gunAmmo[1]],
                                  bulletImage[pistol.gunAmmo[2]],
                                  bulletImage[pistol.gunAmmo[3]],
                                  bulletImage[pistol.gunAmmo[4]],
                                  bulletImage[pistol.gunAmmo[5]]] 
        for i in range(6):
            surface.blit(self.chambershellImage[i],self.chambershellPos[i])    


    #shotgun
    def reload_Shotgun(self, screen, events):
        print(shotgun.shotgunAmmo)
        mouse_pos = pygame.mouse.get_pos()
        if events.type == pygame.MOUSEBUTTONDOWN:
            if events.button == 1:
                
                if self.slugPos[0] <= mouse_pos[0] <= self.slugPos[0]+50 and self.slugPos[1] <= mouse_pos[1] <= self.slugPos[1]+50:
                    self.shotgunActive = True
                    self.shotgunShellImage = slugImage[1]
                for count in range(2):
                    if self.barrelshellPos[count][0] <= mouse_pos[0] <= self.barrelshellPos[count][0]+50 and self.barrelshellPos[count][1] <= mouse_pos[1] <= self.barrelshellPos[count][1]+50:
                        if shotgun.shotgunAmmo[count]==0:
                                shotgunSounds[random.randint(3,4)].play()
                                shotgun.shotgunAmmo[count] = 2
                             

        if events.type == pygame.MOUSEBUTTONUP:
            if events.button == 1:
                self.shotgunShellImage = slugImage[3]
                self.slugPos = ammoDefaultPos
                if self.shotgunActive:
                    for count in range(2):
                        print(count)
                        if self.barrelshellPos[count][0] <= mouse_pos[0] <= self.barrelshellPos[count][0]+50 and self.barrelshellPos[count][1] <= mouse_pos[1] <= self.barrelshellPos[count][1]+50:
                            if shotgun.shotgunAmmo[count]== 2:
                                shotgunSounds[2].play()
                                shotgun.shotgunAmmo[count] = 1
                self.shotgunActive = None

        if events.type == pygame.MOUSEMOTION:
            if self.shotgunActive:
                 self.slugPos = (mouse_pos[0]-25,mouse_pos[1]-25)
                
    def render_Shotgun(self, surface):    
        surface.blit(shotgunImages, self.shotgunPos)
        surface.blit(self.shotgunShellImage, self.slugPos)
        self.barrelshellImage = [slugImage[shotgun.shotgunAmmo[0]],slugImage[shotgun.shotgunAmmo[1]]] 
        for i in range(2):
            surface.blit(self.barrelshellImage[i],self.barrelshellPos[i])  