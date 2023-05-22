import pygame
import math
import Weapon

# Couleur du joueur (rouge)
PLAYERCOLOR = (255, 0, 0)
# Taille du joueur
PLAYERSIZE = 2

size    = (1000, 800)

# Images pour l'animation des jambes du joueur
playerLegs = [pygame.transform.scale(pygame.image.load('sprites/player/legs/leg4.png'), (27*PLAYERSIZE,27*PLAYERSIZE)),
              pygame.transform.scale(pygame.image.load('sprites/player/legs/leg3.png'), (27*PLAYERSIZE,27*PLAYERSIZE)),
              pygame.transform.scale(pygame.image.load('sprites/player/legs/leg2.png'), (27*PLAYERSIZE,27*PLAYERSIZE)),
              pygame.transform.scale(pygame.image.load('sprites/player/legs/leg1.png'), (27*PLAYERSIZE,27*PLAYERSIZE)),]

playerTorso = [pygame.transform.scale(pygame.image.load('sprites/player/torso/Player_gun.png'), (45*PLAYERSIZE,16*PLAYERSIZE)),
               pygame.transform.scale(pygame.image.load('sprites/player/torso/Player_shotgun.png'), (45*PLAYERSIZE,16*PLAYERSIZE)),
               pygame.transform.scale(pygame.image.load('sprites/player/torso/Player_smg.png'), (45*PLAYERSIZE,16*PLAYERSIZE))]

# Fonction qui normalise un vecteur pour le rendre unitaire (de longueur 1)
def normalize_vector(vector):
    # Si le vecteur est nul, retourner [0, 0]
    if vector == [0, 0]:
        return [0, 0]    
    # Calculer la longueur du vecteur
    pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
    # Diviser chaque composante du vecteur par sa longueur pour le rendre unitaire
    return (vector[0] / pythagoras, vector[1] / pythagoras)

def blitRotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)
  
    # draw rectangle around the image
    #pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)


# Classe pour représenter le joueur
class Player(pygame.sprite.Sprite):
    # Groupe de projectiles lancés par le joueur (pour les gérer tous ensemble)
    projectiles = pygame.sprite.Group()
    def __init__(self, screenSize):
        super().__init__()
        # Initialiser l'image du joueur avec la première image d'animation des jambes
        self.image = playerLegs[0]
        self.playerUp = playerTorso
        # Définir le rectangle de collision pour le joueur
        self.rect = self.image.get_rect(x=screenSize[0]//2, y=screenSize[1]//2)
        # Compteur de temps pour l'animation des jambes
        self.frame_count = 0
        # Position du joueur
        self.pos = [screenSize[0] // 2, screenSize[1] // 2]
        # Points de vie du joueur
        self.health = 5
        # Booléen pour savoir si le joueur est en vie
        self.alive = True
        # Vecteur de mouvement du joueur
        self.movementVector = [0, 0]
        # Vitesse de déplacement du joueur
        self.movementSpeed = 4
        # Liste des armes disponibles pour le joueur
        self.availableWeapons = [Weapon.Pistol(), Weapon.Shotgun(), Weapon.MachineGun()]
        # Arme équipée par défaut pour le joueur
        self.equippedWeapon = self.availableWeapons[0]
        # Arme équipée, lisible universelement 1:Gun 2:Shotgun 3:SMG par défaut 0 pour éviter des erreurs
        self.holster = 0

        # Initialiser les variables pour l'animation des jambes
        self.leg_order = [3, 2, 1, 0, 1, 2, 3, 3, 2, 1, 0, 1, 2, 3]
        self.current_leg_index = 0
        self.isFlipped = False
        #Direction :   O
        #            1 2 3
        #             \|/
        #        S   4-Ø-6  N
        #             /|\
        #            7 8 9
        #              E
        self.direction = 6
            
    # Fonction pour déplacer le joueur
    def move(self, screenSize, tDelta,):    
        
        
        
        #Animation
        if self.movementVector != [0,0]:
            
            self.isFlipped = False
            self.frame_count += 1 # Ajouter le temps écoulé au compteur de temps
                # Mettre à jour l'indice de la prochaine image à afficher toutes les 15 frames
            if self.frame_count % 15 == 0:
                self.current_leg_index += 1
                if self.current_leg_index >= len(self.leg_order):
                    self.current_leg_index = 0
                if self.current_leg_index > 6:
                    self.isFlipped = True
                    # Changer l'image en fonction de l'indice de la prochaine image à afficher
                leg_index = self.leg_order[self.current_leg_index]
                if self.isFlipped == False:
                    self.image = playerLegs[leg_index]
                else:
                    self.image = pygame.transform.flip(playerLegs[leg_index], False, True)       
            
            if self.movementVector[1] < 0:
                if self.movementVector[0] < 0:
                    self.direction = 1
                if self.movementVector[0] == 0:
                    self.direction = 2
                if self.movementVector[0] > 0:
                    self.direction = 3
            if self.movementVector[1] == 0:
                if self.movementVector[0] < 0:
                    self.direction = 4
                if self.movementVector[0] > 0:
                    self.direction = 6
            if self.movementVector[1] > 0:
                if self.movementVector[0] < 0:
                    self.direction = 7
                if self.movementVector[0] == 0:
                    self.direction = 8
                if self.movementVector[0] > 0:
                    self.direction = 9


        self.movementVector = normalize_vector(self.movementVector)
        
        newPos = (self.pos[0] + self.movementVector[0]*self.movementSpeed*tDelta,
                  self.pos[1] + self.movementVector[1]*self.movementSpeed*tDelta)
        if newPos[0] < 0:
            self.pos[0] = 0
            
        elif newPos[0] > screenSize[0] - self.rect.width:
            self.pos[0] = screenSize[0] - self.rect.width
            

        else:
            self.pos[0] = newPos[0]

        if newPos[1] < 0:
            self.pos[1] = 0
        elif newPos[1] > screenSize[1]-self.rect.height:
            self.pos[1] = screenSize[1]-self.rect.width
        else:
            self.pos[1] = newPos[1]

        self.rect.topleft = self.pos
        
        
        
        
        
        self.movementVector = [0, 0]
   
            
    def shoot(self, mousePos):
        self.equippedWeapon.shoot(self, mousePos)
        
        




    def render(self, surface):
        
        

        #Direction :   O
        #            1 2 3
        #             \|/
        #        S   4-Ø-6  N
        #             /|\
        #            7 8 9
        #              E
        if self.direction == 6:
            blitRotate(surface, self.image, self.pos, (self.image.get_width()//2, self.image.get_height()//2), 0)
        elif self.direction == 7:
            blitRotate(surface, self.image, self.pos, (self.image.get_width()//2, self.image.get_height()//2), 225)    
        elif self.direction == 2:
            blitRotate(surface, self.image, self.pos, (self.image.get_width()//2, self.image.get_height()//2), 270)
        elif self.direction == 9:
            blitRotate(surface, self.image, self.pos, (self.image.get_width()//2, self.image.get_height()//2), 315)
        elif self.direction == 4:
            blitRotate(surface, self.image, self.pos, (self.image.get_width()//2, self.image.get_height()//2), 180)
        elif self.direction == 1:
            blitRotate(surface, self.image, self.pos, (self.image.get_width()//2, self.image.get_height()//2), 135)
        elif self.direction == 8:
            blitRotate(surface, self.image, self.pos, (self.image.get_width()//2, self.image.get_height()//2), 90)
        elif self.direction == 3:
            blitRotate(surface, self.image, self.pos, (self.image.get_width()//2, self.image.get_height()//2), 45)

        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1])
        angle = math.degrees(angle)
        
        if isinstance(self.equippedWeapon, Weapon.Pistol):
            blitRotate(surface, playerTorso[0], self.pos, (10*PLAYERSIZE,8*PLAYERSIZE), angle-90)
            self.holster=1
        elif isinstance(self.equippedWeapon, Weapon.Shotgun):
            blitRotate(surface, playerTorso[1], self.pos, (16*PLAYERSIZE,6*PLAYERSIZE), angle-90)
            self.holster=2
        elif isinstance(self.equippedWeapon, Weapon.MachineGun):
            blitRotate(surface, playerTorso[2], self.pos, (8*PLAYERSIZE,7*PLAYERSIZE), angle-90) 
            self.holster=3
