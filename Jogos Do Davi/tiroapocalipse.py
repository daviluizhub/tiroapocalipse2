# tiroapocalipse.py - Com Batedor, Game Over, Fases e Minigame Tiro
import pygame
import random
import sys
import os
import traceback

pygame.init()

# --- Helpers para paths ---
def get_base_path():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.abspath(".")

def write_log(msg):
    try:
        with open(os.path.join(get_base_path(), "error.log"), "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass

def load_image_safe(filename, scale=None, alpha=True):
    base = get_base_path()
    path = os.path.join(base, filename)
    try:
        img = pygame.image.load(path)
        if alpha:
            try:
                img = img.convert_alpha()
            except Exception:
                img = img.convert()
        else:
            img = img.convert()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except Exception as e:
        tb = traceback.format_exc()
        write_log(f"ERRO ao carregar imagem: {filename}  -> {e}\n{tb}")
        w, h = scale if scale else (64, 64)
        placeholder = pygame.Surface((w, h), pygame.SRCALPHA)
        placeholder.fill((255, 0, 0, 180))
        pygame.draw.line(placeholder, (255,255,255), (0,0), (w,h), 3)
        pygame.draw.line(placeholder, (255,255,255), (w,0), (0,h), 3)
        return placeholder

def criar_batedor_padrao(scale):
    """Cria um batedor padrão colorido"""
    w, h = scale
    batedor = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(batedor, (30, 150, 255), (0, 0, w, h))
    pygame.draw.rect(batedor, (100, 200, 255), (0, 0, w, h), 3)
    return batedor

# --- MINIGAME: TIRO APOCALIPSE ---
def minigame_tiro(tela_largura, tela_altura, surface, clock, font, font_large):
    """Minigame de tiro: acerte alvos em movimento"""
    alvos = []
    score = 0
    tempo_restante = 15  # 15 segundos
    tempo_inicial = pygame.time.get_ticks()
    minigame_running = True
    
    class Alvo:
        def __init__(self):
            self.x = random.randint(50, tela_largura - 100)
            self.y = random.randint(50, tela_altura - 200)
            self.vx = random.randint(-3, 3)
            self.vy = random.randint(-3, 3)
            self.size = 40
        
        def update(self):
            self.x += self.vx
            self.y += self.vy
            
            if self.x <= 0 or self.x >= tela_largura - self.size:
                self.vx = -self.vx
            if self.y <= 0 or self.y >= tela_altura - 150:
                self.vy = -self.vy
            
            self.x = max(0, min(self.x, tela_largura - self.size))
            self.y = max(0, min(self.y, tela_altura - 150))
        
        def draw(self, surface):
            pygame.draw.circle(surface, (255, 100, 100), (int(self.x + self.size//2), int(self.y + self.size//2)), self.size//2)
            pygame.draw.circle(surface, (255, 200, 200), (int(self.x + self.size//2), int(self.y + self.size//2)), self.size//2, 2)
        
        def colisao(self, mouse_x, mouse_y):
            dist = ((mouse_x - (self.x + self.size//2))**2 + (mouse_y - (self.y + self.size//2))**2)**0.5
            return dist < self.size // 2
    
    # Cria 5 alvos
    for _ in range(5):
        alvos.append(Alvo())
    
    # Loop do minigame
    while minigame_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, alvo in enumerate(alvos):
                    if alvo.colisao(mouse_x, mouse_y):
                        score += 1
                        alvos.pop(i)
                        alvos.append(Alvo())
                        break
        
        # Atualiza tempo
        tempo_passado = (pygame.time.get_ticks() - tempo_inicial) / 1000
        tempo_restante = max(0, 15 - tempo_passado)
        
        if tempo_restante <= 0 or score >= 10:
            minigame_running = False
        
        # Atualiza alvos
        for alvo in alvos:
            alvo.update()
        
        # Desenha
        surface.fill((40, 40, 60))
        
        # Desenha alvos
        for alvo in alvos:
            alvo.draw(surface)
        
        # Desenha interface
        score_text = font_large.render(f"Acertos: {score}/10", True, (0, 255, 100))
        surface.blit(score_text, (20, 20))
        
        tempo_text = font.render(f"Tempo: {tempo_restante:.1f}s", True, (255, 255, 0))
        surface.blit(tempo_text, (20, 80))
        
        instrucao = font.render("Clique nos alvos vermelhos!", True, (200, 200, 255))
        surface.blit(instrucao, (tela_largura // 2 - 200, tela_altura - 100))
        
        pygame.display.flip()
        clock.tick(60)
    
    return score

# --- Configurações da tela ---
surface = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Tiro Apocalipse - Destrua as Pedras!")

# --- Nomes dos assets ---
BALL_IMG = "41d9ogPJszL._AC_SY200_QL15_.jpg"
ROCHA_IMG = "rocha-cinzenta-isolada-em-fundo-transparente_632498-25568.jpg"
BATEDOR_IMG = "batedor.png"

# --- Carrega imagens ---
ball_img = load_image_safe(BALL_IMG, scale=(40, 40), alpha=True)
rocha_img = load_image_safe(ROCHA_IMG, scale=(80, 80), alpha=True)

# Tenta carregar batedor, se falhar cria um padrão
try:
    batedor_img = load_image_safe(BATEDOR_IMG, scale=(180, 30), alpha=True)
except:
    batedor_img = criar_batedor_padrao((180, 30))

# --- Som opcional ---
explosion_sound = None
try:
    expl_path = os.path.join(get_base_path(), "laserShoot.wav")
    if os.path.isfile(expl_path):
        explosion_sound = pygame.mixer.Sound(expl_path)
except Exception as e:
    write_log(f"Erro ao carregar som: {e}")

clock = pygame.time.Clock()
width = surface.get_width()
height = surface.get_height()
font = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 48)

# --- Funções para inicializar e gerar rochas ---
def criar_rochas_fase(fase):
    """Cria rochas baseado na fase do jogo"""
    rochas = []
    num_rochas = 6 + (fase - 1) * 2
    
    # Posições base para as 6 primeiras rochas
    posicoes_base = [
        (80, 60), (320, 60), (560, 60),
        (80, 200), (320, 200), (560, 200),
    ]
    
    # Adiciona as posições base
    for x, y in posicoes_base:
        if rocha_img:
            rocha_rect = rocha_img.get_rect()
            rocha_rect.x = x
            rocha_rect.y = y
            rochas.append(rocha_rect)
    
    # Adiciona rochas extras para fases posteriores
    for i in range(num_rochas - 6):
        if rocha_img:
            rocha_rect = rocha_img.get_rect()
            rocha_rect.x = random.randint(50, width - 130)
            rocha_rect.y = random.randint(50, 250)
            rochas.append(rocha_rect)
    
    return rochas

def inicializar_jogo(fase=1):
    """Inicializa um novo jogo ou inicia uma fase"""
    ball_rect = ball_img.get_rect()
    ball_rect.x = width // 2 - 20
    ball_rect.y = height // 2 - 20
    
    vel_x = 4 + (fase - 1)
    vel_y = -4 - (fase - 1)
    
    rochas = criar_rochas_fase(fase)
    
    # Batedor no centro inferior
    batedor_rect = batedor_img.get_rect()
    batedor_rect.centerx = width // 2
    batedor_rect.bottom = height - 10
    
    return ball_rect, vel_x, vel_y, rochas, batedor_rect

# --- Estado do jogo ---
running = True
game_over = False
fase = 1
pedras_iniciais = 0
vidas = 3
recompensas_desbloqueadas = []

ball_rect, vel_x, vel_y, rochas, batedor_rect = inicializar_jogo(fase)
pedras_iniciais = len(rochas)

# --- Loop principal ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reiniciar o jogo
                game_over = False
                fase = 1
                vidas = 3
                recompensas_desbloqueadas = []
                ball_rect, vel_x, vel_y, rochas, batedor_rect = inicializar_jogo(fase)
                pedras_iniciais = len(rochas)
    
    if not game_over:
        # --- Controlar batedor com mouse ---
        mouse_x, mouse_y = pygame.mouse.get_pos()
        batedor_rect.centerx = mouse_x
        if batedor_rect.left < 0:
            batedor_rect.left = 0
        if batedor_rect.right > width:
            batedor_rect.right = width
        
        # --- Movimento da bola ---
        ball_rect.x += vel_x
        ball_rect.y += vel_y
        
        # --- Rebater nas bordas ---
        if ball_rect.left <= 0 or ball_rect.right >= width:
            vel_x = -vel_x
        if ball_rect.top <= 0:
            vel_y = -vel_y
        
        # --- Colisão com batedor ---
        if ball_rect.colliderect(batedor_rect):
            vel_y = -abs(vel_y)
            ball_rect.y = batedor_rect.y - ball_rect.height
        
        # --- Game Over: bola cai ---
        if ball_rect.top > height:
            vidas -= 1
            if vidas > 0:
                # Reinicia posição da bola
                ball_rect.x = width // 2 - 20
                ball_rect.y = height // 2 - 20
                vel_x = 4 + (fase - 1)
                vel_y = -4 - (fase - 1)
            else:
                game_over = True
        
        # --- Checa colisão com rochas ---
        rochas_para_remover = []
        for i, rocha_rect in enumerate(rochas):
            if ball_rect.colliderect(rocha_rect):
                try:
                    if explosion_sound:
                        explosion_sound.play()
                except Exception as e:
                    write_log(f"Erro ao tocar som: {e}")
                rochas_para_remover.append(i)
                vel_x = -int(vel_x * 1.05) if abs(vel_x) > 0 else -vel_x
                vel_y = -int(vel_y * 1.05) if abs(vel_y) > 0 else -vel_y
        
        # Remove rochas destruídas
        for i in reversed(rochas_para_remover):
            rochas.pop(i)
        
        # --- Próxima fase se destruir todas as rochas ---
        if len(rochas) == 0:
            # ATIVA MINIGAME!
            score_minigame = minigame_tiro(width, height, surface, clock, font, font_large)
            
            recompensas_desbloqueadas.append(f"Fase {fase}: {score_minigame}/10 acertos!")
            
            if score_minigame >= 5:
                vidas += 1  # Recompensa: vida extra
            
            fase += 1
            ball_rect, vel_x, vel_y, rochas, batedor_rect = inicializar_jogo(fase)
            pedras_iniciais = len(rochas)
    
    # --- Desenho ---
    surface.fill((30, 30, 40))
    
    # Desenha bola
    if ball_img:
        surface.blit(ball_img, ball_rect)
    
    # Desenha rochas
    if rocha_img:
        for rocha_rect in rochas:
            surface.blit(rocha_img, rocha_rect)
    
    # Desenha batedor com destaque
    if batedor_img:
        surface.blit(batedor_img, batedor_rect)
        pygame.draw.rect(surface, (100, 255, 150), batedor_rect, 3)
    
    # --- Informações na tela ---
    pedras_restantes = len(rochas)
    info_text = font.render(f"Fase: {fase} | Pedras: {pedras_restantes}/{pedras_iniciais} | Vidas: {vidas}", True, (255, 255, 255))
    surface.blit(info_text, (10, 10))
    
    # --- Tela de Game Over ---
    if game_over:
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        game_over_text = font_large.render("GAME OVER!", True, (255, 50, 50))
        text_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 80))
        surface.blit(game_over_text, text_rect)
        
        fase_text = font.render(f"Fase alcançada: {fase}", True, (255, 255, 100))
        fase_rect = fase_text.get_rect(center=(width // 2, height // 2 - 20))
        surface.blit(fase_text, fase_rect)
        
        # Mostra recompensas
        if recompensas_desbloqueadas:
            recompensas_text = font.render(f"Recompensas: {len([r for r in recompensas_desbloqueadas if '5' in r or '6' in r or '7' in r or '8' in r or '9' in r or '10' in r])} vidas ganhas!", True, (100, 255, 100))
            recompensas_rect = recompensas_text.get_rect(center=(width // 2, height // 2 + 20))
            surface.blit(recompensas_text, recompensas_rect)
        
        restart_text = font.render("Pressione R para reiniciar", True, (150, 255, 150))
        restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 80))
        surface.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
