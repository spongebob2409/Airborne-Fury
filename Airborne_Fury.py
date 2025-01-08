from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random 
import sys 
import time
abc=0
birdie= False
TARGET_FPS=120
FRAME_TIME= 1/TARGET_FPS
last_time = time.time()
last_time_jet1 = 0
last_time_jet2 = 0
poweruptimer=0
winner=""
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_STATE="Main Menu"
birds = []  # List to store birds
BIRD_SPEED_RANGE = (2, 5)
BIRD_SIZE_RANGE = (10, 30)

# Jet positions
jet1_x, jet1_y = 200, 300
jet2_x, jet2_y = 600, 300

# Movement speed
JET1_SPEED = 10
PROJECTILE1_SPEED = 30  # Speed for projectiles
JET2_SPEED = 10
PROJECTILE2_SPEED = 30  # Speed for projectiles

# Key states
keys = {}

# Jet states (active or destroyed)
jet1_active = True
jet2_active = True
jet1_health = 100
jet2_health = 100
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
        # """Move the projectile in the specified direction."""
        if self.direction == 1:

            self.x += PROJECTILE1_SPEED * self.direction
            if self.x < 0 or self.x > SCREEN_WIDTH:
                self.active = False
        else:   
            self.x += PROJECTILE2_SPEED * self.direction
            if self.x < 0 or self.x > SCREEN_WIDTH:
                self.active = False

    def draw(self):
        if self.active:
            glColor3f(self.color[0], self.color[1], self.color[2])
            glBegin(GL_POINTS)
            glVertex2f(self.x, self.y)
            glEnd()

    def check_collision(self, jet_x, jet_y):
        # """Check if the projectile hits a jet."""
        if self.active and abs(self.x - jet_x) < 20 and abs(self.y - jet_y) < 20:
            self.active = False
            return True
        return False
# List to hold projectiles
projectiles = []
class powerups:
    def __init__(  self, x, y, color, type):
        self.x = x
        self.y = y
        self.color = color
        self.active = True
        self.radius = 15
        self.type=type
    def draw(self):
        if self.active:
            glColor3f(self.color[0], self.color[1], self.color[2])
            draw_circle(self.x, self.y, self.radius)
            if self.type=="health":
                glColor3f(1,1,1)
                draw_text(self.x-10,self.y-8,"+", font=GLUT_BITMAP_TIMES_ROMAN_24)
            elif self.type=="speed":
                glColor3f(1,1,1)
                draw_text(self.x-10,self.y-8,">>", font=GLUT_BITMAP_TIMES_ROMAN_24)
            elif self.type=="projectile":
                glColor3f(1,1,1)
                draw_text(self.x-10,self.y-8,"=>", font=GLUT_BITMAP_TIMES_ROMAN_24)
    def check_collision(self, jet_x, jet_y):
        # """Check if the projectile hits a jet."""
        if self.active and abs(self.x - jet_x) < 20 and abs(self.y - jet_y) < 20:
            self.active = False
            return True
        return False
powerup=[]

class lightning:
    def __init__(self, x, y, color, direction):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.active = True
    def draw(self):
        if self.active:
            glColor3f(self.color[0], self.color[1], self.color[2])
            draw_line(self.x, self.y, self.x + (20 * self.direction), self.y)
    def check_collision(self, jet_x, jet_y):
        # """Check if the projectile hits a jet."""
        if self.active and abs(self.x - jet_x) < 20 and abs(self.y - jet_y) < 20:
            self.active = False
            return True
        return False
    
class Bird:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.active = True

    def move(self):
        self.x -= self.speed
        if self.x < 0:
            self.active = False
    
    def draw(self):
        """Render the bird as a custom shape resembling the uploaded image."""
        
        if not self.active:
            return

        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        if self.speed_x < 0:  # Flip the bird if moving left
            glScalef(-1, 1, 1)
        
        glColor3f(1.0, 1.0, 1.0)  # White body

# First triangle
        draw_filled_triangle(
            int(0), int(0),                             # Vertex 1
            int(-self.size), int(-self.size * 0.5),     # Vertex 2
            int(0), int(-self.size)                     # Vertex 3
        )

        # Second triangle
        draw_filled_triangle(
            int(0), int(0),                             # Vertex 1
            int(0), int(-self.size),                    # Vertex 2
            int(self.size * 0.8), int(-self.size * 0.5) # Vertex 3
        )


        # Beak
        
        glColor3f(1.0, 0.5, 0.0)  # Orange
        draw_filled_triangle(
            int(self.size * 0.8), int(-self.size * 0.25),  # First vertex
            int(self.size * 1.2), int(-self.size * 0.5),  # Second vertex
            int(self.size * 0.8), int(-self.size * 0.75), # Third vertex
                                 # Color (R, G, B)
        )
        
        glColor3f(0.0, 0.0, 0.0)  # Black wings
        draw_filled_triangle(
            int(-self.size * 0.5), int(-self.size * 0.25),  # First vertex
            int(-self.size * 1.5), int(-self.size * 0.75),  # Second vertex
            int(0), int(-self.size)                         # Third vertex
        )
        # Wings
        
        glPopMatrix()

    def update(self):
        """Update bird position."""
        self.x += self.speed_x
        self.y += self.speed_y
        # Wrap-around logic to ensure birds reappear from the other side
        if self.x > SCREEN_WIDTH + self.size:
            self.x = -self.size
        elif self.x < -self.size:
            self.x = SCREEN_WIDTH + self.size

        if self.y > SCREEN_HEIGHT + self.size:
            self.y = -self.size
        elif self.y < -self.size:
            self.y = SCREEN_HEIGHT + self.size

    def check_collision(self, jet_x, jet_y):
        """Check if the bird collides with the jet."""
        return self.active and (self.x - jet_x)**2 + (self.y - jet_y)**2 <= self.size**2
birds = [
    Bird(
        random.randint(0, SCREEN_WIDTH),
        random.randint(0, SCREEN_HEIGHT),
        random.randint(15, 30),
        random.uniform(-3, 3),
        random.uniform(-3, 3),
    )
    for _ in range(5)
]
fire_active = False
fire_x = 0
fire_y = 0
def draw_filled_rectangle(x_min, y_min, x_max, y_max):
    """Draw a filled rectangle by filling it with horizontal lines."""
    for y in range(y_min, y_max + 1):
        draw_line(x_min, y, x_max, y)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))

def spawn_bird():
    size = random.randint(*BIRD_SIZE_RANGE)
    speed = random.uniform(*BIRD_SPEED_RANGE)
    x = SCREEN_WIDTH
    y = random.randint(0, SCREEN_HEIGHT)
    birds.append(Bird(x, y, size, speed, random.uniform(-1, 1)))
def draw_fire(x, y):
    """Draw a fire effect at the given position."""
    glColor3f(1.0, 0.0, 0.0)  # Red color
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x - 10, y - 20)
    glVertex2f(x + 10, y - 20)
    glEnd()

    glColor3f(1.0, 0.5, 0.0)  # Orange flames
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y - 10)
    glVertex2f(x - 5, y - 25)
    glVertex2f(x + 5, y - 25)
    glEnd()
def draw_circle(x, y, radius):
    # """Draw a filled circle using the midpoint circle algorithm."""
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

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        self.create_particles()

    def create_particles(self):
        for _ in range(50):  # Number of particles
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-1, 1),
                'life': random.uniform(0.5, 1.5)
            }
            self.particles.append(particle)

    def update(self, dt):
        for particle in self.particles:
            particle['x'] += particle['dx'] * dt
            particle['y'] += particle['dy'] * dt
            particle['life'] -= dt
        self.particles = [p for p in self.particles if p['life'] > 0]

    def draw(self):
        glColor3f(1, 0.5, 0)  # Orange color for explosion
        for particle in self.particles:
            # draw_filled_rectangle(int(particle['x']), int(particle['y']), int(particle['x'] + 2), int(particle['y'] + 2))
            # glColor3f(1, 0.2, 0)  # Orange color for explosion
            draw_circle(int(particle['x']-random.choice([3,1,2,4])), int(particle['y']-random.choice([3,1,2,4])), random.choice([1,2,3,4]))
def check_collision(projectile, jet):
    # Simple collision detection logic
    return (projectile.x > jet.x and projectile.x < jet.x + jet.width and
            projectile.y > jet.y and projectile.y < jet.y + jet.height)

explosions = []
def draw():
    # Existing draw code...
    for explosion in explosions:
        explosion.draw()
def update(dt):
    # Existing update code...
    for explosion in explosions:
        explosion.update(dt)
def draw_circle1(x, y, radius, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
    # """
    # Draw a filled circle using the midpoint circle algorithm.

    # Args:
    # x (int): x-coordinate of the circle's center.
    # y (int): y-coordinate of the circle's center.
    # radius (int): Radius of the circle.
    # screen_width (int): Width of the screen.
    # screen_height (int): Height of the screen.

    # Returns:
    # list: A list of points to be drawn for the filled circle.
    # """
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

def draw_rectengle(x1, y1, x2, y2):
    glBegin(GL_POINTS)
    for x in range(x1, x2 + 1):
        glVertex2f(x, y1)
        glVertex2f(x, y2)
    for y in range(y1, y2 + 1):
        glVertex2f(x1, y)
        glVertex2f(x2, y)
    glEnd()

def draw_line(x1, y1, x2, y2, width=1):
    """
    Draw a line using the midpoint line algorithm with adjustable width.
    
    Parameters:
        x1, y1: Start point of the line.
        x2, y2: End point of the line.
        width: Width of the line (default is 1 pixel).
    """
    glBegin(GL_POINTS)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    half_width = width // 2  # Determine the range for width adjustment
    
    while True:
        # Draw multiple points around the main line for the width
        for w in range(-half_width, half_width + 1):
            if dx > dy:
                glVertex2f(x1, y1 + w)  # Adjust perpendicular to the x-axis
            else:
                glVertex2f(x1 + w, y1)  # Adjust perpendicular to the y-axis
        
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

def draw_triangle(x1, y1, x2, y2, x3, y3):
    """
    Draw a triangle using the draw_line function.

    Parameters:
        x1, y1: Coordinates of the first vertex.
        x2, y2: Coordinates of the second vertex.
        x3, y3: Coordinates of the third vertex.
    """
    # Draw the edges of the triangle
    draw_line(x1, y1, x2, y2)  # Line from vertex 1 to vertex 2
    draw_line(x2, y2, x3, y3)  # Line from vertex 2 to vertex 3
    draw_line(x3, y3, x1, y1)  # Line from vertex 3 to vertex 1
def draw_filled_triangle(x1, y1, x2, y2, x3, y3):
    """
    Draw a filled triangle using a scanline approach.

    Parameters:
        x1, y1: Coordinates of the first vertex.
        x2, y2: Coordinates of the second vertex.
        x3, y3: Coordinates of the third vertex.
    """
    # Sort the vertices by y-coordinate (y1 <= y2 <= y3)
    vertices = sorted([(x1, y1), (x2, y2), (x3, y3)], key=lambda v: v[1])
    x1, y1 = vertices[0]
    x2, y2 = vertices[1]
    x3, y3 = vertices[2]

    def interpolate(y, y0, x0, y1, x1):
        """Linear interpolation for x based on y."""
        if y1 == y0:
            return x0  # Avoid division by zero
        return x0 + (x1 - x0) * (y - y0) / (y1 - y0)

    glBegin(GL_POINTS)
    for y in range(y1, y3 + 1):
        if y < y2:
            # Interpolate x values for the lower part of the triangle
            xa = interpolate(y, y1, x1, y2, x2)
            xb = interpolate(y, y1, x1, y3, x3)
        else:
            # Interpolate x values for the upper part of the triangle
            xa = interpolate(y, y2, x2, y3, x3)
            xb = interpolate(y, y1, x1, y3, x3)

        # Ensure xa is the left-most point
        if xa > xb:
            xa, xb = xb, xa

        # Draw a horizontal line between xa and xb
        for x in range(int(xa), int(xb) + 1):
            glVertex2f(x, y)
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
    # """Draw a cartoon-style cloud using overlapping circles."""
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
    # """
    # Draw a jet with body and triangular nose.
    # direction: 1 for right-facing, -1 for left-facing
    # """
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

def mouse_click(button, state, x, y):
    global GAME_STATE, jet1_active, jet2_active, jet1_health, jet2_health, jet1_x, jet1_y, jet2_x, jet2_y, projectiles, birds, fire_active, fire_x, fire_y, winner, powerup, poweruptimer, JET2_SPEED, JET1_SPEED, PROJECTILE1_SPEED, PROJECTILE2_SPEED
    y=SCREEN_HEIGHT-y
    if state == GLUT_DOWN:  # Mouse button pressed
        if button == GLUT_LEFT_BUTTON:
            if x>250 and x<550 and y>250 and y<350 and GAME_STATE=="Main Menu":
                GAME_STATE="Main Game"
            if x>250 and x<550 and y>150 and y<200 and GAME_STATE=="Game Over":
                GAME_STATE="Main Game"
                jet1_active = True
                jet2_active = True
                jet1_health = 100
                jet2_health = 100
                jet1_x, jet1_y = 200, 300
                jet2_x, jet2_y = 600, 300
                projectiles = []

                birds = []
                fire_active = False
                fire_x = 0
                fire_y = 0
                winner=""
                powerup=[]
                poweruptimer=0
                JET2_SPEED = 10
                JET1_SPEED = 10
                PROJECTILE1_SPEED = 30  # Speed for projectiles
                PROJECTILE2_SPEED = 30  # Speed for projectiles
                
            print(x,y)
            print(f"Left button clicked at ({x}, {y})")

        elif button == GLUT_RIGHT_BUTTON:
            print(f"Right button clicked at ({x}, {y})")
        elif button == GLUT_MIDDLE_BUTTON:
            print(f"Middle button clicked at ({x}, {y})")
def update_positions():
    # """Update jet positions and check for collisions."""
    global jet1_x, jet1_y, jet2_x, jet2_y, jet1_active, jet2_active, jet1_health, jet2_health, last_time, poweruptimer, powerup, JET2_SPEED, JET1_SPEED, PROJECTILE1_SPEED, PROJECTILE2_SPEED, GAME_STATE, winner
    current_time = time.time()
    # Update positions of active jets
    if jet1_active:
        if keys.get(b'w') and jet1_y + JET1_SPEED <= SCREEN_HEIGHT:
            jet1_y += JET1_SPEED
        if keys.get(b's') and jet1_y - JET1_SPEED >= 0:
            jet1_y -= JET1_SPEED
        if keys.get(b'a') and jet1_x - JET1_SPEED >= 0:
            jet1_x -= JET1_SPEED
        if keys.get(b'd') and jet1_x + JET1_SPEED <= SCREEN_WIDTH:
            jet1_x += JET1_SPEED

    if jet2_active:
        if keys.get(b'i') and jet2_y + JET2_SPEED <= SCREEN_HEIGHT:
            jet2_y += JET2_SPEED
        if keys.get(b'k') and jet2_y - JET2_SPEED >= 0:
            jet2_y -= JET2_SPEED
        if keys.get(b'j') and jet2_x - JET2_SPEED >= 0:
            jet2_x -= JET2_SPEED
        if keys.get(b'l') and jet2_x + JET2_SPEED <= SCREEN_WIDTH:
            jet2_x += JET2_SPEED

    # Move projectiles and check collisions
    for projectile in projectiles[:]:
        projectile.move()
        if jet1_active and projectile.check_collision(jet1_x, jet1_y):
            jet1_health -= 30
            explosions.append(Explosion(jet1_x, jet1_y))
            if jet1_health <= 0:
                jet1_active = False
            # jet1_active = False
        if jet2_active and projectile.check_collision(jet2_x, jet2_y):
            jet2_health -= 30
            if jet2_health <= 0:
                jet2_active = False
            explosions.append(Explosion(jet2_x, jet2_y))
        if not projectile.active:
            projectiles.remove(projectile)
    
    for bird in birds[:]:
        bird.update()
        if bird.check_collision(jet1_x, jet1_y):
            bird.active = False
            jet1_health -= 50
            if jet1_health <= 0:
                jet1_active = False
            explosions.append(Explosion(bird.x, bird.y))

            fire_active = True
            fire_x, fire_y = jet1_x, jet1_y
        elif bird.check_collision(jet2_x, jet2_y):
            bird.active = False
            jet2_health -= 50
            if jet2_health <= 0:
                jet2_active = False
            explosions.append(Explosion(bird.x, bird.y))
            fire_active = True
            fire_x, fire_y = jet2_x, jet2_y
        for i in projectiles:
            if i.check_collision(bird.x, bird.y):
                bird.active=False
                explosions.append(Explosion(bird.x, bird.y))    
        
        if not bird.active:
            birds.remove(bird)
    if jet1_active==False or jet2_active==False:
        if jet1_active==False:
            winner="Player 2"
        else:
            winner="Player 1"
        GAME_STATE="Game Over"
    # Randomly spawn birds
    if random.random() < 0.01:  # Adjust spawn probability
        spawn_bird()
    if len(powerup)==0:
        val= random.choice(["health","speed","projectile"])
        color=(1,0,0)
        if val=="health":
            color=(0,1,0)
        if val=="speed":
            color=(0,0,1)
        if val=="projectile":
            color=(1,0,1)
        powerup.append(powerups(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT),color, val))
        # powerup.append(powerups(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT),(1,0,0)))
        # powerup.append(powerups(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT),(1,0,0)))
    if current_time-poweruptimer>10:
        # powerup.append(powerups(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT),(1,0,0)))
        powerup=[]
        poweruptimer=current_time
    if len(powerup)!=0:
        # print(jet1_health,jet2_health)
        for i in powerup:
            if i.type=="health":
                if i.check_collision(jet1_x, jet1_y):
                    
                    jet1_health+=25
                    if jet1_health>100:
                        jet1_health=100
                if i.check_collision(jet2_x, jet2_y):
                    jet2_health+=25
                    if jet2_health>100:
                        jet2_health=100
            if i.type=="speed":
                if i.check_collision(jet1_x, jet1_y):
                    JET1_SPEED+=5
                if i.check_collision(jet2_x, jet2_y):
                    JET2_SPEED+=5
            if i.type=="projectile":
                if i.check_collision(jet1_x, jet1_y):
                    PROJECTILE1_SPEED+=10
                if i.check_collision(jet2_x, jet2_y):
                    PROJECTILE2_SPEED+=10
        dt=current_time-last_time
        for explosion in explosions:
            explosion.update(dt)    
        # print(jet1_health,jet2_health)
    glutPostRedisplay()
def process_points(data, precision=1):
    processed_data = []
    for sublist in data:
        # Use a set to remove duplicates and round points
        rounded_points = set((round(x, precision), round(y, precision)) for x, y in sublist)
        processed_data.append(list(rounded_points))
    return processed_data

def render_birds():
    for bird in birds:
        bird.draw()
def render_fire():
    if fire_active:
        draw_fire(fire_x, fire_y)
def display():
    # """Render the sky, clouds, and jets."""
    global last_time, abc, cloudarr, jet1_active, jet2_active, jet1_x, jet1_y, jet2_x, jet2_y, projectiles, birds, fire_active, fire_x, fire_y, birdie, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_STATE
    current_time=time.time()
    elapsed_time=current_time-last_time
    last_time=current_time
    if abc==0:
           
            draw_cloud(100, 500, 50)
            draw_cloud(350, 450, 30)
            draw_cloud(600, 400, 60)
            draw_cloud(800, 600, 65)
            draw_cloud(100, 100, 65)
            draw_cloud(500, 150, 75)
            abc+=1
            cloudarr=process_points(cloudarr)
            abc+=1
    # if game_state == "Main Menu":
    #     # Draw Main Menu background
    #     draw_rectangle(0.0, 0.0, window_width, window_height, (0.2, 0.2, 0.2))

    #     # Draw Main Menu title
    #     draw_main_menu_text()

    #     # Draw Main Menu buttons
    #     draw_buttons("Main Menu")
    if elapsed_time >= FRAME_TIME:
        
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        
        # Draw Sky Background
        glClearColor(0.5, 0.8, 1.0, 1.0)
        if GAME_STATE=="Main Menu":
            birdie=True
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
            glColor3f(1.0, 0.6, 0.5)
            draw_filled_rectangle(250, 250, 550, 350)
            glColor3f(1.0, 1.0, 1.0)
            draw_rectengle(250, 250, 550, 350)
            glColor3f(1.0, 1.0, 1.0)
            draw_text(SCREEN_WIDTH // 2 -70 , SCREEN_HEIGHT // 2- 10, "Let's FLY!!!!!", font=GLUT_BITMAP_TIMES_ROMAN_24)
        elif GAME_STATE=="Main Game":    
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
            if birdie:
                birds=[]
                birdie=False
            
            # Draw Jets if active
            if jet1_active:
                draw_jet(jet1_x, jet1_y, (1, 0, 0), direction=1)  # Player 1 Jet
            if jet2_active:
                draw_jet(jet2_x, jet2_y, (0, 0, 1), direction=-1)  # Player 2 Jet

            # Draw the outer unfilled rectangle
            val1=jet1_health
            val2=jet2_health
            val1= (val1/100)*200
            val2= (val2/100)*200
            if val1<0:
                val1=0
            if val2<0:
                val2=0
            glColor3f(0,0.8,0)
            draw_rectengle(50, 550, 250, 580)
            draw_rectengle(550, 550, 750, 580)
            glColor3f(0,1,0)
            draw_filled_rectangle(55, 555, 45+val1, 575)



            draw_filled_rectangle(555, 555, 545+val2, 575)
            
           

            # Draw the inner filled rectangle
            

            # Draw Projectiles
            for projectile in projectiles:
                projectile.draw()
            for i in powerup:
                i.draw()
        elif GAME_STATE=="Game Over":
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
            glColor3f(1.0, 0.6, 0.5)
            draw_filled_rectangle(250, 250, 550, 350)
            glColor3f(1.0, 1.0, 1.0)
            draw_text(SCREEN_WIDTH // 2 -70 , SCREEN_HEIGHT // 2- 0, "Game Over", font=GLUT_BITMAP_TIMES_ROMAN_24)
            draw_text(SCREEN_WIDTH // 2 -70 , SCREEN_HEIGHT // 2- 20, f"{winner} Wins", font=GLUT_BITMAP_TIMES_ROMAN_24)
            
            glColor3f(1.0, 0.6, 0.5)
            draw_filled_rectangle(250, 150, 550, 200)
            glColor3f(1.0, 1.0, 1.0)
            draw_rectengle(250, 150, 550, 200)
            glColor3f(1.0, 1.0, 1.0)
            draw_text(SCREEN_WIDTH // 2 -60 , SCREEN_HEIGHT // 2- 130, "Play Again", font=GLUT_BITMAP_TIMES_ROMAN_24)
        for bird in birds:
                bird.draw()
        for i in explosions:
            i.draw()        
        glutSwapBuffers()
# def key_pressed(key, x, y):
#     global jet1_active, jet2_active, last_time
#     keys[key] = True
#     if key == b'f' and  jet1_active:  # Player 1 fires
#         projectile = Projectile(jet1_x + 35, jet1_y, 1, (1, 0, 0))  # Red projectile
#         projectiles.append(projectile)
#     elif key == b' ' and jet2_active:  # Player 2 fires
#         projectile = Projectile(jet2_x - 35, jet2_y, -1, (0, 0, 1))  # Blue projectile
#         projectiles.append(projectile)
# import time

def key_pressed(key, x, y):
    global jet1_active, jet2_active, last_time_jet1, last_time_jet2, projectiles

    keys[key] = True
    current_time = time.time()
    
    # Delay for Jet1 (Player 1)
    if key == b'f' and jet1_active:
        if current_time - last_time_jet1 >= 0.5:  # Check if 1 second has passed
            projectile = Projectile(jet1_x + 35, jet1_y, 1, (1, 0, 0))  # Red projectile
            projectiles.append(projectile)
            last_time_jet1 = current_time  # Update the last fired time

    # Delay for Jet2 (Player 2)
    elif key == b' ' and jet2_active:
        if current_time - last_time_jet2 >= 0.5:  # Check if 1 second has passed
            projectile = Projectile(jet2_x - 35, jet2_y, -1, (0, 0, 1))  # Blue projectile
            projectiles.append(projectile)
            last_time_jet2 = current_time  # Update the last fired time

def key_released(key, x, y):
    keys[key] = False

def init():
    # """Initialize OpenGL settings."""
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
        glutMouseFunc(mouse_click)
    
        glutMainLoop()


if __name__ == "__main__":
    main()