import pygame
import random
import os
import sys

# =========================
# CONFIGURAÇÕES
# =========================

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    pass

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiro Apocalipse 2")
clock = pygame.time.Clock()

# =========================
# CAMINHO DOS ARQUIVOS
# =========================

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# =========================
# CARREGAR IMAGENS
# =========================

player_img = pygame.image.load(resource_path("player.png")).convert_alpha()
enemy_img = pygame.image.load(resource_path("enemy.png")).convert_alpha()
boss_img = pygame.image.load(resource_path("boss.png")).convert_alpha()
bullet_img = pygame.image.load(resource_path("tiro.png")).convert_alpha()
background = pygame.image.load(resource_path("fundo.jpg")).convert()

laser_sound = None
try:
    laser_sound = pygame.mixer.Sound(resource_path("laserShoot.wav"))
except pygame.error:
    laser_sound = None

# =========================
# ARMAS
# =========================

WEAPONS = {
    1: ("Basica", 15),
    2: ("Outono", 20),
    3: ("Chocolate", 25),
    4: ("Pascoa", 30),
    5: ("Dia das Maes", 35),
    6: ("Blocks", 40),
    7: ("Mes dos Namorados", 50),
    8: ("Copa", 60),
    9: ("Dia dos Pais", 70)
}


def get_weapon_id(phase):
    if phase >= 10:
        return 7
    if phase >= 8:
        return 5
    if phase >= 7:
        return 4
    if phase >= 5:
        return 3
    if phase >= 3:
        return 2
    if phase >= 2:
        return 6
    return 1


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 70))
        self.speed = 6
        self.life = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        self.rect.clamp_ip(screen.get_rect())


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, damage):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -12
        self.damage = damage

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -40)
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self, phase):
        super().__init__()
        self.image = boss_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, 100))
        self.hp = 200 + phase * 20
        self.max_hp = self.hp
        self.speed = 3
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1


# =========================
# GRUPOS
# =========================

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
boss_group = pygame.sprite.GroupSingle()

player = Player()
all_sprites.add(player)

# =========================
# VARIÁVEIS DO JOGO
# =========================

score = 0
phase = 1
weapon = get_weapon_id(phase)
weapon_name, weapon_damage = WEAPONS[weapon]

boss_active = False
running = True
font = pygame.font.SysFont("arial", 30)

game_over = False

# =========================
# LOOP PRINCIPAL
# =========================

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullet = Bullet(player.rect.centerx, player.rect.top, weapon_damage)
                all_sprites.add(bullet)
                bullets.add(bullet)
                if laser_sound:
                    laser_sound.play()

            if event.key == pygame.K_r and game_over:
                score = 0
                phase = 1
                player.life = 100
                boss_active = False
                game_over = False
                for sprite in all_sprites:
                    if sprite is not player:
                        sprite.kill()

            if event.key == pygame.K_1:
                weapon = 1
            elif event.key == pygame.K_2:
                weapon = 2
            elif event.key == pygame.K_3:
                weapon = 3
            elif event.key == pygame.K_4:
                weapon = 4
            elif event.key == pygame.K_5:
                weapon = 5
            elif event.key == pygame.K_6:
                weapon = 6
            elif event.key == pygame.K_7:
                weapon = 7
            elif event.key == pygame.K_8:
                weapon = 8
            elif event.key == pygame.K_9:
                weapon = 9

    if not game_over:
        weapon = max(weapon, get_weapon_id(phase))
        weapon_name, weapon_damage = WEAPONS[weapon]

        all_sprites.update()

        if random.random() < 0.03 and not boss_active:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        if phase >= 10 and not boss_active:
            boss = Boss(phase)
            all_sprites.add(boss)
            boss_group.add(boss)
            boss_active = True

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        score += len(hits) * 20

        if boss_active:
            boss_hits = pygame.sprite.groupcollide(boss_group, bullets, False, True)
            for boss in boss_hits:
                boss.hp -= weapon_damage
                if boss.hp <= 0:
                    boss.kill()
                    boss_active = False
                    phase += 1
                    score += 1000

        if pygame.sprite.spritecollide(player, enemies, True):
            player.life -= 10
            if player.life <= 0:
                game_over = True

        if score > phase * 800:
            phase += 1

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    weapon_name, weapon_damage = WEAPONS[weapon]
    screen.blit(font.render(f"Arma: {weapon_name} (Dano: {weapon_damage})", True, WHITE), (10, 10))
    screen.blit(font.render(f"Fase: {phase}", True, WHITE), (10, 45))
    screen.blit(font.render(f"Pontos: {score}", True, WHITE), (10, 80))
    screen.blit(font.render(f"Vida: {player.life}", True, WHITE), (10, 115))

    if boss_active:
        boss = boss_group.sprite
        if boss:
            screen.blit(font.render(f"Boss HP: {boss.hp}/{boss.max_hp}", True, RED), (WIDTH // 2 - 120, 10))

    if game_over:
        go_text = font.render("GAME OVER - Pressione R para reiniciar", True, RED)
        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
