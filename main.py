import pygame
import random
from Player import Player
from Enemy import Enemy
from Projectile import Projectile


pygame.init()
pygame.mixer.init()

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
smgSounds=[pygame.mixer.Sound("sons/player/smg/uncock.wav"),
           pygame.mixer.Sound("sons/player/smg/unload.wav"),
           pygame.mixer.Sound("sons/player/smg/reload.wav"),
           pygame.mixer.Sound("sons/player/smg/cock.wav"),
           pygame.mixer.Sound("sons/player/smg/shot.wav"),
           pygame.mixer.Sound("sons/player/smg/empty.wav")]




size    = (1000, 800)
BGCOLOR = (255, 255, 200)
screen = pygame.display.set_mode(size)
uiweapons = [pygame.image.load("sprites/ui/gameui/gunbig.png"),
             pygame.image.load("sprites/ui/gameui/shotgunbig.png"),
             pygame.image.load("sprites/ui/gameui/smgbig.png")]
scoreFont = pygame.font.Font("polices/Lady Radical 2.ttf", 30)
healthFont = pygame.font.Font("polices/OmnicSans.ttf", 50)
healthRender = healthFont.render('z', True, pygame.Color('red'))
pygame.display.set_caption("Top Down")

done = False
hero = pygame.sprite.GroupSingle(Player(screen.get_size()))

enemies = pygame.sprite.Group()
lastEnemy = 0
sczdqore = 0
clock = pygame.time.Clock()

def render_menu():
    reloadrender = scoreFont.render("RECGARGEMRNT", True, pygame.Color('black'))
    scoreRect = reloadrender.get_rect()
    scoreRect.right = size[0] - 100
    scoreRect.top = 20
    screen.blit(reloadrender, scoreRect)

def move_entities(hero, enemies, timeDelta):
    score = 0
    hero.sprite.move(screen.get_size(), timeDelta)
    for enemy in enemies:
        enemy.move(enemies, hero.sprite.rect.topleft, timeDelta)
        enemy.shoot(hero.sprite.rect.topleft)
    for proj in Enemy.projectiles:
        proj.move(screen.get_size(), timeDelta)
        if pygame.sprite.spritecollide(proj, hero, False):
            proj.kill()
            hero.sprite.health -= 1
            if hero.sprite.health <= 0:
                hero.sprite.alive = True#False
    for proj in Player.projectiles:
        proj.move(screen.get_size(), timeDelta)
        enemiesHit = pygame.sprite.spritecollide(proj, enemies, True)
        if enemiesHit and hero.sprite.holster != 1:
            proj.kill()
            score += len(enemiesHit)
        #Putain mais au lieu de faire un elif pourquoi pas juste mettre "else if:" ? ça craint...
        elif enemiesHit:
            score += len(enemiesHit)   
    return score

def render_entities(hero, enemies):
    hero.sprite.render(screen)
    for proj in Player.projectiles:
        proj.render(screen)
    for proj in Enemy.projectiles:
        proj.render(screen)
    for enemy in enemies:
        enemy.render(screen)
    
def process_keys(keys, hero):
    if keys[pygame.K_z]:
        hero.sprite.movementVector[1] -= 1
    if keys[pygame.K_q]:
        hero.sprite.movementVector[0] -= 1
    if keys[pygame.K_s]:
        hero.sprite.movementVector[1] += 1
    if keys[pygame.K_d]:
        hero.sprite.movementVector[0] += 1
    if keys[pygame.K_1]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[0]
    if keys[pygame.K_2]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[1]
    if keys[pygame.K_3]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[2]
        
def process_mouse(mouse, hero):
    if mouse[0]:
        hero.sprite.shoot(pygame.mouse.get_pos())

            

def game_loop():  
    done = False
    hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
    enemies = pygame.sprite.Group()
    lastEnemy = pygame.time.get_ticks()
    gameState= 0
    score = 0
    print(gameState)

    while hero.sprite.alive and not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        currentTime = pygame.time.get_ticks()
       
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:            
                    if gameState != 1:
                        if hero.sprite.holster == 1:
                            gunSounds[0].play()
                        elif hero.sprite.holster == 2:
                            shotgunSounds[0].play()
                        gameState = 1
                    else:        #ah le voilà le fameux else if {} hehe !
                        if hero.sprite.holster == 1:
                            gunSounds[1].play()
                        elif hero.sprite.holster == 2:
                            shotgunSounds[1].play()    
                        gameState=0    

            if event.type == pygame.QUIT:
                return True
        screen.fill(BGCOLOR)
        
        process_keys(keys, hero)
        if gameState==0:
            process_mouse(mouse, hero)
        elif gameState==1:
            render_menu()
 
        # Enemy spawning process
        if lastEnemy < currentTime - 200 and len(enemies) < 50:
            spawnSide = random.random()
            if spawnSide < 0.25:
                enemies.add(Enemy((0, random.randint(0, size[1]))))
            elif spawnSide < 0.5:
                enemies.add(Enemy((size[0], random.randint(0, size[1]))))
            elif spawnSide < 0.75:
                enemies.add(Enemy((random.randint(0, size[0]), 0)))
            else:
                enemies.add(Enemy((random.randint(0, size[0]), size[1])))
            lastEnemy = currentTime
        
        score += move_entities(hero, enemies, clock.get_time()/17)
        render_entities(hero, enemies)
        
        # Health and score render
        for hp in range(hero.sprite.health):
            screen.blit(healthRender, (15 + hp*35, 0))
        scoreRender = scoreFont.render(str(score), True, pygame.Color('black'))
        weaponRender = uiweapons[0]
        
        scoreRect = scoreRender.get_rect()
        scoreRect.right = size[0] - 20
        scoreRect.top = 20

        weaponRect = weaponRender.get_rect()
        weaponRect.left = 20
        weaponRect.top = 55

        

        if hero.sprite.holster == 1:
            weaponRender = uiweapons[0]
        elif hero.sprite.holster == 2:
            weaponRender = uiweapons[1]
        elif hero.sprite.holster == 3:
            weaponRender = uiweapons[2]
        screen.blit(scoreRender, scoreRect)
        screen.blit(weaponRender, weaponRect)
        
        pygame.display.flip()
        clock.tick(120)

done = game_loop()
while not done:
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    currentTime = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    
    if keys[pygame.K_RETURN]:
        done = game_loop()   
pygame.quit()
