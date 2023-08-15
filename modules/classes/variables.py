# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Font Properties
FONT_COLOR = (255, 255, 255)
GAME_FONT_SIZE = 10
MENU_FONT_SIZE = 15
MENU_HISCORE_SIZE = 10

# Player properties
PLAYER_SIZE = 5
PLAYER_SPEED_X = 200
PLAYER_COLOR = "blue"

# Projectile properties
PROJECTILE_SPEED = 200
PROJECTILE_COOLDOWN = 1000  # milliseconds
PROJECTILE_SIZE = 3
PROJECTILE_COLOR = "green"

# Enemy properties
ENEMY_SIZE = 10
ENEMY_SPEED_X = 50
ENEMY_SPEED_Y = 400
ENEMY_COLUMNS = 1  # MAX: 8
ENEMY_ROWS = 1  # MAX: 5
MAX_ENEMY_COLUMNS = 8
MAX_ENEMY_ROWS = 5
ENEMY_SPACING = 60
ENEMY_COLOR = "black"
ENEMY_PROJECTILE_COLOR = "red"
ENEMY_PROJECTILE_COOLDOWN = 500

# Non Constants
running = True
dt = 0
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
player_score = 0
high_score = 0
player_round = 0
is_starting_page = True
