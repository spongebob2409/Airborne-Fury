from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random 
import sys 
import time

TARGET_FPS=30
FRAME_TIME= 1/TARGET_FPS
last_time = time.time()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Jet positions
jet1_x, jet1_y = 200, 300
jet2_x, jet2_y = 600, 300

# Movement speed
JET_SPEED = 5
PROJECTILE_SPEED = 25  # Speed for projectiles

# Key states
keys = {}

# Jet states (active or destroyed)
jet1_active = True
jet2_active = True
abc=0
cloudarr=[]

# Projectile class
class Projectile:
    def __init__(self, x, y, direction, color):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for right, -1 for left
        self.color = color
        self.active = True

    def move(self):
        self.x += PROJECTILE_SPEED * self.direction
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.active = False

    def draw(self):
        if self.active:
            glColor3f(self.color[0], self.color[1], self.color[2])
            glBegin(GL_POINTS)
            glVertex2f(self.x, self.y)
            glEnd()

    def check_collision(self, jet_x, jet_y):
        """Check if the projectile hits a jet."""
        if self.active and abs(self.x - jet_x) < 15 and abs(self.y - jet_y) < 15:
            self.active = False
            return True
        return False
# List to hold projectiles
projectiles = []

def draw_circle(x, y, radius):
    """Draw a filled circle using the midpoint circle algorithm."""
    glBegin(GL_POINTS)
    p = 1 - radius
    xc, yc = 0, int(radius)  # Cast yc to an integer
    
    while xc <= yc:
        # Draw horizontal lines across the circle for filling
        for i in range(-yc, yc + 1):
            glVertex2f(x + xc, y + i)
            glVertex2f(x - xc, y + i)
        
        for i in range(-xc, xc + 1):
            glVertex2f(x + yc, y + i)
            glVertex2f(x - yc, y + i)
        
        xc += 1
        if p < 0:
            p += 2 * xc + 1
        else:
            yc -= 1
            p += 2 * (xc - yc) + 1
    
    glEnd()
def draw_circle1(x, y, radius, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
    """
    Draw a filled circle using the midpoint circle algorithm.

    Args:
    x (int): x-coordinate of the circle's center.
    y (int): y-coordinate of the circle's center.
    radius (int): Radius of the circle.
    screen_width (int): Width of the screen.
    screen_height (int): Height of the screen.

    Returns:
    list: A list of points to be drawn for the filled circle.
    """
    radius = int(radius)  # Ensure radius is an integer
    p = 1 - radius
    xc, yc = 0, radius
    points = []

    while xc <= yc:
        # Draw horizontal lines across the circle for filling
        for i in range(-yc, yc + 1):
            if 0 <= x + xc < screen_width and 0 <= y + i < screen_height:
                points.append((x + xc, y + i))
            if 0 <= x - xc < screen_width and 0 <= y + i < screen_height:
                points.append((x - xc, y + i))

        for i in range(-xc, xc + 1):
            if 0 <= x + yc < screen_width and 0 <= y + i < screen_height:
                points.append((x + yc, y + i))
            if 0 <= x - yc < screen_width and 0 <= y + i < screen_height:
                points.append((x - yc, y + i))

        # Update decision parameter and points
        xc += 1
        if p < 0:
            p += 2 * xc + 1
        else:
            yc -= 1
            p += 2 * (xc - yc) + 1

    return points



def draw_line(x1, y1, x2, y2):
    """Draw a line using the midpoint line algorithm."""
    glBegin(GL_POINTS)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        glVertex2f(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    glEnd()

# Handle button actions
def handle_button_action(action):
    if action == "play":
        print("Play button pressed")
        # Resume game logic
    elif action == "pause":
        print("Pause button pressed")
        #display_message("PAUSE")
    elif action == "exit":
        print("Exit button pressed")
        sys.exit(0)

# # Display message on screen
# def display_message(message):
#     glColor3f(1.0, 0.0, 0.0)  # Red color
#     glRasterPos2f(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2)
#     for char in message:
#         glutBitmapCharacter(font, ord(char))

def draw_cloud(x, y, size):
    global cloudarr
    """Draw a cartoon-style cloud using overlapping circles."""
    glColor3f(1.0, 1.0, 1.0)  # Pure white color for the cloud
    
    # Draw three main circles for cloud body
    
    arr1=draw_circle1(x - size * 0.6, y - size * 0.3, size * 0.8)  # Left circle
    arr2=draw_circle1(x + size * 0.6, y - size * 0.3, size * 0.8)  # Right circle
    
    # Add gradient effect with a lighter shade
    glColor3f(0.9, 0.9, 1.0)  # Slightly lighter for gradient
    arr3=draw_circle1(x, y + size * 0.2, size * 0.6)  # Top highlight
    cloudarr.append(arr1)
    cloudarr.append(arr2)
    cloudarr.append(arr3)

def draw_jet(x, y, color, direction=1):
    """
    Draw a jet with body and triangular nose.
    direction: 1 for right-facing, -1 for left-facing
    """
    glColor3f(1, 1, 0)  # Yellow Jet Body
    draw_line(x, y, x + (20 * direction), y)  # Body Line

    glColor3f(1, 0, 0)  # Red Jet Nose (Triangle)
    glBegin(GL_TRIANGLES)
    glVertex2f(x + (20 * direction), y + 5)  # Top point of the nose
    glVertex2f(x + (20 * direction), y - 5)  # Bottom point of the nose
    glVertex2f(x + (35 * direction), y)      # Front point of the nose
    glEnd()

    glColor3f(1, 1, 0)  # Yellow for the wings
    draw_line(x + (10 * direction), y + 5, x, y + 15)  # Top Wing (Middle Part)
    draw_line(x + (10 * direction), y - 5, x, y - 15)  # Bottom Wing (Middle Part)


def update_positions():
    """Update jet positions and check for collisions."""
    global jet1_x, jet1_y, jet2_x, jet2_y, jet1_active, jet2_active
    
    # Update positions of active jets
    if jet1_active:
        if keys.get(b'w') and jet1_y + JET_SPEED <= SCREEN_HEIGHT:
            jet1_y += JET_SPEED
        if keys.get(b's') and jet1_y - JET_SPEED >= 0:
            jet1_y -= JET_SPEED
        if keys.get(b'a') and jet1_x - JET_SPEED >= 0:
            jet1_x -= JET_SPEED
        if keys.get(b'd') and jet1_x + JET_SPEED <= SCREEN_WIDTH:
            jet1_x += JET_SPEED

    if jet2_active:
        if keys.get(b'i') and jet2_y + JET_SPEED <= SCREEN_HEIGHT:
            jet2_y += JET_SPEED
        if keys.get(b'k') and jet2_y - JET_SPEED >= 0:
            jet2_y -= JET_SPEED
        if keys.get(b'j') and jet2_x - JET_SPEED >= 0:
            jet2_x -= JET_SPEED
        if keys.get(b'l') and jet2_x + JET_SPEED <= SCREEN_WIDTH:
            jet2_x += JET_SPEED

    # Move projectiles and check collisions
    for projectile in projectiles[:]:
        projectile.move()
        if jet1_active and projectile.check_collision(jet1_x, jet1_y):
            jet1_active = False
        if jet2_active and projectile.check_collision(jet2_x, jet2_y):
            jet2_active = False
        if not projectile.active:
            projectiles.remove(projectile)

    glutPostRedisplay()
def process_points(data, precision=1):
    processed_data = []
    for sublist in data:
        # Use a set to remove duplicates and round points
        rounded_points = set((round(x, precision), round(y, precision)) for x, y in sublist)
        processed_data.append(list(rounded_points))
    return processed_data
def display():
    """Render the sky, clouds, and jets."""
    global last_time, abc, cloudarr
    current_time=time.time()
    elapsed_time=current_time-last_time

    if elapsed_time >= FRAME_TIME:
        
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        
        # Draw Sky Background
        glClearColor(0.5, 0.8, 1.0, 1.0)  # Light Blue Sky
        
        # Draw Clouds
        if abc==0:
           
            draw_cloud(100, 500, 55)
            draw_cloud(350, 150, 75)
            draw_cloud(600, 400, 60)
            draw_cloud(800, 600, 65)
            # draw_cloud(100, 100, 65)
            # draw_cloud(500, 150, 75)
            
            
            
            cloudarr=process_points(cloudarr)
            
            abc+=1
        else:
            
            
            deff=0
            for i in cloudarr:
                if deff==0:
                    
                    glBegin(GL_POINTS)
                    glColor3f(0.9, 0.9, 1.0)
                    for j in i:
                        glVertex2f(j[0],j[1])
                    deff+=1
                    glEnd() 
                    
                else:
                    glBegin(GL_POINTS)
                    glColor3f(1.0, 1.0, 1.0)
                    for j in i:
                        glVertex2f(j[0],j[1])
                    if deff==2:
                        deff=0
                    else:
                        deff+=1
                    glEnd() 
               
        # Draw Jets if active
        if jet1_active:
            draw_jet(jet1_x, jet1_y, (1, 0, 0), direction=1)  # Player 1 Jet
        if jet2_active:
            draw_jet(jet2_x, jet2_y, (0, 0, 1), direction=-1)  # Player 2 Jet


        # Draw Projectiles
        for projectile in projectiles:
            projectile.draw()
        
        glutSwapBuffers()


def key_pressed(key, x, y):
    keys[key] = True
    if key == b'f' and  jet1_active:  # Player 1 fires
        projectile = Projectile(jet1_x + 35, jet1_y, 1, (1, 0, 0))  # Red projectile
        projectiles.append(projectile)
    elif key == b' ' and jet2_active:  # Player 2 fires
        projectile = Projectile(jet2_x - 35, jet2_y, -1, (0, 0, 1))  # Blue projectile
        projectiles.append(projectile)

def key_released(key, x, y):
    keys[key] = False

def init():
    """Initialize OpenGL settings."""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # sky blue background
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)  # Set 2D coordinate system
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPointSize(5.0)  # Slightly larger points for visibility

def main():
    
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(b"Airborne Fury - Jet Battle")
        
        init()
        glutDisplayFunc(display)
        glutIdleFunc(update_positions)
        glutKeyboardFunc(key_pressed)
        glutKeyboardUpFunc(key_released)
    
        glutMainLoop()


if __name__ == "__main__":
    main()