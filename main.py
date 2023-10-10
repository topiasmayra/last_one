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

def handle_events():
    global button_island_color, last_click_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  # Indicate that the game should end
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if button_island.collidepoint(x, y):  # Check if mouse click was inside button_island rect
                button_island_color = Yellow  # Change the color of the button to yellow
                print('New Island Button Clicked')
                i_suppose_i_have_earned_so_much_points(5)
                last_click_time = pygame.time.get_ticks()  # Store the time of the click
    return True  # Indicate that the game should continue







# Run the game loop
running = True
while running:
    running = handle_events()  # Call handle_events and update running based on its return value
    current_time = pygame.time.get_ticks()  # Get the current time
    if button_island_color == Yellow and current_time - last_click_time >= 50:  # Check if 1 second has passed
        button_island_color = NICE  # Change the color of the button back to NICE
    window_surface.fill(BLUE)  # Fill the background
    draw_buttons()  # Draw the buttons
    pygame.display.update()

# Clean up
pygame.quit()
sys.exit()
