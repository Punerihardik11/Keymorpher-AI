import cv2
import time
import os
import sys
from hand_detection import HandDetectionController
from keyboard_display import KeyboardDisplay
from typed_text import TypedText
import numpy as np
from database import init_db, insert_user
from sound_manager import play_intro, play_click


# ===================== CONFIG =====================
# Get the base directory (parent of src folder) for asset paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORCE_SAMPLE_VIDEO = False   # True on PC (no webcam), False on laptop
SAMPLE_VIDEO_PATH = os.path.join(BASE_DIR, "sample.mp4")
# ==================================================


def get_video_source():
    if FORCE_SAMPLE_VIDEO:
        print("Forcing sample video mode.")
        return SAMPLE_VIDEO_PATH

    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        ret, frame = cap.read()
        cap.release()

        if ret and frame is not None and frame.sum() > 0:
            print("Webcam detected and usable.")
            return 0

    print("Webcam not detected or unusable. Using sample video.")
    return SAMPLE_VIDEO_PATH


def show_splash_screen():
    intro_played = False
    logo_path = os.path.join(BASE_DIR, "assets", "keymorpher-ai-logo.png")

    if not os.path.exists(logo_path):
        print(f"[ERROR] Logo file not found at {logo_path}")
        print("[ERROR] This means your assets folder might be missing.")
        print("[HELP] Try running from the project root and verify assets with:")
        print("       cd {repo_root}")
        print("       python verify_assets.py")
        print("[INFO] You can still run without splash screen. Press ENTER to continue...")
        input()
        return

    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    if logo is None:
        print("[ERROR] Failed to load the logo image.")
        return

    logo_height, logo_width = logo.shape[:2]
    scale_factor = 0.85
    target_scale = 1.0
    animation_duration = 4.0  # Extended from 1.5 to allow intro sound to play
    fps = 30
    total_frames = int(animation_duration * fps)

    window_width, window_height = 1280, 720
    background = np.zeros((window_height, window_width, 3), dtype=np.uint8)     

    watermark_height, watermark_width = 50, 150  
    if logo.shape[2] == 4:  
        logo[-watermark_height:, -watermark_width:] = (0, 0, 0, 0)
    else:  
        logo[-watermark_height:, -watermark_width:] = (0, 0, 0)

    for frame_idx in range(total_frames):
        current_scale = scale_factor + (target_scale - scale_factor) * (frame_idx / total_frames)

        new_width = int(logo_width * current_scale)
        new_height = int(logo_height * current_scale)
        resized_logo = cv2.resize(logo, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

        new_width = min(new_width, window_width)
        new_height = min(new_height, window_height)
        resized_logo = cv2.resize(logo, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

        if resized_logo.shape[2] == 4:
            resized_logo = cv2.cvtColor(resized_logo, cv2.COLOR_BGRA2BGR)       

        x_offset = (window_width - new_width) // 2
        y_offset = (window_height - new_height) // 2

        frame = background.copy()
        frame[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_logo

        alpha = frame_idx / total_frames
        overlay = cv2.addWeighted(frame, alpha, background, 1 - alpha, 0)       

        cv2.imshow("Keymorpher AI - Splash Screen", overlay)
        
        if not intro_played:
            play_intro()
            intro_played = True
            
        if cv2.waitKey(int(1000 / fps)) & 0xFF == 27:
            break

    cv2.imshow("Keymorpher AI - Splash Screen", frame)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    cv2.waitKey(1)


def main():
    # Initialize the local database
    init_db()

    video_source = get_video_source()
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    hand_detector = HandDetectionController()
    keyboard = KeyboardDisplay()
    typed_text = TypedText()

    # Form Wizard States
    current_step = "name"
    user_data = {"name": "", "roll_number": "", "branch": ""}
    data_saved = False

    last_key = None
    key_start_time = 0
    done_start_time = 0
    press_delay = 0.6

    cv2.namedWindow("Keymorpher AI", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Keymorpher AI", 1920, 1080)
    cv2.setWindowProperty("Keymorpher AI", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        success, frame = cap.read()
        if not success or frame is None:
            if video_source == SAMPLE_VIDEO_PATH:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            print("ERROR: Failed to read frame from camera")
            continue

        h, w = frame.shape[:2]
        if h == 0 or w == 0:
            print("Invalid frame size")
            continue

        # Force Full HD rendering pipeline to eliminate blur/pixelation
        frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_LINEAR)

        frame = cv2.flip(frame, 1)

        # 1. PRESERVE HAND TRACKING: detect and draw on the original bright frame
        frame, index_tip = hand_detector.detect_hand(frame)

        # 2. DIM CAMERA FEED: Darken the frame to make the UI stand out
        frame = cv2.convertScaleAbs(frame, alpha=0.7, beta=0)

        hovered_key = None
        hovered_branch = None

        if index_tip:
            if current_step in ["name", "roll_number"]:
                hovered_key = keyboard.get_key_at_position(index_tip[0], index_tip[1])
            elif current_step == "branch":
                hovered_branch = keyboard.get_branch_at_position(index_tip[0], index_tip[1])

        current_time = time.time()

        # Input Logic
        if current_step in ["name", "roll_number"]:
            if hovered_key == last_key and hovered_key is not None:
                if current_time - key_start_time >= press_delay:
                    play_click()
                    if hovered_key == "SPACE":
                        typed_text.append_text(" ")
                    elif hovered_key == "BACK":
                        typed_text.delete_text()
                    elif hovered_key == "CLEAR":
                        typed_text.clear()
                    elif hovered_key == "ENTER":
                        if current_step == "name":
                            name_input = typed_text.get_text().strip()
                            if len(name_input) < 2:
                                print("[WARNING] Name must be at least 2 characters")
                                continue
                            user_data["name"] = name_input
                            typed_text.clear()
                            current_step = "roll_number"
                        elif current_step == "roll_number":
                            roll_input = typed_text.get_text().strip()
                            if len(roll_input) < 1:
                                print("[WARNING] Roll number cannot be empty")
                                continue
                            user_data["roll_number"] = roll_input
                            typed_text.clear()
                            current_step = "branch"
                    else:
                        typed_text.append_text(hovered_key)

                    key_start_time = current_time + 0.3
            else:
                last_key = hovered_key
                key_start_time = current_time

        elif current_step == "branch":
            if hovered_branch == last_key and hovered_branch is not None:
                if current_time - key_start_time >= press_delay:
                    play_click()
                    user_data["branch"] = hovered_branch
                    current_step = "done"
                    done_start_time = current_time
            else:
                last_key = hovered_branch
                key_start_time = current_time
                
        elif current_step == "done":
            if not data_saved:
                print(f"Form completed! Data: {user_data}")
                # Store user data in lightweight SQLite DB
                insert_user(user_data["name"], user_data["roll_number"], user_data["branch"])
                data_saved = True
                
                # Reset user data completely after submission (preserving dictionary reference)
                user_data.update({
                    "name": "",
                    "roll_number": "",
                    "branch": ""
                })
            # Restart flow automatically after 5 seconds for the next user
            elif current_time - done_start_time >= 5.0:
                current_step = "name"
                data_saved = False

        # 3. USE UI LAYER: Create a separate layer for UI
        ui_layer = np.zeros_like(frame)

        if current_step == "name":
            ui_layer = keyboard.draw_header(ui_layer)
            ui_layer = keyboard.draw_prompt(ui_layer, "Enter your Name:")
            ui_layer = keyboard.draw_input_box(ui_layer, typed_text.get_text())
            ui_layer = keyboard.draw_keyboard(ui_layer, hovered_key)
        elif current_step == "roll_number":
            ui_layer = keyboard.draw_header(ui_layer)
            ui_layer = keyboard.draw_prompt(ui_layer, "Enter your Roll Number:")
            ui_layer = keyboard.draw_input_box(ui_layer, typed_text.get_text())
            ui_layer = keyboard.draw_keyboard(ui_layer, hovered_key)
        elif current_step == "branch":
            ui_layer = keyboard.draw_header(ui_layer)
            ui_layer = keyboard.draw_prompt(ui_layer, "Select your Branch:")
            ui_layer = keyboard.draw_branch_selection(ui_layer, hovered_branch)
        elif current_step == "done":
            ui_layer = keyboard.draw_header(ui_layer)
            ui_layer = keyboard.draw_final_screen(ui_layer)
        
        # 4. MERGE LAYERS: Combine dimmed frame and UI layer
        combined = cv2.addWeighted(frame, 1.0, ui_layer, 1.0, 0)

        # 5. DISPLAY FINAL OUTPUT
        cv2.imshow("Keymorpher AI", combined)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        show_splash_screen()
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()
        print("Application closed.")