
# Gesture-Controlled 2D Fighting Game with Nemesis AI

This is a **2D fighting game** built using **Python**, **Raylib**, **OpenCV**, and **MediaPipe**.  
It combines **gesture-based controls** with a **custom Nemesis AI system** that adapts to your playstyle, making every match dynamic and challenging.

---

## 🎮 Features

### **1. Adaptive Nemesis AI**
Inspired by the **Nemesis System** (*Shadow of Mordor*), but redesigned for a 2D fighting game.

#### **How It Works:**
1. **Action Logging**: Every move you perform (punch, kick, block, jump, crouch, movement) is **logged with timestamps** into a file.
2. **Pattern Analysis**: The system looks at your **last 100 actions** and identifies which move you use most often (e.g., punch spam).
3. **Counter-Strategy Update**: The CPU dynamically **increases the probability** of countering your most used actions. For example:
   - If you throw many punches → CPU will block more and use counter-kicks.
   - If you rely on kicks → CPU adjusts to block low and punch more.
4. **Continuous Learning**: This analysis runs **every 10 seconds** during gameplay and at the end of each round, making the CPU **progressively smarter**.

This approach creates a **reactive and evolving CPU opponent** without requiring heavy machine learning models.

---

### **2. Gesture-Based Controls with OpenCV + MediaPipe**
Ditch the keyboard — **your body becomes the controller**.

#### **How It Works:**
- **Webcam Capture**: OpenCV continuously captures frames from your webcam.
- **Pose Estimation**: MediaPipe detects key body points like **nose, wrists, knees**.
- **Hand Tracking**: MediaPipe Hands identifies **fingers and hand openness**.
- **Smoothed Detection**: To prevent false triggers, a **buffer (deque)** stores recent positions and calculates movement speed.

#### **Gesture Mapping:**
- **Punch**: Fast horizontal movement of wrists.
- **Kick**: Quick vertical movement of knees.
- **Block**: Wrists brought close together.
- **Jump/Crouch**: Nose position crossing threshold lines relative to a neutral stance.
- **Move Left/Right**: Open hand detected on respective sides of the frame.

#### **Why It’s Effective:**
- **Low-latency tracking** using MediaPipe’s efficient ML models.
- **Smoothed actions** reduce noise and unintentional moves.
- **Natural gameplay**: Movements feel intuitive and immersive.

---

## 🖥 Game Mechanics
- 3-round match system.
- **Combo counter**, **particle effects**, **screen shake** for impactful hits.
- **Health regeneration** for CPU when idle.
- **Dynamic animations** for various states (idle, jump, crouch, attack).
- **Sound effects** and **background music** for full immersion.

---

## 📚 Requirements
- Python 3.8+
- [RaylibPy](https://github.com/overdev/raylib-py)
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://developers.google.com/mediapipe)
- Numpy

Install dependencies:
```bash
pip install raylib-py opencv-python mediapipe numpy
```

---

## ▶️ Running the Game
1. Clone this repository:
```bash
git clone https://github.com/yourusername/gesture-fighter.git
cd gesture-fighter
```
2. Run the game:
```bash
python game2.py
```
Make sure your **webcam** is connected for gesture tracking.

---

## 🔮 Future Improvements
- **Calibration phase** for gesture detection (adjust thresholds per player).
- **Advanced AI** using Markov chains or reinforcement learning.
- **Multiplayer mode**.
- **Special gesture-triggered super moves**.
- **Enhanced graphics and UI**.

---

## 🛠 Credits
Developed through **research, experimentation, and creative problem-solving**.  
All Nemesis logic, gesture integration, and gameplay mechanics are custom-built by analyzing multiple approaches and molding them into a unique design.

---

## 📜 License
MIT License – Free to use and modify.

