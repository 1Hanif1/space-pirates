# Example file showing a basic pygame "game loop"
import pygame
from Projectile import Projectile
from Enemy import Enemy
from variables import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

"""
In the context of game development, a clock is often used to control the timing of various events within the game. 
Games typically need to update their graphics, physics, and logic at a consistent rate, and a clock helps ensure that these updates happen at a regular interval.

1. pygame is the name of the library that provides functionalities for developing games and multimedia applications in Python.

2. pygame.time is a module within the Pygame library that provides functions related to time and timing.

3. Clock() is a constructor function that creates a clock object. This clock object can be used to control the frame rate of your game or application.
"""
clock = pygame.time.Clock()

running = True

dt = 0
player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
first_enemy_x = 30
first_enemy_y = 30

enemy_positions = []  # Starting positions of enemies

for row in range(ENEMY_ROWS):
    for column in range(ENEMY_COLUMNS):
        enemy_positions.append((first_enemy_x, first_enemy_y))
        first_enemy_x += ENEMY_SPACING
    first_enemy_y += (ENEMY_SPACING - 20)
    first_enemy_x = 30


enemies = []
enemies_move_forward = True
enemies_move_downward = False
projectiles = []  # All projectiles shot by player
last_shot_time = 0  # Initialize this at the beginning of your code

for positions in enemy_positions:
    (pos_x, pos_y) = positions
    # enemy_pos = pygame.Vector2(pos_x, pos_y)
    new_enemy = Enemy(pos_x, pos_y)
    enemies.append(new_enemy)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for index, projectile in enumerate(projectiles):
        projectile.move(dt)
        if projectile.pos.y <= 0:
            del projectiles[index]
        pygame.draw.circle(
            screen,
            PROJECTILE_COLOR,
            (int(projectile.pos.x), int(projectile.pos.y)),
            PROJECTILE_SIZE
        )

    # RENDER YOUR GAME HERE
    pygame.draw.circle(screen, PLAYER_COLOR, player_pos, PLAYER_SIZE)

    # Render Enemies
    '''
    1. There will be one level with set number of enemies (5 enemies x 3 rows)
    2. Each enemy would have a position in grid. They would move along x axis, one side to other 
    and then move a row ahead along the y axis
    3. The enemies would randomly shoot particles towards the player side.
    4. Once half the enemies are eliminated, the speed of fire and movement for other enemies would increase
    '''

    for enemy in enemies:
        pygame.draw.circle(
            screen,
            ENEMY_COLOR,
            (int(enemy.pos.x), int(enemy.pos.y)),
            5
        )

        if enemies_move_forward:
            enemy.move_forward_x(dt)
        else:
            enemy.move_backward_x(dt)

    for enemy in enemies:
        if enemy.pos.x >= SCREEN_WIDTH:
            enemies_move_forward = False
            enemies_move_downward = True
            break
        elif enemy.pos.x <= 0:
            enemies_move_forward = True
            enemies_move_downward = True
            break

    if enemies_move_downward:
        for enemy in enemies:
            enemy.move_down_y(dt)
        enemies_move_downward = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        # Shoot projectiles
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - last_shot_time >= PROJECTILE_COOLDOWN:  # 500 milliseconds cooldown
            new_projectile = Projectile(player_pos.x, player_pos.y, screen)
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

    # flip() the display to put your work on screen
    pygame.display.flip()

    '''
    If all the code within the while loop finishes executing in less time than the desired time step (in this case, less than 16.67 milliseconds for a 60 FPS target frame rate), 
    the clock will introduce a pause to ensure that the total time elapsed since the last frame is at least the desired time step.
    '''

    dt = clock.tick(60) / 1000  # limits FPS to 60

pygame.quit()
