import pygame
import Weapon
import Player
import random

GUNSIZE = 4
gunImages = pygame.transform.scale(pygame.image.load('sprites/ui/reloads/gun/gunbarrel.png'), (56*GUNSIZE,59*GUNSIZE))
#J'ai choisi le nom bOOlet avec deux o volontairement car je résèrve le mot correctement écris à quelques exception comme celle ci car j'utilise ce sprite dans plusieurs scripts (Organisation)
bulletImage = [pygame.transform.scale(pygame.image.load('sprites/ui/reloads/gun/shell.png'), (16*GUNSIZE,16*GUNSIZE)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/gun/boolet.png'), (16*GUNSIZE,16*GUNSIZE)),
               pygame.transform.scale(pygame.image.load('sprites/ui/reloads/gun/boolet_ui.png'), (23*GUNSIZE/2,46*GUNSIZE/2))]
bulletDefaultPos = (450,650)
pistol = Weapon.Pistol

class Reloads:
    def __init__(self):
        self.image = gunImages
        self.shellImage = bulletImage[2]
        self.pos = (650,500)
        self.booletPos = bulletDefaultPos
        self.availableWeapons = [Weapon.Pistol(), Weapon.Shotgun(), Weapon.MachineGun()]
        self.chambershellImage = [bulletImage[pistol.gunAmmo[0]],
                                  bulletImage[pistol.gunAmmo[1]],
                                  bulletImage[pistol.gunAmmo[2]],
                                  bulletImage[pistol.gunAmmo[3]],
                                  bulletImage[pistol.gunAmmo[4]],
                                  bulletImage[pistol.gunAmmo[5]]]
        self.chambershellPos = [(),(),(),(),(),()]
        self.active = None
        self.ammoGun = 6

#Je Devienne Fou ma parole... Les contrôles fonctionnent mais ont peu de répondant, je pense que c'est la méthode par laquelle on passe les contrôles qui fais des siennes à cause de python qui est lent...
       
       
        #Gun 
    def reload_Gun(self, screen, events):
        print(self.chambershellImage)
        mouse_pos = pygame.mouse.get_pos()
        if events.type == pygame.MOUSEBUTTONDOWN:
            if (self.booletPos[0] - mouse_pos[0]) < 50 and (self.booletPos[1] - mouse_pos[1]) < 50:
                if events.button == 1:
                            self.active = True
                            self.shellImage = bulletImage[1]
                            #if pygame.Rect.colliderect(self.shellImage, )
                            

        if events.type == pygame.MOUSEBUTTONUP:
            if events.button == 1:
                self.shellImage = bulletImage[2]
                self.active = None
                self.booletPos = bulletDefaultPos
                

        if events.type == pygame.MOUSEMOTION:
            if self.active:
                 self.booletPos = (mouse_pos[0]-25,mouse_pos[1]-25)
                
    def render(self, surface):    
        surface.blit(gunImages, self.pos)
        surface.blit(self.shellImage, self.booletPos)               
