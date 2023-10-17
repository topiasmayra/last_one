import pygame
import sys
import time
import random
import winsound
import threading
from concurrent.futures import ThreadPoolExecutor
import datetime
import math
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
keep_running = True
executor = ThreadPoolExecutor(max_workers=100)
CHANGE_COLOR_BACK_EVENT = pygame.USEREVENT + 1
islands_monkeys_dict = {}
running = True
SEA_RECT = pygame.Rect(0, 500, 700, 200)  # Adjust the dimensions and position as needed
delete_button_hit = False
monkey_lock = threading.Lock() 
combined_monkey_thread_instance = None
sound_thread = None
current_point=None
# Set up buttons
buttons = [pygame.Rect(35 * i, 0, 35, 50) for i in range(20)] # Adjusted positions
point_values = list(range(1, 21))
button_island = pygame.Rect(0, 650, 100, 50)  # New island button
button_island_color = NICE  # Set the default color of the button to NICE
button_delete_islands=pygame.Rect(100,650,100,50)
button_delete_islands_color=RED
def draw_buttons(current_point=None):  # Added current_point argument here
    pygame.draw.rect(window_surface, button_island_color, button_island)  
    label = font.render('new_island', True, (0, 0, 0))
    text_rect = label.get_rect(center=button_island.center)
    window_surface.blit(label, text_rect)

    pygame.draw.rect(window_surface, button_delete_islands_color, button_delete_islands)
    label = font.render('delete_islands', True, (0, 0, 0))
    text_rect = label.get_rect(center=button_delete_islands.center)
    window_surface.blit(label, text_rect)

    for i, button in enumerate(buttons):
        color = GRAY
        if i + 1 <= points:
            color = GREEN
        if current_point is not None and i + 1 == current_point:
            color = GREEN
        pygame.draw.rect(window_surface, color, button)
        label = font.render(f'{point_values[i]}', True, (0, 0, 0))
        window_surface.blit(label, (button.x + 10, button.y + 15))

def i_suppose_i_have_earned_so_much_points(amount_of_points):
    global points
    window_surface.fill((0, 0, 255))
    points = amount_of_points
    for i in range(amount_of_points):
            draw_buttons(i + 1)  # Draw the buttons with the current point lit up
            pygame.display.update()
            winsound.Beep(440+i*100,500)
            time.sleep(1)  # Wait for 1 second after lighting up each button




# Make a Grid
grid_size = 90  # Assume each cell is 150x150 pixels
grid_width = window_surface.get_width() // grid_size
grid_height = window_surface.get_height() // grid_size
grid = [[[] for _ in range(grid_height)] for _ in range(grid_width)]

def add_to_grid(obj):
    grid_x = obj.x // grid_size
    grid_y = obj.y // grid_size
    grid[grid_x][grid_y].append(obj)
def draw_piers(surface, island_position):
    pier_length = 50  # Adjust this value as needed to ensure piers reach the sea
    pier_color = (139, 69, 19)  # Brown color for piers

    # The center coordinates of the island on the window_surface
    island_center = (island_position[0] + 45, island_position[1] + 45)

    # Coordinates for the start of the piers, relative to the island's position on the window_surface
    east_pier_start = (island_center[0] + 45, island_center[1])
    west_pier_start = (island_center[0] - 45, island_center[1])
    south_pier_start = (island_center[0], island_center[1] + 45)
    north_pier_start = (island_center[0], island_center[1] - 45)

    # Coordinates for the end of the piers, extending into the sea
    east_pier_end = (east_pier_start[0] + pier_length, east_pier_start[1])
    west_pier_end = (west_pier_start[0] - pier_length, west_pier_start[1])
    south_pier_end = (south_pier_start[0], south_pier_start[1] + pier_length)
    north_pier_end = (north_pier_start[0], north_pier_start[1] - pier_length)

    # Draw piers in all four directions from the island edges
    pygame.draw.line(surface, pier_color, east_pier_start, east_pier_end, 5)  # East
    pygame.draw.line(surface, pier_color, west_pier_start, west_pier_end, 5)  # West
    pygame.draw.line(surface, pier_color, south_pier_start, south_pier_end, 5)  # South
    pygame.draw.line(surface, pier_color, north_pier_start, north_pier_end, 5)  # North




def draw_island_random_location():
    global island_positions
    if draw_islands:
        island_width = 90
        island_height = 90
        for island in island_positions:
            island_position = island['position']
            island_name = island['name']
            
            # Create a new surface for the island
            island_surface = pygame.Surface((island_width, island_height), pygame.SRCALPHA)

            
            # Choose whether to draw a circle or square based on some condition,
            # or comment out one of the following two lines if you only want one shape
            pygame.draw.circle(island_surface, Yellow, (island_width // 2, island_height // 2), island_width // 2)
            pygame.draw.rect(island_surface, Yellow, (0, 0, island_width, island_height))
            
            # Check if the island is tourism_aware and draw piers if it is
            if island.get('tourism_aware', False):  # Using get() in case 'tourism_aware' key doesn't exist
               draw_piers(window_surface, island_position)
            
            # Count only monkeys that are on the island (exclude those in the sea)
            monkey_count = sum(1 for monkey in all_monkeys if monkey['island_name'] == island_name and not monkey['in_sea'])

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
            
            # Blit the island surface onto the window surface at the island's position
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
    global island_positions, island_rects, draw_islands, num_islands, island_name, island_count, executor, sound_thread, keep_running, keep_running, combined_monkey_thread_instance  # Include executor, sound_thread, keep_playing_sounds in the global statement, delete_button_hit
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
            tourism_aware = True if island_name == 'S1' else False  # Island S1 is tourism aware
    
            # Check if the new island collides with other islands or the new_island button
            if not button_collided and not check_collision(new_island_rect):
                island_rects.append(new_island_rect)  # Add the new island rect to the island_rects list
                occupied_positions.append((x, y, island_width, island_height))  # Record the occupied position
                add_to_grid(new_island_rect)
                add_monkeys_to_island(island_name, (x, y))
                draw_islands = True  # Set draw_islands to True 
                island_info = {'position': (x, y), 'name': island_name, 'tourism_aware': tourism_aware}
                island_positions.append(island_info)  # Append new island info as a dictionary

                if delete_button_hit and len(island_positions) == 10:
                    i_suppose_i_have_earned_so_much_points(5)

                if sound_thread and not sound_thread.is_alive() and not keep_running:
                        keep_running = True  # Allow the sound routine to run again
                        executor = ThreadPoolExecutor()  # Create a new ThreadPoolExecutor
                        sound_thread = threading.Thread(target=monkey_sound_routine)  # Create a new sound thread
                        sound_thread.start()  # Start the sound routine
               
                if not combined_monkey_thread_instance or not combined_monkey_thread_instance.is_alive():
                        keep_running = True  # Set the keep_running flag to True
                        combined_monkey_thread_instance = threading.Thread(target=combined_monkey_thread)
                        combined_monkey_thread_instance.start()  # Start the thread
                break  # Exit the while loop once a new island has been successfully created
def add_monkeys_to_island(island_name, island_position):
    global all_monkeys, islands_monkeys_dict
    monkeys = []  # List to hold the monkeys for this island
    frequencies = random.sample(range(200, 1001), 10)
    if island_name == 'S1':
        num_monkeys_that_can_swim = random.randint(1, 10)  # Random number of monkeys that can swim
    else:
        num_monkeys_that_can_swim = 0  # Monkeys from other islands cannot swim

    for i in range(10):  # Adding 10 monkeys to the island
        monkey_id = len(all_monkeys) + 1  # Generate a unique ID for each monkey
        monkey_frequency = frequencies[i]
        monkey_position = (island_position[0] + random.randint(-20, 20), island_position[1] + random.randint(-20, 20))
        
        # Determine if the current monkey can swim based on our random number
        can_swim = True if i < num_monkeys_that_can_swim else False
        
        monkey = {
            'id': monkey_id,
            'frequency': monkey_frequency,
            'position': monkey_position,
            'island_name': island_name,
            'can_swim': can_swim,
            'in_sea': False,
            'scoop_direction': None,  
             'angle': 0
        }

        monkeys.append(monkey)
        all_monkeys.append(monkey)

    with monkey_lock:
        islands_monkeys_dict[island_name] = monkeys  # Update the dictionary with the monkeys list for this island

def start_sound_thread():
    global sound_thread  # Declare it as global to modify the global variable
    sound_thread = threading.Thread(target=monkey_sound_routine)
    sound_thread.start()

def play_monkey_sound(frequency=None):
    if frequency is None:
        frequency = random.randint(200, 1000)
    duration = 50
    winsound.Beep(frequency, duration)



def monkey_sound_routine():
    while keep_running:
        try:
            with monkey_lock:
                for monkey in all_monkeys:
                    executor.submit(play_monkey_sound, monkey['frequency'])
            time.sleep(10)
        except Exception as e:
            print(f"Error in monkey_sound_routine: {e}")

# Define the islands you want the monkey_action_thread to act upon
island_names = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]  # Add more island names as needed


def combined_monkey_thread():
    print("Starting combined_monkey_thread")
    point_flag = False
    last_island_check = datetime.datetime.now()  # To track when we last checked island events
    last_scoop_check = datetime.datetime.now()  # To track when we last checked scoop events
    print (f'last_island_check: {last_island_check}')    
    while running and keep_running:
        with monkey_lock:
            current_time = datetime.datetime.now()
            print(f'current_time: {current_time}')
            # Check each monkey for island events if it's been more than 10 seconds
            if (current_time - last_island_check).seconds >= 10:
                for monkey in all_monkeys:
                    if not monkey['in_sea'] and random.random() < 0.01:  # 1% chance
                        if monkey in all_monkeys:
                            all_monkeys.remove(monkey)
                            print(f"{current_time} - Monkey {monkey['id']} on island {monkey['island_name']} died laughing")
                            winsound.Beep(666, 950)
                last_island_check = current_time

            # Check each monkey for sea events
            for monkey in all_monkeys:
                print(f"Monkey {monkey['id']} position: {monkey['position']}, in_sea: {monkey['in_sea']}")  # Debugging output
                if monkey['in_sea'] and random.random() < 0.01:  # 1% chance every second
                    all_monkeys.remove(monkey)
                    print(f"{current_time} - Monkey {monkey['id']} in the sea got eaten")
                    winsound.Beep(600, 700)

                # Monkey moving to sea logic
                if monkey['can_swim'] and not monkey['in_sea']:
                    monkey['position'] = (monkey['position'][0], monkey['position'][1] + 5)
                    if SEA_RECT.collidepoint(monkey['position']):
                        monkey['in_sea'] = True
                        print(f"{current_time} - Monkey {monkey['id']} on island {monkey['island_name']} moved to sea")

            # Check for monkey scoop events if it's been more than 10 seconds
            if (current_time - last_scoop_check).seconds >= 10:
                for island in island_positions:
                    if island['tourism_aware']:
                        monkeys_on_island = [monkey for monkey in all_monkeys if monkey['island_name'] == island['name'] and not monkey['in_sea']]
                        if monkeys_on_island:
                            monkey_to_scoop = random.choice(monkeys_on_island)
                            monkey_to_scoop['scoop_direction'] = random.choice(['north', 'east', 'south', 'west'])
                            print(f"{current_time} - Monkey {monkey_to_scoop['id']} on island {island['name']} scooping {monkey_to_scoop['scoop_direction']}")
                            winsound.Beep(500, 500)  # Placeholder for your sound effect
                            # Assume you have a function render_scoop to visualize the scooping
                            render_scoop(monkey_to_scoop)
                last_scoop_check = current_time
def render_scoop(monkey):
    global window_surface

    # Get the monkey's position and scooping direction
    x, y = monkey['position']
    scoop_direction = monkey['scoop_direction']
    angle = monkey['angle']  # Get the current angle

    # Determine the center of the circular scooping path based on the direction
    if scoop_direction == 'north':
        center_x, center_y = x, y - 20  # Adjust values as needed
    elif scoop_direction == 'east':
        center_x, center_y = x + 20, y  # Adjust values as needed
    elif scoop_direction == 'south':
        center_x, center_y = x, y + 20  # Adjust values as needed
    elif scoop_direction == 'west':
        center_x, center_y = x - 20, y  # Adjust values as needed

    # Calculate the new position along the circular path
    scoop_radius = 20  # Radius of the scooping circle
    scoop_x = center_x + scoop_radius * math.cos(math.radians(angle))
    scoop_y = center_y + scoop_radius * math.sin(math.radians(angle))

    # Increment the angle for the next frame
    monkey['angle'] = (angle + 10) % 360  # Adjust the value 10 to control the speed of scooping

    # Draw the monkey as a dot at the new position
    pygame.draw.circle(window_surface, RED, (int(scoop_x), int(scoop_y)), 5)

start_sound_thread()

def delete_all_islands():
    global island_positions, island_rects, grid, island_name, occupied_positions , delete_button_hit
    global island_count, keep_running, executor, sound_thread, combined_monkey_thread_instance  # <-- add the reference here
    
    # Shutdown Executor Once
    executor.shutdown(wait=True)
    
    # Clear the lists and reset variables
    island_positions.clear()
    island_rects.clear()
    occupied_positions = []
    island_count = 1
    delete_button_hit = True

    # Grid Clearing Optimization
    grid = [[[] for _ in range(grid_height)] for _ in range(grid_width)]
    
    # Stop the sound routine and clear all_monkeys list
    keep_running = False
    with monkey_lock:  # Locking
        all_monkeys.clear()
        
    # Stop combined_monkey_thread
    if combined_monkey_thread_instance and combined_monkey_thread_instance.is_alive():  # <-- add this check
        combined_monkey_thread_instance.join()
        
    # Thread Management
    if sound_thread.is_alive():
        sound_thread.join()
    
    # Reinitialize the executor and sound_thread for the next run
    executor = ThreadPoolExecutor(max_workers=100)  # ThreadPoolExecutor Configuration
    sound_thread = threading.Thread(target=monkey_sound_routine)
    sound_thread.start()




def handle_mouse_up(event):
    global last_click_time, button_island_color, button_delete_islands_color  # Ensure all necessary variables are global
    x, y = event.pos
    if button_island.collidepoint(x, y):
        create_new_island()
        print(f"Island {island_name} created")
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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


# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor()



while running:
    events = pygame.event.get()
    handle_events(events)
    current_time = pygame.time.get_ticks()
    if button_island_color == Yellow and current_time - last_click_time >= 50:
        button_island_color = NICE
    window_surface.fill(BLUE)
    draw_buttons()
    draw_island_random_location()
    for monkey in all_monkeys:
        if monkey['scoop_direction']:
            render_scoop(monkey)

    pygame.display.update()



pygame.quit()
sys.exit()