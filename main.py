# Example file showing a basic pygame "game loop"
import pygame
import random
import math
from pygame.sprite import Group
from modules.classes.projectile import Projectile
from modules.classes.enemy import Enemy
from modules.classes.variables import *
from modules.helper.playership import PlayerShip
from modules.helper.enemyship import EnemyShip

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space pirates ~ Mo (Github: @1Hanif1)")

icon = pygame.image.load("Assets/Images/alien_ship.png")
pygame.display.set_icon(icon)

shoot = pygame.mixer.Sound(f"{AUDIO_SRC}/jet-fire.wav")
enemy_down = pygame.mixer.Sound(f"{AUDIO_SRC}/enemy-beaten.wav")
game_over = pygame.mixer.Sound(f"{AUDIO_SRC}/game-over.wav")

clock = pygame.time.Clock()

player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
font = pygame.font.Font(
    './Assets/Font/PressStart2P-regular.ttf',
    GAME_FONT_SIZE
)

background_image = pygame.image.load("./Assets/Images/bg.jpg")
background_image = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
)


try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.readline())
except FileNotFoundError:
    high_score = 0
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))


def create_number_of_enemies(enemy_rows, enemy_columns, enemy_spacing):
    global first_enemy_x, first_enemy_y

    for row in range(enemy_rows):
        for column in range(enemy_columns):
            enemy_positions.append((first_enemy_x, first_enemy_y))
            first_enemy_x += enemy_spacing

        first_enemy_y += (enemy_spacing - 20)
        first_enemy_x = 30


create_number_of_enemies(ENEMY_ROWS, ENEMY_COLUMNS, ENEMY_SPACING)


def render_score_card(screen):
    global font

    # Current Score
    text_surface = font.render(f"Score: {player_score}", True, FONT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.center = (SCREEN_WIDTH / 6, 10)
    screen.blit(text_surface, text_rect)

    # High Score
    text_surface = font.render(
        f"High Score: {high_score if high_score > player_score else player_score}", True, FONT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.center = (SCREEN_WIDTH / 2, 10)
    screen.blit(text_surface, text_rect)

    # Number of Rounds
    text_surface = font.render(f"Round: {player_round + 1}", True, FONT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.center = (SCREEN_WIDTH / 2 + SCREEN_WIDTH / 3, 10)
    screen.blit(text_surface, text_rect)


def update_high_score():
    global high_score

    if high_score > player_score:
        return

    high_score = player_score
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))


def create_enemies():
    global num_of_enemies
    for positions in enemy_positions:
        (pos_x, pos_y) = positions
        # enemy_pos = pygame.Vector2(pos_x, pos_y)
        new_enemy = Enemy(pos_x, pos_y)
        enemies.append(new_enemy)

    num_of_enemies = len(enemy_positions)


create_enemies()


def move_enemies_sideways():
    global enemies_move_forward, enemies, screen

    for enemy in enemies:
        # pygame.draw.circle(
        #     screen,
        #     ENEMY_COLOR,
        #     (int(enemy.pos.x), int(enemy.pos.y)),
        #     5
        # )

        ship = EnemyShip(enemy_pos=enemy.pos)
        ship.draw(screen)

        if enemies_move_forward:
            enemy.move_forward_x(dt)
        else:
            enemy.move_backward_x(dt)


def change_enemy_movement_state():
    global enemies_move_forward, enemies_move_downward, enemies

    for enemy in enemies:
        if enemy.pos.x >= SCREEN_WIDTH:
            enemies_move_forward = False
            enemies_move_downward = True
            break
        elif enemy.pos.x <= 0:
            enemies_move_forward = True
            enemies_move_downward = True
            break


def move_enemies_downwards():
    global enemies_move_downward, enemies

    if enemies_move_downward:
        for enemy in enemies:
            enemy.move_down_y(dt)
        enemies_move_downward = False


def check_enemy_projectile_collision(enemy_projectiles, player_pos):
    for projectile in enemy_projectiles:
        if player_pos.distance_to(projectile.pos) < (PLAYER_SIZE + 5):
            return True


def check_enemy_passed_player(player_pos, enemies):
    for enemy in enemies:
        if enemy.pos.y >= player_pos.y:
            return True


def reset_game():
    global ENEMY_ROWS, ENEMY_COLUMNS, ENEMY_SPACING, enemies, projectiles, enemy_projectiles, player_score, first_enemy_x, first_enemy_y, enemy_positions, num_of_enemies, player_round
    enemies.clear()
    projectiles.clear()
    enemy_projectiles.clear()
    player_score = 0
    first_enemy_x = 30
    first_enemy_y = 30
    enemy_positions = []
    num_of_enemies = 0
    ENEMY_ROWS = 1
    ENEMY_COLUMNS = 1
    player_round = 0
    reset_enemy_positions()
    create_number_of_enemies(ENEMY_ROWS, ENEMY_COLUMNS, ENEMY_SPACING)
    create_enemies()
    pass


def render_start_page():
    global high_score
    # Intro Image
    logo_image = pygame.image.load("./Assets/Images/logo.png")
    logo_image = pygame.transform.scale(
        logo_image, (300, 300)
    )
    # Start
    font_start = pygame.font.Font(
        './Assets/Font/PressStart2P-regular.ttf', MENU_FONT_SIZE)
    start_text_surface = font_start.render(
        "Press Space to Start", True, FONT_COLOR)
    start_text_rect = start_text_surface.get_rect()
    start_text_rect.center = (
        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 8)

    # High Score
    font_start = pygame.font.Font(
        './Assets/Font/PressStart2P-regular.ttf', MENU_HISCORE_SIZE)
    high_score_text = font_start.render(
        f"High Score: {high_score}", True, FONT_COLOR)
    high_score_rect = high_score_text.get_rect()
    high_score_rect.center = (
        SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + (SCREEN_HEIGHT / 4))
    return (logo_image, start_text_surface, start_text_rect, high_score_text, high_score_rect)


def reset_enemy_positions():
    global first_enemy_x, first_enemy_y, enemy_positions, num_of_enemies
    first_enemy_x = 30
    first_enemy_y = 30
    enemy_positions = []
    num_of_enemies = 0


def check_number_of_enemies(enemies):
    global ENEMY_ROWS, ENEMY_COLUMNS, MAX_ENEMY_ROWS, MAX_ENEMY_COLUMNS, ENEMY_SPACING, player_round, num_of_enemies, enemy_positions
    if (len(enemies) == 0):
        player_round += 1
        # Change number of enemies based on rounds
        if ENEMY_ROWS < (MAX_ENEMY_ROWS + 1):
            ENEMY_ROWS += 1
        if ENEMY_COLUMNS <= (MAX_ENEMY_COLUMNS + 1):
            ENEMY_COLUMNS += 1

        reset_enemy_positions()
        create_number_of_enemies(ENEMY_ROWS, ENEMY_COLUMNS, ENEMY_SPACING)
        create_enemies()


# Create sprite groups
all_sprites = Group()
player_group = Group()
projectile_group = Group()

# Create player's ship
player_ship = PlayerShip(player_pos)
all_sprites.add(player_ship)
player_group.add(player_ship)

bg_music = pygame.mixer.music.load('./Assets/Sounds/bg-music.wav')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

game_state = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("white")
    screen.blit(background_image, (0, 0))
    keys = pygame.key.get_pressed()

    if not game_state:
        text_surface = font.render(f"Game Over!", True, FONT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        screen.blit(text_surface, text_rect)

        text_surface = font.render(f"Press SPACE to replay!", True, FONT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 8)
        screen.blit(text_surface, text_rect)

        render_score_card(screen)
        
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        # dt = clock.tick(30) / 1000  # limits FPS to 60
        if keys[pygame.K_SPACE]:
            game_state = True
            reset_game()  # Transition to game loop
        continue
        

    if is_starting_page:
        (
            logo_image,
            start_text_surface,
            start_text_rect,
            high_score_text,
            high_score_rect
        ) = render_start_page()
        screen.blit(logo_image, ((SCREEN_WIDTH - 300) / 2, 0))
        screen.blit(start_text_surface, start_text_rect)
        screen.blit(high_score_text, high_score_rect)
        keys = pygame.key.get_pressed()
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # limits FPS to 60
        if keys[pygame.K_SPACE]:
            is_starting_page = False  # Transition to game loop
        else:
            continue
    
    pygame.mixer.music.set_volume(0)
    render_score_card(screen)

    for index, projectile in enumerate(projectiles):
        projectile.move_up(dt)
        if projectile.pos.y <= 0:
            del projectiles[index]
        pygame.draw.circle(
            screen,
            PROJECTILE_COLOR,
            (int(projectile.pos.x), int(projectile.pos.y)),
            PROJECTILE_SIZE
        )

        # Check for collision with enemies
        collided_enemy = projectile.check_collision(enemies)
        if collided_enemy:
            enemy_down.play()
            projectiles.remove(projectile)
            enemies.remove(collided_enemy)

            player_score += 20

        if len(enemies) <= math.floor(num_of_enemies / 2):
            for enemy in enemies:
                enemy.speed_x += ENEMY_SPEED_X
                enemy.speed_y += ENEMY_SPEED_Y
            num_of_enemies = math.floor(num_of_enemies / 2)

    check_number_of_enemies(enemies)

    # RENDER YOUR GAME HERE
    pygame.draw.circle(screen, PLAYER_COLOR, player_pos, PLAYER_SIZE)

    # Render Enemies
    enemy_last_shot_time = Enemy.shoot_projectiles(
        enemies,
        enemy_projectiles,
        enemy_last_shot_time,
        ENEMY_PROJECTILE_COOLDOWN,
        screen,
        dt
    )

    if check_enemy_projectile_collision(enemy_projectiles, player_pos):
        # Update High Schore
        update_high_score()
        # Game Over Screen
        game_over.play()
        game_state = False
        

    if check_enemy_passed_player(player_pos, enemies):
        # Update High Schore
        update_high_score()
        # Reset game State variables
        game_over.play()
        game_state = False

    move_enemies_sideways()

    change_enemy_movement_state()

    move_enemies_downwards()

    
    if keys[pygame.K_w] or keys[pygame.K_UP] :
        # Shoot projectiles
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - last_shot_time >= PROJECTILE_COOLDOWN:  # 500 milliseconds cooldown
            new_projectile = Projectile(player_pos.x, player_pos.y)
            projectiles.append(new_projectile)
            shoot.play()
            last_shot_time = current_time
    if keys[pygame.K_s]:
        # Maybe add a power up system to have once in a while AoE attack
        pass
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        # Check if we have hit a wall
        left_pos = player_pos.x - 200 * dt
        if not left_pos < PLAYER_SIZE:
            player_pos.x = left_pos
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        # Check if we have hit a wall
        right_pos = player_pos.x + 200 * dt
        if not right_pos + PLAYER_SIZE >= SCREEN_WIDTH:
            player_pos.x = right_pos

    # print("X: ", player_pos.x, " Player Size: ", player_size)
    player_ship.update()
    player_ship.draw(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(30) / 1000  # limits FPS to 60

pygame.quit()
