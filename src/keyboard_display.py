import cv2
import numpy as np
import os

# Get the base directory for asset paths (parent of src folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
    """Overlay img_overlay on img at (x, y) using alpha_mask for transparency."""
    # Calculate crop areas for both images (to handle boundaries)
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])
    
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)
    
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return
    
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o] / 255.0
    
    for c in range(3):
        img_crop[:, :, c] = alpha * img_overlay_crop[:, :, c] + (1 - alpha) * img_crop[:, :, c]

def draw_rounded_rectangle(img, pt1, pt2, color, thickness, r):
    x1, y1 = pt1
    x2, y2 = pt2

    # Top left
    cv2.circle(img, (x1 + r, y1 + r), r, color, thickness)
    # Top right
    cv2.circle(img, (x2 - r, y1 + r), r, color, thickness)
    # Bottom left
    cv2.circle(img, (x1 + r, y2 - r), r, color, thickness)
    # Bottom right
    cv2.circle(img, (x2 - r, y2 - r), r, color, thickness)

    # Rectangles
    cv2.rectangle(img, (x1 + r, y1), (x2 - r, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + r), (x2, y2 - r), color, thickness)


class KeyboardDisplay:
    def __init__(self):
        # Full keyboard layout
        self.keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M"]
        ]

        self.key_width = 55
        self.key_height = 55
        self.gap = 8

        self.start_x = 40
        self.start_y = 180

        # Special keys layout mapping (Label, Width Multiplier)
        self.special_keys = [
            ("CLEAR", 2.0),
            ("SPACE", 4.0),
            ("BACK", 2.0),
            ("ENTER", 2.0)
        ]
        
        self.all_keys = [k for row in self.keys for k in row] + [k[0] for k in self.special_keys]
        self.hover_states = {k: 0.0 for k in self.all_keys}

        # Load logo for header left
        self.logo_path = os.path.join(BASE_DIR, "assets", "keyboard-symbol.png")
        if os.path.exists(self.logo_path):
            self.logo = cv2.imread(self.logo_path, cv2.IMREAD_UNCHANGED)
            if self.logo is not None:
                print(f"[OK] Keyboard symbol loaded")
            else:
                print(f"[WARNING] Failed to read keyboard-symbol.png (corrupted file?)")
                self.logo = None
        else:
            print(f"[WARNING] Keyboard symbol not found at {self.logo_path}")
            print(f"[TIP] Run 'python verify_assets.py' to check all assets")
            self.logo = None

        # Load branding text image for header right
        self.brand_text_path = os.path.join(BASE_DIR, "assets", "name.png")
        if os.path.exists(self.brand_text_path):
            self.brand_text_img = cv2.imread(self.brand_text_path, cv2.IMREAD_UNCHANGED)
            if self.brand_text_img is not None:
                print(f"[OK] Branding text loaded")
            else:
                print(f"[WARNING] Failed to read name.png (corrupted file?)")
                self.brand_text_img = None
        else:
            print(f"[WARNING] Brand text image not found at {self.brand_text_path}")
            print(f"[TIP] Run 'python verify_assets.py' to check all assets")
            self.brand_text_img = None

        # Fix: Add caching attributes that are used by _prepare_header_assets
        self.cached_logo = None
        self.cached_text = None
        self.last_frame_size = None

        # Form Wizard states
        self.branches = ["BBA", "BSC", "BCOM"]
        self.branch_hover_states = {b: 0.0 for b in self.branches}
        self.branch_hitboxes = {}

    def _update_hover_states(self, highlight_key):
        # Smooth transition: increase alpha if hovered, decrease if not
        step = 0.15
        for key in self.all_keys:
            if key == highlight_key:
                self.hover_states[key] = min(1.0, self.hover_states[key] + step)
            else:
                self.hover_states[key] = max(0.0, self.hover_states[key] - step)

    def _update_branch_hover_states(self, highlight_branch):
        step = 0.15
        for b in self.branches:
            if b == highlight_branch:
                self.branch_hover_states[b] = min(1.0, self.branch_hover_states[b] + step)
            else:
                self.branch_hover_states[b] = max(0.0, self.branch_hover_states[b] - step)

    def draw_key(self, frame, key, x, y, w, h, hover_alpha):
        # Constants for styling
        KEY_COLOR = np.array([230, 230, 230]) # BGR soft white/gray
        HOVER_COLOR = np.array([245, 216, 173]) # Soft blue (BGR)
        TEXT_COLOR = (50, 50, 50)
        SHADOW_COLOR = (120, 120, 120)
        FONT = cv2.FONT_HERSHEY_SIMPLEX
        frame_height, frame_width = frame.shape[:2]
        
        FONT_SCALE = max(0.6, frame_width / 1500.0)
        FONT_THICKNESS = max(1, int(frame_width / 800))
        CORNER_RADIUS = max(5, int(frame_width / 120))

        # Interpolate color based on hover_alpha
        current_color = KEY_COLOR * (1 - hover_alpha) + HOVER_COLOR * hover_alpha
        current_color = tuple(map(int, current_color))

        # Size adjustment based on hover (1.0 to 1.05)
        scale = 1.0 + (0.05 * hover_alpha)
        
        new_w = int(w * scale)
        new_h = int(h * scale)
        cx = x + w // 2
        cy = y + h // 2
        nx = cx - new_w // 2
        ny = cy - new_h // 2

        # Draw Shadow
        shadow_offset = int(3 + 2 * hover_alpha)
        draw_rounded_rectangle(frame, (nx + shadow_offset, ny + shadow_offset), 
                               (nx + new_w + shadow_offset, ny + new_h + shadow_offset), 
                               SHADOW_COLOR, -1, CORNER_RADIUS)

        # Draw Glow (only if hovering)
        if hover_alpha > 0:
            glow_offset = 2
            glow_color = tuple(map(lambda c: min(255, c + 50), current_color))
            draw_rounded_rectangle(frame, (nx - glow_offset, ny - glow_offset), 
                                   (nx + new_w + glow_offset, ny + new_h + glow_offset), 
                                   glow_color, -1, CORNER_RADIUS)

        # Draw Main Key
        draw_rounded_rectangle(frame, (nx, ny), (nx + new_w, ny + new_h), current_color, -1, CORNER_RADIUS)

        # Draw Text
        text_size = cv2.getTextSize(key, FONT, FONT_SCALE, FONT_THICKNESS)[0]
        text_x = nx + (new_w - text_size[0]) // 2
        text_y = ny + (new_h + text_size[1]) // 2
        cv2.putText(frame, key, (text_x, text_y), FONT, FONT_SCALE, TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    def draw_keyboard(self, frame, highlight_key=None):
        self._update_hover_states(highlight_key)

        # Extract frame dimensions
        frame_height, frame_width = frame.shape[:2]

        # Calculate dynamic dimensions based on frame size
        # Slightly reduced sizes for 1920x1080 resolution
        keyboard_width = int(frame_width * 0.85)
        keyboard_height = int(frame_height * 0.35)
        
        # Allocate rows vertically (4 for letters + 1 for special)
        num_rows = len(self.keys) + 1
        self.key_height = keyboard_height // num_rows
        self.gap = int(self.key_height * 0.15)
        
        # Recalculate actual key dimensions, subtracting gaps
        actual_key_h = self.key_height - self.gap
        self.key_width = (keyboard_width // 10) - self.gap
        
        self.start_y = frame_height - keyboard_height - int(frame_height * 0.06) # More bottom margin for accessibility
        self.hitboxes = {}
        self.HITBOX_TOLERANCE = 15  # Add 15px tolerance around hitboxes for better detection

        # Draw normal keys
        for row_index, row in enumerate(self.keys):
            row_width = len(row) * self.key_width + (len(row) - 1) * self.gap
            start_x_row = (frame_width - row_width) // 2

            for col_index, key in enumerate(row):
                x = start_x_row + col_index * (self.key_width + self.gap)
                y = self.start_y + row_index * self.key_height
                self.draw_key(frame, key, x, y, self.key_width, actual_key_h, self.hover_states[key])
                self.hitboxes[key] = (x, y, self.key_width, actual_key_h)

        # Draw special keys row
        special_y = self.start_y + len(self.keys) * self.key_height
        
        # Calculate total width of special row to perfectly center it
        total_special_w = sum([int(self.key_width * mult) for _, mult in self.special_keys]) + (len(self.special_keys) - 1) * self.gap
        current_x = (frame_width - total_special_w) // 2

        for key, multiplier in self.special_keys:
            key_w = int(self.key_width * multiplier)
            self.draw_key(frame, key, current_x, special_y, key_w, actual_key_h, self.hover_states[key])
            self.hitboxes[key] = (current_x, special_y, key_w, actual_key_h)
            current_x += key_w + self.gap

        return frame

    def _prepare_header_assets(self, frame_height, frame_width):
        if self.last_frame_size == (frame_width, frame_height):
            return

        self.last_frame_size = (frame_width, frame_height)
        header_height = int(frame_height * 0.1)
        padding = int(header_height * 0.2)
        target_h = header_height - (padding * 2)

        if self.logo is not None:
            aspect = self.logo.shape[1] / self.logo.shape[0]
            target_w = int(target_h * aspect)
            self.cached_logo = cv2.resize(self.logo, (target_w, target_h), interpolation=cv2.INTER_AREA)

        if self.brand_text_img is not None:
            aspect = self.brand_text_img.shape[1] / self.brand_text_img.shape[0]
            target_w = int(target_h * aspect)
            self.cached_text = cv2.resize(self.brand_text_img, (target_w, target_h), interpolation=cv2.INTER_AREA)

    def draw_header(self, frame):
        frame_height, frame_width = frame.shape[:2]
        self._prepare_header_assets(frame_height, frame_width)
        
        header_height = int(frame_height * 0.1)
        padding = int(header_height * 0.2)

        # Draw left logo
        if self.cached_logo is not None:
            logo_x = padding
            logo_y = padding
            h, w = self.cached_logo.shape[:2]
            if self.cached_logo.shape[2] == 4:
                overlay_image_alpha(frame, self.cached_logo[:, :, :3], logo_x, logo_y, self.cached_logo[:, :, 3])
            else:
                frame[logo_y:logo_y+h, logo_x:logo_x+w] = self.cached_logo

        # Draw right text brand
        if self.cached_text is not None:
            h, w = self.cached_text.shape[:2]
            text_x = frame_width - w - padding
            text_y = padding
            if self.cached_text.shape[2] == 4:
                overlay_image_alpha(frame, self.cached_text[:, :, :3], text_x, text_y, self.cached_text[:, :, 3])
            else:
                frame[text_y:text_y+h, text_x:text_x+w] = self.cached_text

        return frame

    def draw_prompt(self, frame, text):
        frame_height, frame_width = frame.shape[:2]
        header_height = int(frame_height * 0.1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1.2
        thickness = 2
        color = (230, 230, 230)
        
        text_size = cv2.getTextSize(text, font, scale, thickness)[0]
        text_x = (frame_width - text_size[0]) // 2
        # Position below header but above input box:
        text_y = header_height + int(frame_height * 0.08)
        
        cv2.putText(frame, text, (text_x, text_y), font, scale, color, thickness, cv2.LINE_AA)
        return frame

    def draw_input_box(self, frame, text):
        frame_height, frame_width = frame.shape[:2]
        header_height = int(frame_height * 0.1)
        
        box_w = int(frame_width * 0.8)
        box_h = int(frame_height * 0.1)
        box_x = (frame_width - box_w) // 2
        box_y = header_height + int(frame_height * 0.15) # Position below header
        
        CORNER_RADIUS = 15
        
        # Draw soft shadow
        draw_rounded_rectangle(frame, (box_x+3, box_y+3), (box_x+box_w+3, box_y+box_h+3), (120, 120, 120), -1, CORNER_RADIUS)
        
        # Draw main clean input box
        draw_rounded_rectangle(frame, (box_x, box_y), (box_x+box_w, box_y+box_h), (250, 250, 250), -1, CORNER_RADIUS)
        
        # Draw user text right-aligned against a clean margin, with a cursor
        FONT = cv2.FONT_HERSHEY_SIMPLEX
        FONT_SCALE = max(0.8, frame_width / 1200.0)
        FONT_THICKNESS = max(1, int(frame_width / 600))
        
        display_text = "> " + text + "|"
        text_size = cv2.getTextSize(display_text, FONT, FONT_SCALE, FONT_THICKNESS)[0]

        # Center vertically and align left
        text_x = box_x + int(frame_width * 0.02)
        text_y = box_y + (box_h + text_size[1]) // 2

        cv2.putText(frame, display_text, (text_x, text_y), FONT, FONT_SCALE, (60, 60, 60), FONT_THICKNESS, cv2.LINE_AA)
        
        return frame

    def get_key_at_position(self, x, y):
        # Use hitboxes calculated during the last draw_keyboard
        if not hasattr(self, 'hitboxes'):
            return None

        tolerance = getattr(self, 'HITBOX_TOLERANCE', 15)
        
        for key, (bx, by, bw, bh) in self.hitboxes.items():
            # Add tolerance padding around hitboxes for better proximity detection
            # Especially important for bottom keys when hands are close
            if (bx - tolerance) <= x <= (bx + bw + tolerance) and (by - tolerance) <= y <= (by + bh + tolerance):
                return key

        return None


    def draw_branch_selection(self, frame, highlight_branch=None):
        self._update_branch_hover_states(highlight_branch)
        frame_height, frame_width = frame.shape[:2]
        
        box_w = int(frame_width * 0.25)
        box_h = int(frame_height * 0.15)
        gap = int(frame_width * 0.05)
        start_x = (frame_width - (box_w * 3 + gap * 2)) // 2
        start_y = frame_height // 2
        
        self.branch_hitboxes.clear()
        
        for i, branch in enumerate(self.branches):
            hover_alpha = self.branch_hover_states[branch]
            x = start_x + i * (box_w + gap)
            y = start_y
            
            # Hover transition logic
            base_color = np.array([230, 230, 230])
            # Blue highlight! Note BGR format: (250, 150, 50) roughly
            hover_color = np.array([255, 180, 50])
            
            current_color = base_color * (1 - hover_alpha) + hover_color * hover_alpha
            current_color = tuple(map(int, current_color))
            
            scale = 1.0 + (0.05 * hover_alpha)
            new_w = int(box_w * scale)
            new_h = int(box_h * scale)
            cx, cy = x + box_w // 2, y + box_h // 2
            nx, ny = cx - new_w // 2, cy - new_h // 2
            
            CORNER_RADIUS = 15
            shadow_offset = int(4 + 2 * hover_alpha)
            draw_rounded_rectangle(frame, (nx + shadow_offset, ny + shadow_offset), 
                                   (nx + new_w + shadow_offset, ny + new_h + shadow_offset), 
                                   (120, 120, 120), -1, CORNER_RADIUS)
                                   
            draw_rounded_rectangle(frame, (nx, ny), (nx + new_w, ny + new_h), current_color, -1, CORNER_RADIUS)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.5
            font_thickness = 3
            text_size = cv2.getTextSize(branch, font, font_scale, font_thickness)[0]
            text_x = nx + (new_w - text_size[0]) // 2
            text_y = ny + (new_h + text_size[1]) // 2
            
            cv2.putText(frame, branch, (text_x, text_y), font, font_scale, (50, 50, 50), font_thickness, cv2.LINE_AA)
            self.branch_hitboxes[branch] = (nx, ny, new_w, new_h)
            
        return frame

    def get_branch_at_position(self, x, y):
        for branch, (bx, by, bw, bh) in self.branch_hitboxes.items():
            if bx <= x <= bx + bw and by <= y <= by + bh:
                return branch
        return None

    def draw_final_screen(self, frame):
        frame_height, frame_width = frame.shape[:2]
        
        msg = "Thank you for your response!"
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1.5
        thickness = 3
        color = (250, 250, 250)
        
        text_size = cv2.getTextSize(msg, font, scale, thickness)[0]
        text_x = (frame_width - text_size[0]) // 2
        text_y = (frame_height // 2) - 50
        
        cv2.putText(frame, msg, (text_x, text_y), font, scale, color, thickness, cv2.LINE_AA)
        
        # Draw logo below if available
        if self.cached_logo is not None:
            logo_h, logo_w = self.cached_logo.shape[:2]
            logo_x = (frame_width - logo_w) // 2
            logo_y = text_y + 50
            if self.cached_logo.shape[2] == 4:
                overlay_image_alpha(frame, self.cached_logo[:, :, :3], logo_x, logo_y, self.cached_logo[:, :, 3])
            else:
                frame[logo_y:logo_y+logo_h, logo_x:logo_x+logo_w] = self.cached_logo

        return frame
