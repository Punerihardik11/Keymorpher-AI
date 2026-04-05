import os

# Get the base directory for asset paths (parent of src folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

intro_sound = None
click_sound = None

try:
    import pygame
    # Initialize the pygame mixer without starting the whole pygame engine
    pygame.mixer.init()

    intro_path = os.path.join(BASE_DIR, "assets", "intro.wav")
    if os.path.exists(intro_path):
        intro_sound = pygame.mixer.Sound(intro_path)
        intro_sound.set_volume(0.4)
        print(f"[OK] Intro sound loaded from {intro_path}")
    else:
        print(f"[WARNING] assets/intro.wav not found at {intro_path}. Intro sound disabled.")

    click_path = os.path.join(BASE_DIR, "assets", "click.wav")
    if os.path.exists(click_path):
        click_sound = pygame.mixer.Sound(click_path)
        click_sound.set_volume(0.3)
        print(f"[OK] Click sound loaded from {click_path}")
    else:
        print(f"[WARNING] assets/click.wav not found at {click_path}. Click sound disabled.")

except ImportError:
    print("[ERROR] pygame is not installed. Run 'pip install pygame' to enable UI sounds.")
except Exception as e:
    print(f"[ERROR] Sound system initialization failed -> {e}")

def play_intro():
    """Play the application startup sound once."""
    if intro_sound:
        try:
            intro_sound.play()
        except:
            pass

def play_click():
    """Play a short, minimal UI tap sound on confirmed input."""
    if click_sound:
        try:
            click_sound.play()
        except:
            pass
