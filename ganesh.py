import pygame
import sys
import math
import random

# -------------------- Pygame Setup --------------------
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Ganesha with Moving Diya & Mantra")

# Colors
WHITE = (255, 255, 255)
GLOW_COLOR = (255, 153, 51)
FLAME_COLOR = (255, 200, 0)
SPARKLE_COLOR = (255, 255, 150)
TEXT_COLOR = (255, 0, 0)

# Load images
ganesha_img = pygame.image.load("ganesha.png").convert_alpha()
ganesha_img = pygame.transform.smoothscale(ganesha_img, (350, 350))

try:
    flame_img = pygame.image.load("diya_flame.png").convert_alpha()
    flame_img = pygame.transform.smoothscale(flame_img, (30, 50))
except:
    flame_img = None

# Font
try:
    font = pygame.font.Font("NotoSansDevanagari-Regular.ttf", 48)  # Devanagari font
except:
    font = pygame.font.SysFont(None, 48)

# -------------------- Sparkle Class --------------------
class Sparkle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(2, 4)
        self.speed = random.uniform(0.2, 1.0)
        self.opacity = random.randint(100, 255)

    def update(self):
        self.y -= self.speed
        self.opacity -= 1
        if self.y < 0 or self.opacity <= 0:
            self.__init__()

    def draw(self, surf):
        pygame.draw.circle(surf, (*SPARKLE_COLOR, self.opacity), (int(self.x), int(self.y)), self.size)

sparkles = [Sparkle() for _ in range(50)]

# -------------------- Play Mantra Audio --------------------
pygame.mixer.music.load("ganesh_mantra.mp3")  # Full Ganesh mantra audio
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)  # Loop mantra continuously

# -------------------- Clock --------------------
clock = pygame.time.Clock()
time_counter = 0

# -------------------- Fade Control --------------------
fade_duration = 3  # seconds
fade_alpha = 0
fade_in = True

# -------------------- Diya Orbit Settings --------------------
diya_radius = 100  # radius of circular orbit around Ganesha
diya_angle = 0  # current angle
diya_speed = 0.02  # speed of movement

# -------------------- Main Loop --------------------
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Float animation for Ganesha
    float_offset = int(math.sin(pygame.time.get_ticks() * 0.002) * 10)

    # Glowing aura
    time_counter += 1
    glow_radius = 200 + int(math.sin(time_counter * 0.05) * 15)
    glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, (GLOW_COLOR[0], GLOW_COLOR[1], GLOW_COLOR[2], 50),
                       (WIDTH//2, HEIGHT//2 + float_offset), glow_radius)
    screen.blit(glow_surface, (0, 0))

    # Sparkles
    for s in sparkles:
        s.update()
        s.draw(screen)

    # Draw Ganesha
    ganesha_x = WIDTH//2 - ganesha_img.get_width()//2
    ganesha_y = HEIGHT//2 - ganesha_img.get_height()//2 + float_offset
    screen.blit(ganesha_img, (ganesha_x, ganesha_y))

    # -------------------- Diya Movement --------------------
    # Circular orbit around Ganesha
    diya_angle += diya_speed
    diya_x = WIDTH//2 + int(diya_radius * math.cos(diya_angle)) - 15  # 15 = half flame width
    diya_y = HEIGHT//2 + int(diya_radius * math.sin(diya_angle)) - 25  # 25 = half flame height

    # Optional: follow mouse when near Ganesha
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if abs(mouse_x - WIDTH//2) < 150 and abs(mouse_y - HEIGHT//2) < 150:
        diya_x, diya_y = mouse_x - 15, mouse_y - 25

    # Draw flame
    flame_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    if flame_img:
        flame = pygame.transform.rotozoom(flame_img, 0, 1.0)
        screen.blit(flame, (diya_x, diya_y))
    else:
        pygame.draw.circle(flame_surface, (FLAME_COLOR[0], FLAME_COLOR[1], 0, 180),
                           (diya_x + 15, diya_y + 25), 20)
        screen.blit(flame_surface, (0, 0))

    # -------------------- Fade Logic for Mantra --------------------
    if fade_in:
        fade_alpha += 255 / (fade_duration * 60)
        if fade_alpha >= 255:
            fade_alpha = 255
            fade_in = False
    else:
        fade_alpha -= 255 / (fade_duration * 60)
        if fade_alpha <= 0:
            fade_alpha = 0
            fade_in = True

    # Draw mantra text with fade
    mantra_surf = font.render("ॐ गणेशाय नमः", True, TEXT_COLOR)
    mantra_surf.set_alpha(int(fade_alpha))
    screen.blit(mantra_surf, (WIDTH//2 - mantra_surf.get_width()//2, HEIGHT - 100))

    # -------------------- Event Handling --------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

# Stop mantra audio when exiting
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
