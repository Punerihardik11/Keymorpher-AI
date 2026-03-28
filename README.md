# Keymorpher AI  
### Gesture-Based Virtual Keyboard with Intelligent UI & Data Capture

---

## 📌 Overview

**Keymorpher AI** is a gesture-based virtual keyboard system that enables users to interact with a computer using hand and finger movements captured through a webcam.

The system leverages real-time computer vision to detect hands, track finger positions, and convert hover gestures into key inputs. It extends beyond typing by implementing a structured multi-step input flow and local data persistence.

This project demonstrates the integration of **computer vision, UI design, state management, and backend storage** into a cohesive interactive system.

---

## ✨ Features

### 🖐️ Gesture-Based Interaction
- Real-time hand detection using MediaPipe
- Finger tracking for precise interaction
- Hover-based key selection with delay control

### ⌨️ Virtual Keyboard UI
- Fully responsive layout (resolution-independent)
- Modern, minimal UI design
- Dynamic scaling across devices
- Special keys: ENTER, BACK, SPACE, CLEAR

### 🧠 Intelligent Input Flow
- Multi-step form system:
  - Enter Name
  - Enter Roll Number
  - Select Branch (BBA / BSC / BCOM)
- State-driven architecture
- Smooth transitions between steps

### 🎨 Enhanced User Experience
- Splash screen with branding
- Sound effects:
  - Intro sound
  - Key press feedback
- Clean overlay UI with dimmed camera background

### 💾 Data Persistence
- Lightweight database using SQLite
- Stores:
  - Name
  - Roll Number
  - Branch
- Safe insert logic (no duplicates)

### ⚙️ Robust Architecture
- Modular code structure
- Separation of concerns:
  - UI rendering
  - gesture detection
  - state management
  - database handling
  - sound system

---

## 🏗️ Project Structure
Keymorpher-AI/
│
├── src/
│ ├── main.py
│ ├── hand_detection.py
│ ├── gesture_controller.py
│ ├── keyboard_display.py
│ ├── typed_text.py
│ ├── database.py
│ └── sound_manager.py
│
├── assets/
│ ├── keyboard-symbol.png
│ ├── keymorpher-name.png
│ ├── intro.wav
│ └── click.wav
│
├── docs/
│ └── diagrams/
│
├── requirements.txt
├── README.md
└── .gitignore


---

## 🛠️ Technology Stack

- **Language:** Python  
- **Computer Vision:** OpenCV  
- **Hand Tracking:** MediaPipe  
- **Database:** SQLite  
- **Audio:** Pygame  
- **Numerical Processing:** NumPy  

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/Punerihardik11/Keymorpher-AI.git

cd Keymorpher-AI

pip install -r requirements.txt

python src/main.py

🧪 System Workflow
Splash screen with intro sound
Gesture-based typing interface loads
User inputs:
Name
Roll Number
User selects branch using hover interaction
Data is stored in SQLite database
Thank you screen is displayed
System resets automatically for next user

🧠 System Design (OOSE)

The project follows Object-Oriented Software Engineering (OOSE) principles:

Entity Objects: User data
Interface Objects: UI components (keyboard, input box, header)
Control Objects: Gesture controller, system state manager

📊 Diagrams Included:
Use Case Diagram
Class Diagram
OOSE Analysis Model


🎯 Key Highlights
Resolution-independent UI system
Gesture-driven interaction model
State machine-based workflow
Real-time performance with smooth rendering
Modular and scalable architecture

👨‍💻 Authors
Hardik Waghmare — Roll No: 145
Parth K Kamble — Roll No: 58
Bhumika Phutane — Roll No: 106

Final Year BSc Computer Science Project

📌 Future Scope
Touchless system for accessibility applications
Integration with external applications (text input APIs)
Mobile device compatibility
Advanced gesture recognition (multi-finger commands)