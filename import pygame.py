import pygame
import time, sys

pygame.init
pygame.mixer.init()
sounda= pygame.mixer.Sound("sons/player/gun/shot.wav")



sounda.play()

time.sleep(5)