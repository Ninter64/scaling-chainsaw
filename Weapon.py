import pygame
import math
import random
from Projectile import Projectile
import time, sys

class Weapon():
    def __init__(self):
        self.lastShot = 0
    
    def shoot():
        pass
    
    @staticmethod
    def normalize_vector(vector):
        if vector == [0, 0]:
            return [0, 0]    
        pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
        return (vector[0] / pythagoras, vector[1] / pythagoras)
    
    @staticmethod
    def rotate_vector(vector, theta):
        resultVector = (vector[0] * math.cos(theta)
                        - vector[1] * math.sin(theta),
                        vector[0] * math.sin(theta)
                        + vector[1] * math.cos(theta))
        return resultVector

class Pistol(Weapon):
    gunAmmo = [1,1,1,1,1,1] 
    def __init__(self):
        super().__init__()
        self.weaponCooldown = 1500 
        self.chamberIndex = 0
        self.shoot_sound = pygame.mixer.Sound("sons/player/gun/shot.wav"); self.shoot_sound.set_volume(0.5)
        self.empty_sound = pygame.mixer.Sound("sons/player/gun/empty.wav"); self.shoot_sound.set_volume(0.5)
    
    def shoot(self, user, mousePos, Ammo=gunAmmo):
        print(Ammo)
        currentTime = pygame.time.get_ticks()

        if self.chamberIndex==6:
            self.chamberIndex=0

        if currentTime - self.lastShot > self.weaponCooldown:
            direction = (mousePos[0] - user.pos[0], mousePos[1] - user.pos[1]) \
                if mousePos != user.pos else (1, 1)
            self.lastShot = currentTime
            if Ammo[self.chamberIndex]==1:
                user.projectiles.add(Projectile(user.pos,
                                                super().normalize_vector(direction),
                                                25, 9999, (0, 0, 255)))
                self.shoot_sound.play()
                Ammo[self.chamberIndex]=0
                self.chamberIndex+=1
            else:
                self.empty_sound.play()
                self.chamberIndex+=1  
            
class Shotgun(Weapon):
    shotgunAmmo = [1,1]
    def __init__(self):
        super().__init__()
        self.weaponCooldown = 750
        self.spreadArc = 35
        self.projectilesCount = 12
        self.chamberIndex = 0
        self.shoot_sound = pygame.mixer.Sound("sons/player/shotgun/shot.wav")
        self.empty_sound = pygame.mixer.Sound("sons/player/shotgun/empty.wav"); self.shoot_sound.set_volume(0.5)
        self.shoot_sound.set_volume(0.5)

    def shoot(self, user, mousePos, Ammo=shotgunAmmo):
        currentTime = pygame.time.get_ticks()

        if self.chamberIndex==2:
            self.chamberIndex=0
            
        if currentTime - self.lastShot > self.weaponCooldown:
            direction = (mousePos[0] - user.pos[0], mousePos[1] - user.pos[1]) \
                if mousePos != user.pos else (1, 1)
            self.lastShot = currentTime
            arcDifference = self.spreadArc / (self.projectilesCount - 1)
            if Ammo[self.chamberIndex]==1:
                for proj in range(self.projectilesCount):
                    theta = math.radians(arcDifference*proj - self.spreadArc/2)
                    projDir = super().rotate_vector(direction, theta)
                    user.projectiles.add(Projectile(user.pos,
                                                    super().normalize_vector(projDir),
                                                    7, 1250, (232, 144, 42)))
                self.shoot_sound.play()
                Ammo[self.chamberIndex]=0
                self.chamberIndex+=1
            else:
                self.empty_sound.play()
                self.chamberIndex+=1

           
                
class MachineGun(Weapon):
    def __init__(self):
        super().__init__()
        self.weaponCooldown = 100
        self.spreadArc = 25
        self.smgAmmo = 20
    
        self.shoot_sound = pygame.mixer.Sound("sons/player/smg/shot.wav")
        self.shoot_sound.set_volume(0.5)


    def shoot(self, user, mousePos):
        currentTime = pygame.time.get_ticks()
        
        if currentTime - self.lastShot > self.weaponCooldown:
            direction = (mousePos[0] - user.pos[0], mousePos[1] - user.pos[1]) \
                if mousePos != user.pos else (1, 1)
            self.lastShot = currentTime
            theta = math.radians(random.random()*self.spreadArc - self.spreadArc/2)
            projDir = super().rotate_vector(direction, theta)
            user.projectiles.add(Projectile(user.pos,
                                            super().normalize_vector(projDir),
                                            6, 1500, (194, 54, 16)))

            self.shoot_sound.play()

