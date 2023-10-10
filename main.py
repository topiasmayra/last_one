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
RED=(255,0,0)

#Varibles / boolens
island_count = 1 
points = 0
last_click_time = 0  # Variable to keep track of when the button was last clicked
num_islands=0
# Variables to store the island's positions
island_positions = []
draw_islands = False


# Set up buttons
buttons = [pygame.Rect(35 * i, 0, 35, 50) for i in range(20)] # Adjusted positions
point_values = list(range(1, 21))
button_island = pygame.Rect(0, 650, 100, 50)  # New island button
button_island_color = NICE  # Set the default color of the button to NICE
button_delete_islands=pygame.Rect(100,650,100,50)
button_delete_islands_color=RED
def draw_buttons():
    pygame.draw.rect(window_surface, button_island_color, button_island)  # Draw the new_island button using the button_island_color variable
    label = font.render('new_island', True, (0, 0, 0))
    text_rect = label.get_rect(center=button_island.center)  # Center the label text
    window_surface.blit(label, text_rect)  # Draw the label text

    pygame.draw.rect(window_surface, button_delete_islands_color, button_delete_islands)
    label = font.render('delete_islands', True, (0, 0, 0))
    text_rect = label.get_rect(center=button_delete_islands.center)
    window_surface.blit(label, text_rect)  # Draw the label text for delete_islands button

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



# Make a Grid
grid_size = 60  # Assume each cell is 150x150 pixels
grid_width = window_surface.get_width() // grid_size
grid_height = window_surface.get_height() // grid_size
grid = [[[] for _ in range(grid_height)] for _ in range(grid_width)]

def add_to_grid(obj):
    grid_x = obj.x // grid_size
    grid_y = obj.y // grid_size
    grid[grid_x][grid_y].append(obj)


def draw_island_random_location():
    if draw_islands:
        island_width = 90
        island_height = 90
        for island_position in island_positions:
            island_surface = pygame.Surface((island_width, island_height), pygame.SRCALPHA)
            pygame.draw.circle(island_surface, Yellow, (island_width // 2, island_height // 2), island_width // 2)
            window_surface.blit(island_surface, island_position)
island_rects = []  # Define the island_rects list


draw_islands = False  # Define draw_islands somewhere in the code
def check_collision(obj_rect):
    for existing_rect in island_rects:
        if existing_rect.colliderect(obj_rect):
            return True  # A collision was detected with an existing island
    if button_island.colliderect(obj_rect):
        return True  # A collision was detected with the new_island button
    for occupied_position in occupied_positions:
        if pygame.Rect(*occupied_position).colliderect(obj_rect):
            return True  # A collision was detected with a previously occupied position
    return False  # No collisions were detected

def add_island_name(surface, name):
    # Create a font for the island name
    island_font = pygame.font.Font(None, 24)  # You can adjust the font size as needed

    # Render the island name text
    island_name_text = island_font.render(name, True, (0, 0, 0))

    # Calculate the position to center the island name on the island surface
    text_rect = island_name_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))

    # Blit the island name text onto the island surface
    surface.blit(island_name_text, text_rect.topleft)  # Use topleft to position the text correctly

def new_islands():
    global island_positions, island_rects, draw_islands, num_islands, island_name, island_count  # Include num_islands in the global statement
    island_name = "S" + str(island_count)  # Generate a unique name for the island
    island_count += 1  # Increment the island count
    if len(island_positions) < 10:  # Check if the number of islands is less than 10
        island_width = 90
        island_height = 90
        while True:
            x = random.randint(0, window_width - island_width)
            y = random.randint(0, window_height - island_height)
            new_island_rect = pygame.Rect(x, y, island_width, island_height)
            
            # Check if the new island collides with any buttons
            button_collided = False
            for button in buttons:
                if button.colliderect(new_island_rect):
                    button_collided = True
                    break
            
            # Check if the new island collides with the delete_islands button
            if button_delete_islands.colliderect(new_island_rect):
                button_collided = True
            
            if not button_collided and not check_collision(new_island_rect):
                island_positions.append((x, y))
                island_rects.append(new_island_rect)  # Add the new island rect to the island_rects list
                occupied_positions.append((x, y, island_width, island_height))  # Record the occupied position
                add_to_grid(new_island_rect)
                draw_islands = True  # Set draw_islands to True 
                break  # Exit the while loop once a new island has been successfully created
window_width, window_height = window_surface.get_size()

occupied_positions = []

def delete_all_islands():
    global island_positions, island_rects, grid, occupied_positions,island_count
    island_positions.clear()  # Clear the island_positions list
    island_rects.clear()  # Clear the island_rects list
    for x in range(grid_width):
        for y in range(grid_height):
            grid[x][y].clear()  # Clear each cell in the grid
    occupied_positions = []  # Reset the occupied_positions list
    island_count=1  # Generate a unique name for the island

def handle_events():
    global last_click_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  # Indicate that the game should end
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if button_island.collidepoint(x, y):
                new_islands()
                print(f"Island {island_name} created")
                button_island_color = Yellow
                last_click_time = pygame.time.get_ticks()
            elif button_delete_islands.collidepoint(x, y):
                delete_all_islands()
            # Remove the else block to prevent calling delete_all_islands function when no button is clicked
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