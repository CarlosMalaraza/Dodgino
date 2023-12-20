import pygame
import serial
import sys
import random
import dataBaseDodgino 
import win32gui
import win32com.client
import time

nombre_usuario = input("Ingresa tu nombre de usuario: ")

# Configuración de la comunicación serial con Arduino
ser = serial.Serial('COM3', 9600)  # Reemplaza 'COMX' con el puerto correcto de tu Arduino

# Configuración de Pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size() # Obtiene las dimensiones de la pantalla

# Trae la ventana de Pygame al frente
HWND = pygame.display.get_wm_info()['window']
shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')
win32gui.SetForegroundWindow(HWND)

clock = pygame.time.Clock()

# Variables
player_speed = 15
player_size_x = 50
player_size_y = 50

obstacle_speed = 10
obstacle_size_x = 45
obstacle_size_y = 45

obstacle_timer_spawn = 75
speed_up_timer = 6000
obstacle_adittional_speed = 0.5

ally_size_x = 100
ally_size_y = 100
ally_timer_spawn = 2000
ally_speed = 10

final_score = 0

clock_time = 180

font = pygame.font.Font(None, 36)  # Crea el objeto "fuente"

background = pygame.image.load('backgroundRanking.png')
background = pygame.transform.scale(background,(screen_width,screen_height)) #Redimensiona a las dimensiones de pantalla

background_game_original = pygame.image.load('backgroundGame4.png')
background_game = pygame.transform.smoothscale(background_game_original, (screen_width, screen_height))

raking_position = 1

score = 0  # Inicializa la puntuación

# Player
player_image = pygame.image.load('player2.png')  # Carga la imagen del jugador
player_image = pygame.transform.scale(player_image, (player_size_x, player_size_y))  # Cambia el tamaño del sprite del jugador a 50x50
player_rect = player_image.get_rect()  # Obtiene el rectángulo de la imagen del jugador
player_rect.center = (screen_width // 2, screen_height - 50)  # Centra el jugador en la pantalla

collision_margin_x = 20  # Márgenes para reducir el tamaño del rectángulo en el eje X
collision_margin_y = 15  # Márgenes para reducir el tamaño del rectángulo en el eje Y
player_rect.inflate_ip(-collision_margin_x, -collision_margin_y)  # Reduce el tamaño del rectángulo de colisión

# Obstáculos
obstacle_event = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_event, obstacle_timer_spawn)  # Crea un nuevo obstáculo cada x milisegundos
obstacle_image = pygame.image.load('obstacle2.png')  # Carga la imagen del obstáculo
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_size_x, obstacle_size_y))
obstacles = []

obstacle_collision_margin_x = 20
obstacle_collision_margin_y = 15  



#Ally
ally_event = pygame.USEREVENT +2
pygame.time.set_timer(ally_event, ally_timer_spawn)  # Crea un nuevo ally cada x milisegundos
ally_image = pygame.image.load('ally.png')  # Carga la imagen del ally
ally_image = pygame.transform.scale(ally_image, (ally_size_x, ally_size_y))
allies = []


# Evento de temporizador para aumentar la velocidad de los obstáculos
speed_up_event = pygame.USEREVENT + 3
pygame.time.set_timer(speed_up_event, speed_up_timer)  # Aumenta la velocidad de los obstáculos cada x milisegundos

# Tiempo de juego, será la puntuación
start_time = pygame.time.get_ticks()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == obstacle_event:
            x = random.randrange(10, screen_width - obstacle_size_x)
            obstacles.append(pygame.Rect(x, -20, 20, 20))
        elif event.type == speed_up_event:
            obstacle_speed += obstacle_adittional_speed  # Aumenta la velocidad de los obstáculos
        elif event.type == ally_event:
            x = random.randrange(10, screen_width - ally_size_x)
            allies.append(pygame.Rect(x, -20, ally_size_x, ally_size_y))


    # Lectura del estado de los botones desde Arduino
    right_button_state, left_button_state = map(int, ser.readline().decode().strip().split(','))

    # Actualiza la puntuación basada en el tiempo de juego solo una vez
    time_based_score = (pygame.time.get_ticks() - start_time) // 1000

    # Mueve al jugador
    if right_button_state == 0:
        player_rect.x += player_speed
    elif left_button_state == 0:
        player_rect.x -= player_speed

    # Asegura que el jugador esté dentro de la pantalla
    player_rect.clamp_ip(screen.get_rect())

    # Mueve los obstáculos
    for obstacle in obstacles[:]:
        obstacle.y += obstacle_speed  # Los obstáculos caen a una velocidad mayor en cada iteración
        if obstacle.top > screen_height:
            obstacles.remove(obstacle)
        # Verifica si el jugador se ha chocado con el obstáculo

        if player_rect.colliderect(obstacle):
            ser.write(b'1')  # Envía '1' a Arduino para indicar que el jugador ha muerto
            final_score = time_based_score +score
            dataBaseDodgino.commit_score(nombre_usuario, final_score)
            final_ranking = dataBaseDodgino.get_score()
            y_position = 120

            #Dibujar las scores de la base de datos
            screen.blit(background, (0, 0))
            for rank, (name, score) in enumerate(final_ranking, start=1):
                player_info = f"{raking_position}. {name}: {score}"
                player_text = font.render(player_info, True, (0, 0, 0))
                
                screen.blit(player_text, (screen_width // 2 - 500, y_position))
                y_position += 60
                raking_position+=1

            pygame.display.flip()
            
            #Despues de dos segundos pausamos el juego
            time.sleep(2)
            clock_time=1 

            # Espera hasta que el jugador pulse una tecla para salir
            waiting_for_key = True
            while waiting_for_key:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        pygame.quit()
                        sys.exit()

    for ally in allies[:]:
        ally.y += ally_speed
        if ally.top > screen_height:
            allies.remove(ally)
        if player_rect.colliderect(ally):
            ser.write(b'2')
            score+=10
            allies.remove(ally)

    # Dibuja al jugador y los obstáculos en la pantalla
    screen.blit(background_game, (0, 0))
    screen.blit(player_image, player_rect)  # Dibuja la imagen del jugador en la pantalla
    for ally in allies:
        screen.blit(ally_image,ally)
        # pygame.draw.rect(screen, (0, 255, 0), ally, 2)  #Depuración de colliders
    for obstacle in obstacles:
        screen.blit(obstacle_image, obstacle)


    # Dibuja la puntuación actualizada
    score_text = font.render(f'Score: {time_based_score + score}', True, (0, 0, 0))
    screen.blit(score_text, (screen_width - 110, 10))

    pygame.display.flip()
    clock.tick(clock_time)  #180 fotogramas por segundo
