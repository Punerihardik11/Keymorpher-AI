import os
import time

# Get the base directory for asset paths (parent of src folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

intro_sound = None
click_sound = None
mixer_initialized = False

try:
    import pygame
    # Initialize the pygame mixer with larger buffer for better audio playback
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    mixer_initialized = True
    time.sleep(0.1)  # Give mixer time to stabilize
    
    intro_path = os.path.join(BASE_DIR, "assets", "intro.wav")
    if os.path.exists(intro_path):
        intro_sound = pygame.mixer.Sound(intro_path)
        intro_sound.set_volume(0.7)  # Increased from 0.4 for better audibility
        print(f"[OK] Intro sound loaded from {intro_path}")
    else:
        print(f"[WARNING] assets/intro.wav not found at {intro_path}. Intro sound disabled.")

    click_path = os.path.join(BASE_DIR, "assets", "click.wav")
    if os.path.exists(click_path):
        click_sound = pygame.mixer.Sound(click_path)
        click_sound.set_volume(0.5)  # Increased from 0.3 for better audibility
        print(f"[OK] Click sound loaded from {click_path}")
    else:
        print(f"[WARNING] assets/click.wav not found at {click_path}. Click sound disabled.")

except ImportError:
    print("[ERROR] pygame is not installed. Run 'pip install pygame' to enable UI sounds.")
except Exception as e:
    print(f"[ERROR] Sound system initialization failed -> {e}")

def play_intro():
    """Play the application startup sound once - allows time for audio to process."""
    if intro_sound and mixer_initialized:
        try:
            intro_sound.play()
            time.sleep(0.05)  # Brief delay to ensure sound starts playing
        except Exception as e:
            print(f"[WARNING] Failed to play intro sound: {e}")

def play_click():
    """Play a short, minimal UI tap sound on confirmed input."""
    if click_sound and mixer_initialized:
        try:
            click_sound.play()
        except Exception as e:
            print(f"[WARNING] Failed to play click sound: {e}")
