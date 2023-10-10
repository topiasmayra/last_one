import pygame
import sys
import time
import random
import winsound
# Initialize pygame
pygame.init()

# Set up the display
window_surface = pygame.display.set_mode((700, 700))
pygame.display.set_caption('Exercise 5')

# Set up fonts
font = pygame.font.Font(None, 16)  # Reduced font size to 16

# Set up colors
BLUE = (0, 0, 255)
GRAY = (192, 192, 192)
GREEN = (0, 255, 0)
NICE = (0, 255, 127)
Yellow = (255, 252, 72)
points = 0

# Set up buttons
buttons = [pygame.Rect(35 * i, 0, 35, 50) for i in range(20)] # Adjusted positions
point_values = list(range(1, 21))
button_island = pygame.Rect(0, 650, 100, 50)  # New island button
button_island_color = NICE  # Set the default color of the button to NICE

def draw_buttons():
    pygame.draw.rect(window_surface, button_island_color, button_island)  # Draw the new_island button using the button_island_color variable
    label = font.render('new_island', True, (0, 0, 0))
    text_rect = label.get_rect(center=button_island.center)  # Center the label text
    window_surface.blit(label, text_rect)  # Draw the label text

    for i, button in enumerate(buttons):
        pygame.draw.rect(window_surface, GRAY if i + 1 > points else GREEN, button)
        label = font.render(f'{point_values[i]}', True, (0, 0, 0))
        window_surface.blit(label, (button.x + 10, button.y + 15))

def i_suppose_i_have_earned_so_much_points(amount_of_points):
    global points
    points = amount_of_points
    window_surface.fill((0, 0, 255))  # Fill the background
    draw_buttons()  # Draw the buttons
    pygame.display.update()
    time.sleep(1)  # Wait for 1 second
    for i in range(amount_of_points):
       winsound.Beep(440+i*100,500)

last_click_time = 0  # Variable to keep track of when the button was last clicked


# Variables to store the island's positions
island_positions = []
draw_islands = False

# Make a Grid
grid_size = 150  # Assume each cell is 150x150 pixels
grid_width = window_surface.get_width() // grid_size
grid_height = window_surface.get_height() // grid_size
grid = [[[] for _ in range(grid_height)] for _ in range(grid_width)]

def add_to_grid(obj):
    grid_x = obj.x // grid_size
    grid_y = obj.y // grid_size
    grid[grid_x][grid_y].append(obj)

def check_collision(obj):
    grid_x = obj.x // grid_size
    grid_y = obj.y // grid_size
    for existing_obj in grid[grid_x][grid_y]:
        if existing_obj.colliderect(obj):
            return True
    return False

def draw_island_random_location():
    if draw_islands:
        island_width = 150
        island_height = 150
        for island_position in island_positions:
            island_surface = pygame.Surface((island_width, island_height), pygame.SRCALPHA)
            pygame.draw.circle(island_surface, Yellow, (island_width // 2, island_height // 2), island_width // 2)
            window_surface.blit(island_surface, island_position)

def new_islands():
    global draw_islands, island_positions
    draw_islands = True
    if len(island_positions) < 10:
        attempts = 0  # Counter to keep track of the number of attempts
        max_attempts = 100  # Set a maximum number of attempts to prevent an infinite loop
        while attempts < max_attempts:
            # Generate a new random coordinate for the island
            new_island_rect = pygame.Rect(
                random.randint(150, window_surface.get_width() - 150),
                random.randint(150, window_surface.get_height() - 150),
                150, 150
            )
            # Check for collisions with existing islands and buttons using the grid
            if not check_collision(new_island_rect):
                island_positions.append(new_island_rect.topleft)  # Add the new island to the list
                add_to_grid(new_island_rect)  # Add the new island to the grid
                break  # Break out of the loop since a suitable position was found
            attempts += 1  # Increment the attempts counter
        if attempts == max_attempts:
            print("Could not find a suitable position for a new island after 100 attempts.")
    draw_island_random_location()
def handle_events():
    global button_island_color, last_click_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  # Indicate that the game should end
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if button_island.collidepoint(x, y):  # Check if mouse click was inside button_island rect
                button_island_color = Yellow  # Change the color of the button to yellow
                print(f"island position {island_positions}")
                new_islands()  # Call new_islands to spawn islands
                last_click_time = pygame.time.get_ticks()  # Store the time of the click
    return True  # Indicate that the game should continue





running = True
while running:
    running = handle_events()  # Call handle_events and update running based on its return value
    current_time = pygame.time.get_ticks()  # Get the current time
    if button_island_color == Yellow and current_time - last_click_time >= 50:  # Check if 1 second has passed
        button_island_color = NICE  # Change the color of the button back to NICE
    window_surface.fill(BLUE)  # Fill the background
    draw_buttons()  # Draw the buttons
    draw_island_random_location()  # Draw the island if necessary, ensuring it's on top
    pygame.display.update()

# Clean up
pygame.quit()
sys.exit()


