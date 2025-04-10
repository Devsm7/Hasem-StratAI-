# Hasem

## Overview

Hasem is an advanced AI-powered platform that leverages **Computer Vision** technology to detect key match events and analyze game statistics. It provides real-time insights into football matches by identifying events such as **goals, penalties, and fouls**, while also computing crucial metrics like **ball possession** and player performance.

## Features

- **Event Detection:** Automatically detects key match events, including:
  - Goals
  - Penalties
  - Fouls
- **Match Analysis:** Tracks and analyzes key statistics such as:
  - Ball possession
  - shots
  - passes
- **Real-time Processing:** Uses **computer vision** to deliver instant insights with minimal delay.
- **AI-powered Detection:** Utilizes deep learning models for accurate event recognition.

## Technologies Used

- **Computer Vision** (for event detection and analysis)
- **Deep Learning Models** (for player, ball, and referee recognition)
- **YOLOv8** (for object detection)
- Supervision (for detection processing and annotations)
- OpenCV (for image and video processing)
- PyTorch (for deep learning model training and inference)
- **NumPy & Pandas** (for data processing)
- **Python** (for AI model development and integration)
- Jupyter Notebook (for experimentation and model training)

## Installation

To set up the Hasem platform on your local machine:

```bash
# Clone the repository
git clone https://github.com/your-username/Hasem.git
cd Hasem

# Install required dependencies
pip install -r requirements.txt
```

## Usage

1. Place the match video in the **input/videos/** directory.
2. Run the main script to start event detection:
   ```bash
   python main.py --video input/videos/match.mp4
   ```
3. The system will process the video and generate:
   - Detected match events
   - Statistical insights (e.g., ball possession, team performance)


## External pre-trained model used
-Detecting the players , Ball , refrees:
https://universe.roboflow.com/roboflow-jvuqo/football-players-detection-3zvbc

-Detecting the Goalpost:
https://universe.roboflow.com/yolo-b6voi/goalpost-u6e0h


## Demos

<img src="لقطة شاشة 2025-04-09 145519.png" width="500">

<video width="500" controls>
  <source src="video.mp4" type="video/mp4">
</video>
## Contact

For any inquiries or support, contact: [a7mad24680@gmail.com]

