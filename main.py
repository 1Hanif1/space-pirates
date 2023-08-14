# Example file showing a basic pygame "game loop"
import pygame
from Projectile import Projectile

# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 500))
screen_height = screen.get_height()
screen_width = screen.get_width()
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
player_pos = pygame.Vector2(screen_width / 2, screen_height - 50)
player_size = 20

projectiles = []
last_shot_time = 0  # Initialize this at the beginning of your code

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
        pygame.draw.circle(screen, "red", (int(projectile.pos.x), int(projectile.pos.y)), 5)


    # RENDER YOUR GAME HERE
    pygame.draw.circle(screen, "black", player_pos, player_size)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        # Shoot projectiles
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - last_shot_time >= 500:  # 500 milliseconds cooldown
            new_projectile = Projectile(player_pos.x, player_pos.y, screen)
            projectiles.append(new_projectile)
            last_shot_time = current_time
    if keys[pygame.K_s]:
        # Maybe add a power up system to have once in a while AoE attack
        pass
    if keys[pygame.K_a]:
        # Check if we have hit a wall
        left_pos = player_pos.x - 200 * dt
        if not left_pos < player_size:
            player_pos.x = left_pos
    if keys[pygame.K_d]:
        # Check if we have hit a wall
        right_pos = player_pos.x + 200 * dt
        if not right_pos + player_size >= screen_width:
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
