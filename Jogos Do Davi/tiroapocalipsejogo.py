import pygame
import sys
import os
import random

# === FUNÇÃO OBRIGATÓRIA PARA PYINSTALLER --ONEFILE ===
def resource_path(relative_path):
    """Retorna caminho correto para assets (funciona rodando .py ou .exe)"""
    try:
        # Pasta temporária criada pelo PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Quando roda normalmente com python
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Inicializa Pygame
pygame.init()
pygame.mixer.init()

# Configurações da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiro Apocalipse - v1.0.3 ")
clock = pygame.time.Clock()
FPS = 60

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
 
# Carrega assets com resource_path (todos os arquivos que existem na pasta)
player_img = pygame.image.load(resource_path("player.png")).convert_alpha()
enemy_img   = pygame.image.load(resource_path("enemy.png")).convert_alpha()
boss_img    = pygame.image.load(resource_path("boss.png")).convert_alpha()
laser_img   = pygame.image.load(resource_path("tiro.png")).convert_alpha()

laser_sound = pygame.mixer.Sound(resource_path("laserShoot.wav"))

# Fundos reais que existem na tua pasta (9 fundos + reuse do último para fase 10+)
backgrounds = [
    pygame.image.load(resource_path("fundo.jpg")).convert(),   # 1
    pygame.image.load(resource_path("fundo2.jpg")).convert(),
    pygame.image.load(resource_path("fundo3.jpg")).convert(),
    pygame.image.load(resource_path("fundo4.jpg")).convert(),
    pygame.image.load(resource_path("fundo5.jpg")).convert(),
    pygame.image.load(resource_path("fundo6.jpg")).convert(),
    pygame.image.load(resource_path("fundo7.jpg")).convert(),
    pygame.image.load(resource_path("fundo8.jpg")).convert(),
    pygame.image.load(resource_path("fundo9.png")).convert(),  # 9
    pygame.image.load(resource_path("fundo9.png")).convert()   # 10+ (reuso do fundo9)
   
   

]

obby = [
    pygame.Rect(250,450,120,20),
    pygame.Rect(450,350,120,20),
    pygame.Rect(650,250,120,20)
]

# Classes do jogo
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        self.speed = 6
        self.lives = 100

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
        
        # Não sair da tela
        self.rect.clamp_ip(screen.get_rect())

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = laser_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -12

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), random.randint(-150, -40)))
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boss_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, 120))
        self.hp = 190          # Valor da update 1.0.2
        self.max_hp = 190
        self.speed = 3
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1

# Grupos de sprites
all_sprites = pygame.sprite.Group()
lasers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
boss_group = pygame.sprite.GroupSingle()

player = Player()
all_sprites.add(player)

# Variáveis do jogo
current_phase = 1
score = 0
boss_active = False
game_over = False
font = pygame.font.SysFont("arial", 36)

WEAPONS = {
    1: ("Basica", 15),
    2: ("Outono", 20),
    3: ("Chocolate", 25),
    4: ("Pascoa", 30),
    5: ("Dia das Maes", 35),
    6: ("Blocks", 40),
    7: ("Mes dos Namorados", 50)
}

weapon = 1

if current_phase >= 2:
    weapon = max(weapon, 6)

if current_phase >= 3:
    weapon = max(weapon, 2)

if current_phase >= 5:
    weapon = max(weapon, 3)

if current_phase >= 7:
    weapon = max(weapon, 4)

if current_phase >= 8:
    weapon = max(weapon, 5)

if current_phase >= 10:
    weapon = max(weapon, 7)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                laser = Laser(player.rect.centerx, player.rect.top)
                all_sprites.add(laser)
                lasers.add(laser)
                laser_sound.play()
            if event.key == pygame.K_r and game_over:  # Restart
                # Reset simples
                current_phase = 1
                score = 0
                player.lives = 100
                boss_active = False
                game_over = False
                for s in all_sprites:
                    if s != player:
                        s.kill()

    if not game_over:
        all_sprites.update()

        # Spawn inimigos normais
        if random.random() < 0.035 and not boss_active:  # chance por frame
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Ativa boss na fase 10
        if current_phase >= 10 and not boss_active:
            boss = Boss()
            all_sprites.add(boss)
            boss_group.add(boss)
            boss_active = True
            boss.hp = 210 + (current_phase * 25)
            boss.max_hp = boss.hp
            
        # Colisões tiros vs inimigos
        hits = pygame.sprite.groupcollide(enemies, lasers, True, True)
        for _ in hits:
            score += 20

        # Colisões tiros vs boss
        if boss_active:
            boss_hits = pygame.sprite.groupcollide(boss_group, lasers, False, True)
            for boss in boss_hits:
                boss.hp -= 15  # dano por tiro (ajuste o valor)
                if boss.hp <= 0:
                    boss.kill()
                    boss_active = False
                    current_phase += 1
                    score += 1000

        # Inimigos colidem com player
        if pygame.sprite.spritecollide(player, enemies, True):
            player.lives -= 25
            if player.lives <= 0:
                game_over = True

        # Avança fase por pontos (exemplo)
        if score > current_phase * 800:
            current_phase += 1

    #
      
    screen.blit(font.render(
    f"Arma: {WEAPONS[weapon][0]}",
    True,
    WHITE
), (10,130)) 
     
    

    if boss_active:
        screen.blit(font.render(f"Boss HP: {boss.hp}/{boss.max_hp}", True, RED), (WIDTH//2 - 120, 10))
    #  Desenho
    bg_index = min(current_phase - 1, len(backgrounds) - 1)
    screen.blit(backgrounds[bg_index], (0, 0))
    all_sprites.draw(screen)

    screen.blit(font.render(f"Fase: {current_phase}", True, WHITE), (10,10))
    screen.blit(font.render(f"Pontos: {score}", True, WHITE), (10,50))
    screen.blit(font.render(f"Vida: {player.lives}", True, WHITE), (10,90))

    if game_over:
        go_text = font.render("GAME OVER - Pressione R para reiniciar", True, RED)
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2))

    pygame.display.flip()

pygame.quit()
sys.exit()
 