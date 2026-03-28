import os

intro_sound = None
click_sound = None

try:
    import pygame
    # Initialize the pygame mixer without starting the whole pygame engine
    pygame.mixer.init()

    if os.path.exists("assets/intro.wav"):
        intro_sound = pygame.mixer.Sound("assets/intro.wav")
        intro_sound.set_volume(0.4)
    else:
        print("Warning: assets/intro.wav not found. Intro sound disabled.")

    if os.path.exists("assets/click.wav"):
        click_sound = pygame.mixer.Sound("assets/click.wav")
        click_sound.set_volume(0.3)
    else:
        print("Warning: assets/click.wav not found. Click sound disabled.")

except ImportError:
    print("Warning: pygame is not installed. Run 'pip install pygame' to enable UI sounds.")
except Exception as e:
    print(f"Warning: Sound system initialization failed -> {e}")

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
