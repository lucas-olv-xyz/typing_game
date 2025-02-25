import pygame
import random
import sys

pygame.init()
#no game over mostrar qual rapido  a sua cadencia de palavras foi, WPM

#tela
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
GREEN = (224,248,207)
BLACK = (55,54,53)
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
running = True
tela = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Type Magus')
user_input = ""
monster_alive = True
vidas = 3

menu_music = "sounds/telainicial.mp3"
game_music = "sounds/somgame.mp3"
over_music = "sounds/gameover.mp3"

words_easy = ["A", "B", "C", "D", "E", "F", 
    "G", "H", "I", "J", "K", "L", 
    "M", "N", "O", "P", "Q", "R", 
    "S", "T", "U", "V", "W", "X", 
    "Y", "Z"]
    
words_medium = [ "ABACAXI", "BOLA", "CACHORRO", "DINOSSAURO", "ELEFANTE", "FLORESTA", 
    "GATO", "HIPOPOTAMO", "IGLU", "JOGADOR", "KIWI", "LIVRO", 
    "MACACO", "NAVIO", "OVELHA", "PINGUIM", "QUEIJO", "RATO", 
    "SAPATO", "TIGRE", "URSO", "VIOLINO", "WAFFLE", "XAROPE", 
    "YOGA", "ZEBRA"]
    
words_hard = [ "ARQUIPELAGO", "BIBLIOTECA", "CATASTROFICO", "DESENVOLVIMENTO", 
    "ELETRONICO", "FOTOSSINTETICO", "GEOMETRICO", "HIERARQUIA", 
    "IMPOSSIBILIDADE", "JURISPRUDENCIA", "KILOMETRAGEM", "LABIRINTICO", 
    "METAMORFOSE", "NEUROLOGICO", "ORNITOLOGIA", "PROCRASTINACAO", 
    "QUIMERICO", "REVOLUCIONARIO", "SIMETRICO", "TRANSCENDENTAL", 
    "UNIVERSALIDADE", "VEROSSIMILHANCA", "WESTERNIANO", "XILOFONISTA", 
    "YOUTUBERS", "ZUMBIFICADO"]
#------------------PERSONAGEM---------------------------------
player_img = pygame.image.load('p1.png')
width, height = player_img.get_size()
player_rect = player_img.get_rect()
#posição na tela
#PEGAMOS A LARGURA E A ALTURA TOTAL DA TELA E DIVIDIMOS POR 2, ESSE E O CENTRO DA TELA
x_pos = (WINDOW_WIDTH - width) // 2
y_pos = (WINDOW_HEIGHT - height) // 2
player_rect.center = (x_pos,y_pos)
side = random.randint(0,3)# 0=esq, 1=dir, 2=top, 3=bottom

#-------------------------ANIMAÇÕES-------------------------------
enemy_type_1 = [
    pygame.image.load('e1.png'),
    pygame.image.load('e2.png'),
]
enemy_type_2 = [
    pygame.image.load('e3.png'),
    pygame.image.load('e4.png'),
]
enemy_type_3 = [
    pygame.image.load('e5.png'),
    pygame.image.load('e6.png'),
]
enemy_type_4 = [
    pygame.image.load('e7.png'),
    pygame.image.load('e8.png'),
]
player_idle_frames = [pygame.image.load('p1.png'),pygame.image.load('p2.png')]
enemy_idle_frames = [pygame.image.load('e1.png'),pygame.image.load('e2.png')]

#-------------------TELA INICIAL------------------------------------
def show_start_screen_with_difficulty():
    start_running = True
    selected_difficulty = None
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)
    
    while start_running:
        tela.fill(GREEN)
        
        title_text = font.render("Type Mosquito", True, (BLACK))
        instruction_text = font.render("Escolha a Dificuldade:", True, (BLACK))
        easy_text = font.render("1 - Fácil (letras / monstro lento)", True, (BLACK))
        medium_text = font.render("2 - Médio (palavras curtas / monstro médio)", True, (BLACK))
        hard_text = font.render("3 - Difícil (palavras grandes / monstro rápido)", True, (BLACK))
        
        # Desenha os textos na tela
        tela.blit(title_text, (WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2 - 150))
        tela.blit(instruction_text, (WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 - 100))
        tela.blit(easy_text, (WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 - 40))
        tela.blit(medium_text, (WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 + 0))
        tela.blit(hard_text, (WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 + 40))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_difficulty = "easy"
                    start_running = False
                elif event.key == pygame.K_2:
                    selected_difficulty = "medium"
                    start_running = False
                elif event.key == pygame.K_3:
                    selected_difficulty = "hard"
                    start_running = False

    pygame.mixer.music.stop()

    return selected_difficulty
selected_difficulty = show_start_screen_with_difficulty()
#--------------------------------------------------------------------

#-------------------SPAWN DE MONSTROS ALEATORIOS-----------------------------
def spawn_monster():
    enemy_types = [enemy_type_1,enemy_type_2,enemy_type_3,enemy_type_4]
    selected_frames = random.choice(enemy_types)
    
    monster_img = enemy_idle_frames[0]
    monster_rect = monster_img.get_rect()
    
    side = random.randint(0, 3)
    if side == 0: #esquerda
        x = 0
        y = random.randint(0, WINDOW_HEIGHT)
    elif side == 1: #direita
        x = WINDOW_WIDTH
        y = random.randint(0, WINDOW_HEIGHT)
    elif side == 2: #cima
        x = random.randint(0,WINDOW_WIDTH)
        y = 0
    else: #baixo
        x = random.randint(0,WINDOW_WIDTH)
        y = WINDOW_HEIGHT
    
    monster_rect.x = x
    monster_rect.y = y
    
    # Dependendo da dificuldade selecionada, sorteie do array correspondente
    if selected_difficulty == "easy":
        monster_word = random.choice(words_easy)
    elif selected_difficulty == "medium":
        monster_word = random.choice(words_medium)
    else:  # "hard"
        monster_word = random.choice(words_hard)
    
    return {
        "x": x,
        "y": y,
        "img": monster_img,
        "rect": monster_rect,
        "word": monster_word,
        "alive": True,
        "frames": selected_frames,
        "current_frame": 0,
        "anim_timer": 0,
    }
#--------------------------------------------------------------------

#---------------------GAME OVER--------------------------------------
def Gamer_over_screen(score):
    over_running = True
    pygame.mixer.music.load(over_music)
    pygame.mixer.music.play(1)
    
    while over_running:
        tela.fill((GREEN))
        
        game_over_text = font.render("GAME OVER", True ,
                                     (BLACK))
        score_final_text = font.render(f"Score Final: {score}", True, (BLACK))
        continuer_text = font.render('Pressione ENTER para sair', True, (BLACK))
        
        tela.blit(game_over_text, (WINDOW_WIDTH//2-80, WINDOW_HEIGHT//2-50))
        tela.blit(score_final_text, (WINDOW_WIDTH//2-80, WINDOW_HEIGHT//2))
        tela.blit(continuer_text, (WINDOW_WIDTH//2-120, WINDOW_HEIGHT//2+50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                sys.exit()
#--------------------------------------------------------------------

monsters = []
score = 0
# for _ in range(5):
#     monsters.append(spawn_monster())
spawn_timer = 0
animation_counter = 0
animation_speed = 10
player_current_frame = 0
enemy_current_frame = 0
animation_timer = 0
enemy_idle_index = 0

pygame.mixer.music.load(game_music)
pygame.mixer.music.play(-1)

while running:
    clock.tick(60)
    
    if selected_difficulty == "easy":
        base_speed = 0.2
        spawn_interval = 120
    elif selected_difficulty == "medium":
        base_speed = 0.3
        spawn_interval = 110
    else:  # hard
        base_speed = 0.4
        spawn_interval = 100

    # Você pode ajustar a velocidade com base na pontuação, se desejar:
    speed = base_speed + (score * 0.01)
    
    # 1) Limpa a tela
    tela.fill(GREEN)
    
    # 2) Desenha o jogador usando o retângulo já configurado (garanta que a imagem e o retângulo estejam alinhados)
    player_img = player_idle_frames[player_current_frame]
    tela.blit(player_img, player_rect.topleft)
    animation_counter += 1
    
    if animation_counter > animation_speed:
        animation_counter = 0
        player_current_frame = (player_current_frame + 1) % len(player_idle_frames)
    
    # 3) Desenha os textos de interface
    texto_digitado = font.render(user_input, True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    vidas_texto = font.render(f"Vidas: {vidas}", True, BLACK)
    tela.blit(texto_digitado, (x_pos, y_pos - 30))
    tela.blit(score_text, (10, 10))
    tela.blit(vidas_texto, (10, 40))
    
    # 4) Atualiza o temporizador de spawn e cria novos inimigos se necessário
    spawn_timer += 1
    if spawn_timer > spawn_interval:
        monsters.append(spawn_monster())
        spawn_timer = 0
    
    # 5) Processa eventos (incluindo digitação)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode
                # Verifica imediatamente se o texto digitado bate com a palavra de algum inimigo
                for monstro in monsters:
                    if monstro['alive'] and user_input.lower() == monstro['word'].lower():
                        monstro['alive'] = False
                        score += 1
                        user_input = ""  # reseta a digitação
                        break  # elimina apenas um inimigo por vez
    
    # 6) Atualiza o comportamento de cada inimigo
    for monstro in monsters:
        if monstro["alive"]:
            # Cálculo do vetor de movimento em direção ao centro do jogador
            dx = player_rect.centerx - monstro["x"]
            dy = player_rect.centery - monstro["y"]
            dist = (dx**2 + dy**2) ** 0.5
            if dist != 0:
                dx_norm = dx / dist
                dy_norm = dy / dist
                monstro["x"] += dx_norm * speed
                monstro["y"] += dy_norm * speed

            # Atualiza a posição do retângulo para a colisão
            monstro["rect"].x = monstro["x"]
            monstro["rect"].y = monstro["y"]
            
            # Verifica colisão com o jogador
            if player_rect.colliderect(monstro["rect"]) and vidas > 0:
                vidas -= 1
                monstro["alive"] = False
            
            if vidas <= 0:
                vidas = 0
                pygame.mixer.music.stop()
                Gamer_over_screen(score)
                running = False
            
            # Atualiza a animação individual do inimigo
            monstro["anim_timer"] += 1
            if monstro["anim_timer"] > 10:  # troca de frame a cada 10 frames
                monstro["current_frame"] = (monstro["current_frame"] + 1) % len(monstro["frames"])
                monstro["anim_timer"] = 0
            
            # Desenha o inimigo com o frame atual do seu conjunto de sprites
            tela.blit(monstro["frames"][monstro["current_frame"]], (monstro["x"], monstro["y"]))
            
            # Desenha a palavra do inimigo acima dele
            texto_monstro = font.render(monstro["word"], True, BLACK)
            tela.blit(texto_monstro, (monstro["x"], monstro["y"] - 20))

        
    pygame.display.flip()

pygame.quit()
sys.exit()
