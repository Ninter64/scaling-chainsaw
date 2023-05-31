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

shotgunImages = pygame.transform.scale(pygame.image.load('sprites/ui/reloads/shotgun/shotgunbarrel.png'), (59*GUNSIZE,36*GUNSIZE))
slugImages = [pygame.transform.scale(pygame.image.load('sprites/ui/reloads/shotgun/slugshell.png'), (23*GUNSIZE,23*GUNSIZE)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/shotgun/slug.png'), (23*GUNSIZE,23*GUNSIZE)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/shotgun/empty.png'), (23*GUNSIZE/2,46*GUNSIZE/2)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/shotgun/slug_ui.png'), (23*GUNSIZE/2,56*GUNSIZE/2))]

smgImages = [pygame.transform.scale(pygame.image.load('sprites/ui/reloads/smg/smgreload.png'), (109*GUNSIZE,68*GUNSIZE)),
             pygame.transform.scale(pygame.image.load('sprites/ui/reloads/smg/smgmag.png'), (14*GUNSIZE,58*GUNSIZE)),    
             pygame.transform.scale(pygame.image.load('sprites/ui/reloads/smg/lever.png'), (9*GUNSIZE,5*GUNSIZE)),
             pygame.transform.scale(pygame.image.load('sprites/ui/reloads/smg/smgmagfull.png'), (14*GUNSIZE,58*GUNSIZE))]

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
smg= Weapon.MachineGun

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
        self.shotgunShellImage = slugImages[3]
        self.shotgunPos = (650,500)
        self.slugPos = ammoDefaultPos
        self.barrelshellImage = [slugImages[shotgun.shotgunAmmo[0]],slugImages[shotgun.shotgunAmmo[1]]]
        self.barrelshellPos = [(662,520),(782,520)]
        self.shotgunActive = None
        #smg vars
        self.smgImage = smgImages[0]
        self.magImage = smgImages[1]
        self.leverImage = smgImages[2]
        self.smgPos = (500,300)
        self.magPos = (616,540)
        self.leverPos = (525,308)
        self.magActive = None
        self.leverActive = None
        #Étape 0 : Il faut désarmer la SMG pour éjecter la dernière balle #Étape 1 : Il faut enlever le chargeur vide
        #Étape 2 : Il faut mettre un nouveau chargeur de 20 balle #Étape 3 : Il faut armer la SMG #Étape 4 : Prêt à tirer
        self.smgReloadStep = 0

        
        


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
        mouse_pos = pygame.mouse.get_pos()
        if events.type == pygame.MOUSEBUTTONDOWN:
            if events.button == 1:
                
                if self.slugPos[0] <= mouse_pos[0] <= self.slugPos[0]+50 and self.slugPos[1] <= mouse_pos[1] <= self.slugPos[1]+50:
                    self.shotgunActive = True
                    self.shotgunShellImage = slugImages[1]
                for count in range(2):
                    if self.barrelshellPos[count][0] <= mouse_pos[0] <= self.barrelshellPos[count][0]+50 and self.barrelshellPos[count][1] <= mouse_pos[1] <= self.barrelshellPos[count][1]+50:
                        if shotgun.shotgunAmmo[count]==0:
                                shotgunSounds[random.randint(3,4)].play()
                                shotgun.shotgunAmmo[count] = 2
                             

        if events.type == pygame.MOUSEBUTTONUP:
            if events.button == 1:
                self.shotgunShellImage = slugImages[3]
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
        self.barrelshellImage = [slugImages[shotgun.shotgunAmmo[0]],slugImages[shotgun.shotgunAmmo[1]]] 
        for i in range(2):
            surface.blit(self.barrelshellImage[i],self.barrelshellPos[i]) 


    #smg
    def reload_Smg(self, screen, events):
        mouse_pos=pygame.mouse.get_pos()
        if self.smgReloadStep == 4:
            smg.smgAmmo=20
            self.smgImage = smgImages[0]
            self.magImage = smgImages[1]
            self.leverImage = smgImages[2]
            self.smgPos = (500,300)
            self.magPos = (616,540)
            self.leverPos = (525,308)
            self.magActive = None
            self.leverActive = None
            self.smgReloadStep = 0
        
        if events.type == pygame.MOUSEBUTTONDOWN:
            if events.button == 1:
                
                if self.leverPos[0] <= mouse_pos[0] <= self.leverPos[0]+25 and  self.leverPos[1] <= mouse_pos[1] <= self.leverPos[1]+50 and (self.smgReloadStep==0 or self.smgReloadStep==3):
                    self.leverActive = True
                if self.magPos[0] <= mouse_pos[0] <= self.magPos[0]+40 and  self.magPos[1] <= mouse_pos[1] <= self.magPos[1]+300 and (self.smgReloadStep==1 or self.smgReloadStep==2):
                    self.magActive = True

        if events.type == pygame.MOUSEBUTTONUP:
            if events.button == 1:
                self.leverActive = None

        if events.type == pygame.MOUSEMOTION:
            print(self.leverPos)
            if self.smgReloadStep== 0 or 3:
                if self.leverActive and 517 < self.leverPos[0] < 760:
                    self.leverPos = (mouse_pos[0]-12,self.leverPos[1])
                if self.leverPos[0] > 760:
                    self.leverPos=(758,self.leverPos[1])
                if self.leverPos[0] < 517:
                    self.leverPos=(520,self.leverPos[1])
                if self.leverPos[0] > 755 and self.smgReloadStep==0:
                    self.smgReloadStep+=1
                if self.leverPos[0] < 525 and self.smgReloadStep==3:
                    self.leverPos=(525,308)
                    self.smgReloadStep+=1
            if self.smgReloadStep== 1 or 2:
                if self.magActive and 540 < self.magPos[1] < 700:
                    if self.magPos[1] > 698:
                        self.leverPos=(self.magPos[0],694)
                    if self.leverPos[1] < 545:
                        self.leverPos=(self.leverPos[0],530)
                    if self.leverPos[1] > 688 and self.smgReloadStep==1:
                        self.magImage=smgImages[3]
                        self.smgReloadStep+=1
                    if self.leverPos[1] < 550 and self.smgReloadStep==2:
                        self.smgReloadStep+=1



    
    def render_Smg(self, surface):    
        surface.blit(self.magImage, self.magPos)
        surface.blit(self.smgImage, self.smgPos)
        surface.blit(self.leverImage, self.leverPos)
        