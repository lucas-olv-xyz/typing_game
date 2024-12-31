import pygame
import random
import sys

pygame.init()
#no game over mostrar qual rapido  a sua cadencia de palavras foi, WPM

#tela
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
GREEN = (172,212,115)
BLACK = (55,54,53)
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
running = True
tela = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Type Magus')
user_input = ""
monster_alive = True
vidas = 3

#------------------PERSONAGEM---------------------------------
player_img = pygame.image.load('h1.png')
width, height = player_img.get_size()
player_rect = player_img.get_rect()
#posição na tela
#PEGAMOS A LARGURA E A ALTURA TOTAL DA TELA E DIVIDIMOS POR 2, ESSE E O CENTRO DA TELA
x_pos = (WINDOW_WIDTH - width) // 2
y_pos = (WINDOW_HEIGHT - height) // 2
player_rect.center = (x_pos,y_pos)
side = random.randint(0,3)# 0=esq, 1=dir, 2=top, 3=bottom

#-------------------------ANIMAÇÕES-------------------------------
player_idle_frames = [pygame.image.load('h1.png'),pygame.image.load('h2.png'),pygame.image.load('h3.png')]
enemy_idle_frames = [pygame.image.load('e1.png'),pygame.image.load('e2.png'),pygame.image.load('e3.png')]

#-------------------TELA INICIAL------------------------------------
def show_start_screen():
    start_running = True
    while start_running:
        tela.fill(GREEN)
        
        title_text = font.render("Type Mosquito", True, (BLACK))
        instruction_text = font.render("Pressione ENTER para começar", True, (BLACK))
        
        tela.blit(title_text, (WINDOW_WIDTH//2-80, WINDOW_HEIGHT//2-50))
        tela.blit(instruction_text, (WINDOW_WIDTH//2-180, WINDOW_HEIGHT//2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                start_running = False

#-------------------SPAWN DE MONSTROS ALEATORIOS-----------------------------
def spawn_monster():
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
    
    #rect acompanha a localização dos mobs    
    monster_rect.x = x
    monster_rect.y = y
    
    #DICIONARIO DE PALAVRAS
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
    monster_word = random.choice(words_easy)
    
    if score < 40:
        monster_word = random.choice(words_easy)
    elif score < 60:
        monster_word = random.choice(words_medium)
    else:
        monster_word = random.choice(words_hard)
    
    return {
        "x":x,
        "y":y,
        "img":monster_img,
        "rect":monster_rect,
        "word":monster_word,
        "alive":True,
    }

#---------------------GAME OVER--------------------------------------
def Gamer_over_screen(score):
    over_running = True
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

show_start_screen()

#LOOP
while running:
    clock.tick(60)
    speed = 0.2
    # 1) Limpa a tela
    tela.fill(GREEN)

    # 2) Desenha o player
    player_img = player_idle_frames[player_current_frame]
    tela.blit(player_img, (x_pos,y_pos))
    animation_counter += 1

    # 8) Desenha o texto digitado
    texto_digitado = font.render(user_input, True, (BLACK))
    score_text = font.render(f"Score: {score}", True, (BLACK))
    vidas_texto = font.render(f'vidas: {vidas}', True, (BLACK))
    tela.blit(texto_digitado, (x_pos, y_pos - 30))
    tela.blit(score_text, (10,10))
    tela.blit(vidas_texto, (10,40))
    
    spawn_timer += 1
    spawn_interval = 120
    
    if animation_counter > animation_speed:
        animation_counter = 0
        player_current_frame += 1
        if player_current_frame >= len(player_idle_frames):
            player_current_frame = 0
    
    if score >= 30:
        spawn_interval = 90
        speed = 0.4
    if score >= 50:
        spawn_interval = 60
        speed = 1.5
    
    if spawn_timer > spawn_interval:
        monsters.append(spawn_monster())
        spawn_timer = 0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                for monstro in monsters:
                    if monstro['alive'] and user_input.lower() == monstro['word'].lower():
                        monstro['alive'] = False
                        score += 1 
                        
                user_input = ""
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode
                
    animation_timer +=1 
    #COMPORTAMENTO DOS MONSTROS
    for monstro in monsters:
        if monstro["alive"]:
            dx = x_pos - monstro["x"]
            dy = y_pos - monstro["y"]
            dist = (dx**2 + dy**2) ** 0.5

            if dist != 0:
                dx_norm = dx / dist
                dy_norm = dy / dist

                monstro["x"] += dx_norm * speed
                monstro["y"] += dy_norm * speed

            if monstro['alive'] and player_rect.colliderect(monstro['rect']):
                vidas -= 1
                monstro['alive'] = False
            if vidas <= 0:
                Gamer_over_screen(score)
                running = False

            # Atualizar rect
            monstro["rect"].x = monstro["x"]
            monstro["rect"].y = monstro["y"]
            
            
            
            if animation_timer > 10:  # a cada 10 frames
                enemy_idle_index = (enemy_idle_index + 1) % len(enemy_idle_frames)
                animation_timer = 0  
                    
         
            
            tela.blit(enemy_idle_frames[enemy_idle_index], (monstro['x'],monstro['y']))
            
            texto_monstro = font.render(monstro['word'], True, (BLACK))
            tela.blit(texto_monstro, (monstro['x'],monstro['y'] - 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
