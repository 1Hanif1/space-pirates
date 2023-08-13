# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

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
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    pygame.draw.circle(screen, "black", player_pos, 20)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    '''
    If all the code within the while loop finishes executing in less time than the desired time step (in this case, less than 16.67 milliseconds for a 60 FPS target frame rate), 
    the clock will introduce a pause to ensure that the total time elapsed since the last frame is at least the desired time step.
    '''

    dt = clock.tick(60) / 1000  # limits FPS to 60

pygame.quit()
