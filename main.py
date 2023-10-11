import pygame
import sys
import time
import random
import winsound
import threading
from concurrent.futures import ThreadPoolExecutor

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
island_rects = []  # Define the island_rects list
occupied_positions = []  # Define the occupied_positions list
draw_islands = False
all_monkeys = []
keep_playing_sounds = True
executor = ThreadPoolExecutor(max_workers=10)
CHANGE_COLOR_BACK_EVENT = pygame.USEREVENT + 1
run_once_flag = False


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
    global island_positions
    if draw_islands:
        island_width = 90
        island_height = 90
        for island in island_positions:
            island_position = island['position']
            island_name = island['name']
            island_surface = pygame.Surface((island_width, island_height), pygame.SRCALPHA)
            pygame.draw.circle(island_surface, Yellow, (island_width // 2, island_height // 2), island_width // 2)
            
            # Count the number of monkeys on this island
            monkey_count = sum(1 for monkey in all_monkeys if monkey['island_name'] == island_name)
            
            # Create a font for displaying the text
            text_font = pygame.font.Font(None, 20)
            
            # Combine the island name and monkey count into one string
            text_string = f'{island_name}: {monkey_count}'
            
            # Render the text
            text_surface = text_font.render(text_string, True, (0, 0, 0))
            
            # Calculate the position to center the text on the island surface
            text_rect = text_surface.get_rect(center=(island_surface.get_width() // 2, island_surface.get_height() // 2))
            
            # Blit the text onto the island surface
            island_surface.blit(text_surface, text_rect.topleft)
            
            window_surface.blit(island_surface, island_position)

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

def create_new_island():
    global island_positions, island_rects, draw_islands, num_islands, island_name, island_count, executor, sound_thread, keep_playing_sounds  # Include executor, sound_thread, keep_playing_sounds in the global statement
    
    # Get the window dimensions
    window_width, window_height = window_surface.get_size()
    
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
            button_collided = any(button.colliderect(new_island_rect) for button in buttons)
            button_collided = button_collided or button_delete_islands.colliderect(new_island_rect) or button_island.colliderect(new_island_rect)
            
            # Check if the new island collides with other islands or the new_island button
            if not button_collided and not check_collision(new_island_rect):
                island_info = {'position': (x, y), 'name': island_name, 'monkeys': []}
                island_positions.append(island_info)
                island_rects.append(new_island_rect)
                island_positions.append({'position': (x, y), 'name': island_name})  # Append new island info as a dictionary
                island_rects.append(new_island_rect)  # Add the new island rect to the island_rects list
                occupied_positions.append((x, y, island_width, island_height))  # Record the occupied position
                add_to_grid(new_island_rect)
                add_monkeys_to_island(island_name, (x, y))
                draw_islands = True  # Set draw_islands to True 
                if not sound_thread.is_alive() and not keep_playing_sounds:
                        keep_playing_sounds = True  # Allow the sound routine to run again
                        executor = ThreadPoolExecutor()  # Create a new ThreadPoolExecutor
                        sound_thread = threading.Thread(target=monkey_sound_routine)  # Create a new sound thread
                        sound_thread.start()  # Start the sound routine
                break  # Exit the while loop once a new island has been successfully created

monkey_lock = threading.Lock()  



def add_monkeys_to_island(island_name, island_position):
    # Find the island by its name
    island = next(island for island in island_positions if island['name'] == island_name)
    if island:
        for _ in range(10):  # Adding 10 monkeys to the island
            monkey_id = len(island['monkeys']) + 1  # Generate a unique ID for each monkey
            monkey_frequency = random.randint(200, 1000)  # Assign a unique random frequency to each monkey
            monkey_position = (island_position[0] + random.randint(-20, 20), 
                               island_position[1] + random.randint(-20, 20))
            monkey = {
                'id': monkey_id,
                'frequency': monkey_frequency,
                'position': monkey_position,
                'island_name': island_name
            }
            island['monkeys'].append(monkey)







def play_monkey_sound():
    frequency = random.randint(200, 1000)  # Generate a random frequency between 200 and 1000 Hz
    duration = 500  # Duration of the sound in milliseconds
    winsound.Beep(frequency, duration)


def monkey_sound_routine():
    while keep_playing_sounds:
        for monkey in all_monkeys:
            executor.submit(play_monkey_sound, monkey['frequency'])
        time.sleep(10)  # wait for ten seconds before playing the sounds again


def play_monkey_sound(frequency):
    duration = 500
    winsound.Beep(frequency, duration)

def monkey_sound_routine():
    global keep_playing_sounds
    while keep_playing_sounds:
        with monkey_lock:  # Acquire the lock when iterating through all_monkeys
            for monkey in all_monkeys:
                executor.submit(play_monkey_sound, monkey['frequency'])
        time.sleep(10)  # wait for ten seconds before playing the sounds again




# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor()

# Start the monkey sound routine in a separate thread
sound_thread = threading.Thread(target=monkey_sound_routine)
sound_thread.start()
def delete_all_islands():
    global island_positions, island_rects, grid, island_name, occupied_positions
    global island_count, keep_playing_sounds, executor, sound_thread
    
    # Shutdown Executor Once
    executor.shutdown(wait=True)
    
    # Clear the lists and reset variables
    island_positions.clear()
    island_rects.clear()
    occupied_positions = []
    island_count = 1
    
    # Grid Clearing Optimization
    grid = [[[] for _ in range(grid_height)] for _ in range(grid_width)]
    
    # Stop the sound routine and clear all_monkeys list
    keep_playing_sounds = False
    with monkey_lock:  # Locking
        all_monkeys.clear()
    
    # Thread Management
    if sound_thread.is_alive():
        sound_thread.join()
    
    # Reinitialize the executor and sound_thread for the next run
    executor = ThreadPoolExecutor(max_workers=10)  # ThreadPoolExecutor Configuration
    sound_thread = threading.Thread(target=monkey_sound_routine)
    sound_thread.start()

def restart_sound_thread():
    global keep_playing_sounds, executor, sound_thread
    keep_playing_sounds = True  # Allow the sound routine to run again
    executor = ThreadPoolExecutor()  # Create a new ThreadPoolExecutor
    sound_thread = threading.Thread(target=monkey_sound_routine)  # Create a new sound thread
    sound_thread.start()  # Start the sound routi



def check_and_run_command():
    global run_once_flag
    # Check if the command hasn't been run yet, and there are 10 islands,
    # and island_count has been reset indicating delete_all_islands was called
    if not run_once_flag and len(island_positions) == 10 and island_count == 1:  # island_count would be 1 if islands were deleted and 10 new islands have been created
        run_once_flag = True  # Set the flag to True so this function won't run again
        i_suppose_i_have_earned_so_much_points(5)  # Run the command

def start_check_and_run_command_thread():
    command_thread = threading.Thread(target=check_and_run_command)
    command_thread.start()
def monkey_die_laughing(island_name):
    time.sleep(10)  # Wait for 10 seconds
    island = next((island for island in island_positions if island['name'] == island_name), None)
    if island:
        with monkey_lock:
            monkey = next((monkey for monkey in island['monkeys'] if random.random() <= 0.51), None)
            if monkey:
                island['monkeys'].remove(monkey)
                play_monkey_sound(440)  # Play a sound at 440 Hz
                print(f"Monkey {monkey['id']} on island {island_name} died laughing")
                winsound.Beep(666, 950)

def monkey_dying_thread():
    while running:
        for island in island_positions:
            monkey_die_laughing(island['name'])
        time.sleep(1)
# ... later in your code ...
# Start the monkey_dying_thread
dying_thread = threading.Thread(target=monkey_dying_thread)
dying_thread.start()

def handle_mouse_up(event):
    global last_click_time, button_island_color, button_delete_islands_color  # Ensure all necessary variables are global
    x, y = event.pos
    if button_island.collidepoint(x, y):
        create_new_island()
        print(f"Island {island_name} created")
        button_island_color = Yellow
        last_click_time = pygame.time.get_ticks()
    elif button_delete_islands.collidepoint(x, y):
        button_delete_islands_color = GREEN
        delete_all_islands()
        pygame.time.set_timer(CHANGE_COLOR_BACK_EVENT, 50)  # Set a timer to change color back in 500 milliseconds

def handle_quit(event):
    pygame.quit()
    sys.exit()

def handle_events(events):
    for event in events:
        handler = event_handlers.get(event.type)
        if handler:
            handler(event)
def handle_change_color_back(event):
    global button_delete_islands_color
    button_delete_islands_color = RED

event_handlers = {
    pygame.MOUSEBUTTONUP: handle_mouse_up,
    pygame.QUIT: handle_quit,
    CHANGE_COLOR_BACK_EVENT: handle_change_color_back,
}
def handle_events(events):
    for event in events:
        handler = event_handlers.get(event.type)
        if handler:
            handler(event)

running = True
running = True
while running:
    events = pygame.event.get()
    handle_events(events)  # Call handle_events with the list of current events
    current_time = pygame.time.get_ticks()  # Get the current time
    if button_island_color == Yellow and current_time - last_click_time >= 50:  # Check if 1 second has passed
        button_island_color = NICE  # Change the color of the button back to NICE
    window_surface.fill(BLUE)  # Fill the background
    draw_buttons()  # Draw the buttons
    draw_island_random_location()  # Draw the island if necessary, ensuring it's on top
    start_check_and_run_command_thread()
    pygame.display.update()
    if not sound_thread.is_alive() and keep_playing_sounds:  # Check if the sound thread has stopped and should be restarted
        restart_sound_thread()  # Restart the sound routine if necessary
# Clean up
pygame.quit()
sys.exit()
