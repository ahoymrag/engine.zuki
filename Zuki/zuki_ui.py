import pygame
import sys
import math

pygame.init()

# --- Color Palette (provided hex values) ---
# #6bc8cd, #cdd8c7, #fbb38d, #f58b7e, #d05774
def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

colors_hex = ["#6bc8cd", "#cdd8c7", "#fbb38d", "#f58b7e", "#d05774"]
colors_rgb = [hex_to_rgb(h) for h in colors_hex]

# We'll use these colors as follows:
face_border_color = colors_rgb[0]  # #6bc8cd
# Face fill color will vary with expression:
face_fill_colors = {
    "neutral": colors_rgb[1],  # #cdd8c7
    "happy": colors_rgb[2],    # #fbb38d
    "sad": colors_rgb[4]       # #d05774
}
# Use colors_rgb[3] (#f58b7e) as an accent (for input field border)

# --- Screen Setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zuki's Visual Console")

# --- Fonts ---
terminal_font = pygame.font.Font(None, 24)
input_font = pygame.font.Font(None, 28)

# --- Global State ---
current_expression = "neutral"
terminal_lines = ["🤖 Welcome to Zuki's Console! Type 'help' for commands."]
current_input = ""
cursor_visible = True
cursor_timer = 0
CURSOR_BLINK_INTERVAL = 500  # milliseconds

clock = pygame.time.Clock()

# --- Helper Functions ---

def draw_gradient_background(surface, color_stops):
    """Draws a vertical gradient over the entire surface using multiple color stops."""
    h = surface.get_height()
    num_stops = len(color_stops)
    # Each stop is placed evenly from y=0 to y=h-1
    for y in range(h):
        pos = y / (h - 1)
        # Determine which two stops y falls between
        segment = pos * (num_stops - 1)
        index = int(segment)
        t = segment - index
        if index >= num_stops - 1:
            color = color_stops[-1]
        else:
            c1 = color_stops[index]
            c2 = color_stops[index + 1]
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            color = (r, g, b)
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))

def quadratic_bezier(P0, P1, P2, num_points=30):
    """Returns a list of points along a quadratic Bézier curve."""
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (1 - t)**2 * P0[0] + 2 * (1 - t) * t * P1[0] + t**2 * P2[0]
        y = (1 - t)**2 * P0[1] + 2 * (1 - t) * t * P1[1] + t**2 * P2[1]
        points.append((int(x), int(y)))
    return points

def draw_face(surface, expression, center, radius):
    """Draws Zuki's face with eyes and a mouth that changes based on expression."""
    fill_color = face_fill_colors.get(expression, face_fill_colors["neutral"])
    # Draw face circle
    pygame.draw.circle(surface, fill_color, center, radius)
    pygame.draw.circle(surface, face_border_color, center, radius, 4)
    
    # Draw eyes
    eye_radius = 8
    eye_offset_x = 35
    eye_offset_y = 30
    left_eye = (center[0] - eye_offset_x, center[1] - eye_offset_y)
    right_eye = (center[0] + eye_offset_x, center[1] - eye_offset_y)
    pygame.draw.circle(surface, (0, 0, 0), left_eye, eye_radius)
    pygame.draw.circle(surface, (0, 0, 0), right_eye, eye_radius)
    
    # Draw mouth based on expression
    mouth_width = 60
    mouth_y_offset = 40
    if expression == "happy":
        P0 = (center[0] - mouth_width // 2, center[1] + mouth_y_offset)
        P2 = (center[0] + mouth_width // 2, center[1] + mouth_y_offset)
        control_offset = 20
        P1 = (center[0], center[1] + mouth_y_offset + control_offset)
        points = quadratic_bezier(P0, P1, P2)
        pygame.draw.lines(surface, (0, 0, 0), False, points, 3)
    elif expression == "sad":
        P0 = (center[0] - mouth_width // 2, center[1] + mouth_y_offset + 20)
        P2 = (center[0] + mouth_width // 2, center[1] + mouth_y_offset + 20)
        P1 = (center[0], center[1] + mouth_y_offset)
        points = quadratic_bezier(P0, P1, P2)
        pygame.draw.lines(surface, (0, 0, 0), False, points, 3)
    else:  # neutral
        start_pos = (center[0] - mouth_width // 2, center[1] + mouth_y_offset)
        end_pos = (center[0] + mouth_width // 2, center[1] + mouth_y_offset)
        pygame.draw.line(surface, (0, 0, 0), start_pos, end_pos, 3)

# --- Dummy Command Functions (Simulate main.py modules) ---
def dummy_motor_control_move(direction):
    return f"Moving {direction}."

def dummy_speech_speak(text):
    return f"Zuki says: {text}"

def dummy_sensors_read():
    return "Sensor data: [temperature: 22°C, humidity: 45%]"

def dummy_ai_process(query):
    return f"AI Response: I don't have an answer for '{query}'."

def dummy_web_server_start():
    return "Web server started at http://localhost:8000"

def process_command(command):
    """Parses the command and returns output text along with an exit flag."""
    global current_expression
    command = command.strip()
    if command == "":
        return "", False
    if command == "exit":
        current_expression = "neutral"
        return "Shutting down Zuki...", True
    elif command == "help":
        current_expression = "happy"
        return ("Available Commands:\n"
                "  move [direction] - Move Zuki (forward, backward, left, right)\n"
                "  speak [text] - Make Zuki talk\n"
                "  sense - Read sensor data\n"
                "  ai [question] - Ask Zuki something\n"
                "  web - Start web server\n"
                "  exit - Shutdown Zuki", False)
    elif command.startswith("move "):
        parts = command.split(" ", 1)
        if len(parts) > 1:
            direction = parts[1]
            current_expression = "neutral"
            return dummy_motor_control_move(direction), False
        else:
            current_expression = "sad"
            return "Please specify a direction.", False
    elif command.startswith("speak "):
        text = command[6:]
        current_expression = "happy"
        return dummy_speech_speak(text), False
    elif command == "sense":
        current_expression = "neutral"
        return dummy_sensors_read(), False
    elif command.startswith("ai "):
        query = command[3:]
        current_expression = "neutral"
        return dummy_ai_process(query), False
    elif command == "web":
        current_expression = "neutral"
        return dummy_web_server_start(), False
    else:
        current_expression = "sad"
        return "Unknown command. Type 'help' for available commands.", False

# --- Main Loop ---
running = True

while running:
    dt = clock.tick(30)
    cursor_timer += dt
    if cursor_timer >= CURSOR_BLINK_INTERVAL:
        cursor_timer = 0
        cursor_visible = not cursor_visible

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                current_input = current_input[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                # Echo command in terminal
                terminal_lines.append("> " + current_input)
                result, should_exit = process_command(current_input)
                if result:
                    for line in result.split("\n"):
                        terminal_lines.append(line)
                current_input = ""
                if should_exit:
                    running = False
                    break
            else:
                # Append character if printable
                if event.unicode:
                    current_input += event.unicode

    # --- Drawing ---
    # Draw a smooth vertical gradient background using our palette
    draw_gradient_background(screen, colors_rgb)
    
    # Draw Zuki's face near the top center
    face_center = (WIDTH // 2, 150)
    face_radius = 100
    draw_face(screen, current_expression, face_center, face_radius)
    
    # Terminal Log Area (a white box with a border)
    terminal_area = pygame.Rect(50, 300, 700, 200)
    pygame.draw.rect(screen, (255, 255, 255), terminal_area)
    pygame.draw.rect(screen, face_border_color, terminal_area, 2)
    
    # Display the last few terminal lines (limit to 8)
    max_lines = 8
    lines_to_show = terminal_lines[-max_lines:]
    y = terminal_area.y + 10
    for line in lines_to_show:
        text_surface = terminal_font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (terminal_area.x + 10, y))
        y += text_surface.get_height() + 2

    # Input Field at the bottom
    input_rect = pygame.Rect(50, 520, 700, 40)
    pygame.draw.rect(screen, (255, 255, 255), input_rect)
    pygame.draw.rect(screen, colors_rgb[3], input_rect, 2)
    input_surface = input_font.render(current_input, True, (0, 0, 0))
    screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 5))
    
    # Blinking cursor
    if cursor_visible:
        cursor_x = input_rect.x + 10 + input_surface.get_width() + 2
        cursor_y = input_rect.y + 5
        cursor_height = input_surface.get_height()
        pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
››