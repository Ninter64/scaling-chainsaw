import pygame
import math
from Projectile import Projectile

ENEMYSIZE = 2

ennemyTorso = [pygame.transform.scale(pygame.image.load('sprites/ennemis/chevalier1.png'), (37*ENEMYSIZE,50*ENEMYSIZE)),
              pygame.transform.scale(pygame.image.load('sprites/ennemis/chevalier2.png'), (37*ENEMYSIZE,50*ENEMYSIZE)),
              pygame.transform.scale(pygame.image.load('sprites/ennemis/chevalier3.png'), (37*ENEMYSIZE,50*ENEMYSIZE)),
              pygame.transform.scale(pygame.image.load('sprites/ennemis/chevalier4.png'), (37*ENEMYSIZE,50*ENEMYSIZE)),]


def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]
    pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
    return (vector[0] / pythagoras, vector[1] / pythagoras)

class Enemy(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    def __init__(self, pos):
        super().__init__()
        self.image = ennemyTorso[0]
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.radius = self.rect.width / 2
        
        self.pos = list(pos)
        self.movementVector = [0, 0]
        self.movementSpeed = 1.5
        self.lastShot = pygame.time.get_ticks()
        self.weaponCooldown = 1500

        # Initialiser les variables pour l'animation des jambes
        self.frame_count = 0
        self.anim_order = [0,1,2,3]
        self.current_anim_index = 0
        self.isFlipped = False
        self.distance_to_player = 100

        
    def move(self, enemies, playerPos, tDelta):
        self.movementVector = (playerPos[0] - self.pos[0],
                               playerPos[1] - self.pos[1])
        self.movementVector = normalize_vector(self.movementVector)
        self.pos[0] += self.movementVector[0] * self.movementSpeed * tDelta
        self.pos[1] += self.movementVector[1] * self.movementSpeed * tDelta
        
        # Collision test with other enemies
        self.movementVector = [0, 0]
        for sprite in enemies:
            if sprite is self:
                continue
            if pygame.sprite.collide_circle(self, sprite):
                self.movementVector[0] += self.pos[0] - sprite.pos[0]
                self.movementVector[1] += self.pos[1] - sprite.pos[1]

        self.movementVector = normalize_vector(self.movementVector)
        self.pos[0] += self.movementVector[0] * 0.5  # The constant is how far the sprite will be
        self.pos[1] += self.movementVector[1] * 0.5  # dragged from the sprite it collided with
        
        self.rect.topleft = self.pos
    def shoot(self, playerPos):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastShot > self.weaponCooldown:
            direction = (playerPos[0] - self.pos[0], playerPos[1] - self.pos[1])
            self.lastShot = currentTime
            self.projectiles.add(Projectile(self.pos,
                                            normalize_vector(direction),
                                            3, 50, (255, 0, 0)))
    def render(self, surface, playerPos):
        self.frame_count += 1 # Ajouter le temps écoulé au compteur de temps
        self.distance_to_player = math.sqrt((playerPos[0]-self.pos[0])**2 + (playerPos[1]-playerPos[1])**2)
        print(self.distance_to_player)
        if self.distance_to_player < 100:
                if self.frame_count % 15 == 0:
                        self.current_anim_index += 1
                        if self.current_anim_index >= len(self.anim_order):
                            self.current_anim_index = 0
                        if self.current_anim_index == 3:
                            self.isFlipped = not self.isFlipped
                            # Changer l'image en fonction de l'indice de la prochaine image à afficher
                        anim_index = self.anim_order[self.current_anim_index]
                        if self.isFlipped == False:
                            self.image = ennemyTorso[anim_index]
                        else:
                            self.image = pygame.transform.flip(ennemyTorso[anim_index], False, True)   
        surface.blit(self.image, self.pos)
