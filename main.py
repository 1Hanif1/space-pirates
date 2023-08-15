# Example file showing a basic pygame "game loop"
import pygame
import random
from pygame.sprite import Group
from modules.classes.projectile import Projectile
from modules.classes.enemy import Enemy
from modules.classes.variables import *
from modules.helper.playership import PlayerShip
from modules.helper.enemyship import EnemyShip

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Variables
running = True
dt = 0
player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
first_enemy_x = 30
first_enemy_y = 30
enemy_positions = []  # Starting positions of enemies
enemies = []
enemies_move_forward = True
enemies_move_downward = False
num_of_enemies = 0
projectiles = []  # All projectiles shot by player
enemy_projectiles = []
last_shot_time = 0  # Initialize this at the beginning of your code
enemy_last_shot_time = 0
font = pygame.font.Font(
    './Assets/Font/PressStart2P-regular.ttf',
    GAME_FONT_SIZE
)
player_score = 0
high_score = 0
is_starting_page = True


for row in range(ENEMY_ROWS):
    for column in range(ENEMY_COLUMNS):
        enemy_positions.append((first_enemy_x, first_enemy_y))
        first_enemy_x += ENEMY_SPACING
    first_enemy_y += (ENEMY_SPACING - 20)
    first_enemy_x = 30


try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.readline())
except FileNotFoundError:
    high_score = 0
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))

# Replace with your image file path
background_image = pygame.image.load("./Assets/Images/bg.jpg")
background_image = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
)


def render_score(screen):
    global font

    # Current Score
    text_surface = font.render(f"Score: {player_score}", True, FONT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.center = (SCREEN_WIDTH / 3, 10)
    screen.blit(text_surface, text_rect)

    # High Score
    text_surface = font.render(f"High Score: {high_score}", True, FONT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.center = (SCREEN_WIDTH / 2 + SCREEN_WIDTH / 8, 10)
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


def reset_game():
    global enemies, projectiles, enemy_projectiles, player_score
    enemies.clear()
    projectiles.clear()
    enemy_projectiles.clear()
    player_score = 0
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


# Create sprite groups
all_sprites = Group()
player_group = Group()
projectile_group = Group()

# Create player's ship
player_ship = PlayerShip(player_pos)
all_sprites.add(player_ship)
player_group.add(player_ship)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("white")
    screen.blit(background_image, (0, 0))

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

    render_score(screen)

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
            projectiles.remove(projectile)
            enemies.remove(collided_enemy)
            player_score += 20

        if len(enemies) < num_of_enemies / 2:
            for enemy in enemies:
                enemy.speed_x += ENEMY_SPEED_X
            num_of_enemies /= 2

    if (len(enemies) == 0):
        create_enemies()

    # RENDER YOUR GAME HERE
    pygame.draw.circle(screen, PLAYER_COLOR, player_pos, PLAYER_SIZE)

    # Render Enemies
    '''
    The enemies would randomly shoot particles towards the player side.
    '''
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
        # Reset game State variables
        reset_game()
        pass

    move_enemies_sideways()

    change_enemy_movement_state()

    move_enemies_downwards()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        # Shoot projectiles
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - last_shot_time >= PROJECTILE_COOLDOWN:  # 500 milliseconds cooldown
            new_projectile = Projectile(player_pos.x, player_pos.y)
            projectiles.append(new_projectile)
            last_shot_time = current_time
    if keys[pygame.K_s]:
        # Maybe add a power up system to have once in a while AoE attack
        pass
    if keys[pygame.K_a]:
        # Check if we have hit a wall
        left_pos = player_pos.x - 200 * dt
        if not left_pos < PLAYER_SIZE:
            player_pos.x = left_pos
    if keys[pygame.K_d]:
        # Check if we have hit a wall
        right_pos = player_pos.x + 200 * dt
        if not right_pos + PLAYER_SIZE >= SCREEN_WIDTH:
            player_pos.x = right_pos

    # print("X: ", player_pos.x, " Player Size: ", player_size)
    player_ship.update()
    player_ship.draw(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS to 60

pygame.quit()
