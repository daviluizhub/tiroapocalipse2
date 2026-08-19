import pygame
import random

pygame.init()
pygame.mixer.init()

# ================== TELA ==================
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tiro Apocalipse")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# ================== ASSETS ==================
fundo = pygame.image.load("fundo.jpg").convert()
player_img = pygame.image.load("player.png").convert_alpha()
enemy_img = pygame.image.load("inimigo.png").convert_alpha()
boss_img = pygame.image.load("boss.png").convert_alpha()
som_tiro = pygame.mixer.Sound("laserShoot.wav")

# ================== PLAYER ==================
player = pygame.Rect(100, ALTURA // 2, 48, 48)
VEL_PLAYER = 5
vida_player = 100
VIDA_MAX = 100

# ================== POWER UPS ==================
power_dano = 1
power_vel_tiro = 0

# ================== TIROS ==================
player_tiros = []
enemy_tiros = []
VEL_TIRO_PLAYER = 10
VEL_TIRO_ENEMY = 6

# ================== INIMIGOS ==================
inimigos = []
spawn_timer = 0

# ================== FASE ==================
fase = 1
kills = 0

# ================== BOSS ==================
boss_ativo = False
boss = pygame.Rect(1050, ALTURA // 2 - 60, 120, 120)
boss_hp = 0
boss_hp_max = 0

# ================== FUNÇÕES ==================
def config_fase(f):
    if f <= 2:
        return {"spawn": 120, "vel": 2, "atira": False}
    elif f <= 4:
        return {"spawn": 90, "vel": 3, "atira": True}
    elif f == 5:
        return {"spawn": 200, "vel": 0, "atira": True}
    elif f <= 7:
        return {"spawn": 80, "vel": 4, "atira": True}
    elif f <= 9:
        return {"spawn": 60, "vel": 5, "atira": True}
    else:
        return {"spawn": 220, "vel": 0, "atira": True}

def desenhar_hud():
    screen.blit(font.render(f"Vida: {vida_player}", True, (255,255,255)), (20,20))
    screen.blit(font.render(f"Fase: {fase}", True, (255,255,255)), (20,50))
    screen.blit(font.render(f"Dano: x{power_dano}", True, (255,255,255)), (20,80))

    if boss_ativo:
        pygame.draw.rect(screen, (255,0,0), (400,20,400,20))
        pygame.draw.rect(screen, (0,255,0),
            (400,20,400*(boss_hp/boss_hp_max),20))

# ================== LOOP ==================
rodando = True
while rodando:
    clock.tick(60)
    cfg = config_fase(fase)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro = pygame.Rect(player.right, player.centery - 2, 12, 5)
                player_tiros.append(tiro)
                som_tiro.play()

    # -------- MOVIMENTO --------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.top > 0:
        player.y -= VEL_PLAYER
    if keys[pygame.K_s] and player.bottom < ALTURA:
        player.y += VEL_PLAYER
    if keys[pygame.K_a] and player.left > 0:
        player.x -= VEL_PLAYER
    if keys[pygame.K_d] and player.right < LARGURA:
        player.x += VEL_PLAYER

    # -------- SPAWN INIMIGOS --------
    spawn_timer += 1
    if spawn_timer >= cfg["spawn"] and not boss_ativo:
        spawn_timer = 0
        inimigos.append(
            pygame.Rect(LARGURA, random.randint(60, ALTURA-60), 48, 48)
        )

    # -------- INIMIGOS --------
    for inimigo in inimigos[:]:
        inimigo.x -= cfg["vel"]

        if cfg["atira"] and random.randint(0, 120) == 0:
            enemy_tiros.append(
                pygame.Rect(inimigo.left, inimigo.centery, 10, 4)
            )

        if inimigo.right < 0:
            inimigos.remove(inimigo)

    # -------- TIROS PLAYER --------
    for tiro in player_tiros[:]:
        tiro.x += VEL_TIRO_PLAYER + power_vel_tiro
        if tiro.left > LARGURA:
            player_tiros.remove(tiro)
            continue

        for inimigo in inimigos[:]:
            if tiro.colliderect(inimigo):
                inimigos.remove(inimigo)
                player_tiros.remove(tiro)
                kills += 1

                # chance de power-up
                if random.randint(0, 5) == 0:
                    power_dano += 1
                break

        if boss_ativo and tiro.colliderect(boss):
            boss_hp -= power_dano
            player_tiros.remove(tiro)

    # -------- TIROS INIMIGOS --------
    for tiro in enemy_tiros[:]:
        tiro.x -= VEL_TIRO_ENEMY
        if tiro.right < 0:
            enemy_tiros.remove(tiro)
        elif tiro.colliderect(player):
            vida_player -= 5
            enemy_tiros.remove(tiro)

    # -------- BOSS --------
    if fase in (5,10) and not boss_ativo:
        boss_ativo = True
        boss_hp_max = 180 if fase == 5 else 260
        boss_hp = boss_hp_max

    if boss_ativo:
        if random.randint(0, 40) == 0:
            enemy_tiros.append(
                pygame.Rect(boss.left, boss.centery, 14, 6)
            )

        if boss_hp <= 0:
            boss_ativo = False
            fase += 1
            kills = 0
            inimigos.clear()
            enemy_tiros.clear()

    # -------- AVANÇAR FASE --------
    if not boss_ativo and kills >= 10:
        fase += 1
        kills = 0
        inimigos.clear()
        enemy_tiros.clear()

    if vida_player <= 0:
        rodando = False

    # -------- RENDER --------
    screen.blit(fundo, (0,0))
    screen.blit(player_img, player)

    for inimigo in inimigos:
        screen.blit(enemy_img, inimigo)

    if boss_ativo:
        screen.blit(boss_img, boss)

    for tiro in player_tiros:
        pygame.draw.rect(screen, (0,255,255), tiro)

    for tiro in enemy_tiros:
        pygame.draw.rect(screen, (255,0,0), tiro)

    desenhar_hud()
    pygame.display.flip()

pygame.quit()
