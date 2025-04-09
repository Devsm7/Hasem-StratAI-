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
  - Player movements
  - Team performance metrics
- **Real-time Processing:** Uses **computer vision** to deliver instant insights with minimal delay.
- **AI-powered Detection:** Utilizes deep learning models for accurate event recognition.

## Technologies Used

- **Computer Vision** (for event detection and analysis)
- **Deep Learning Models** (for player, ball, and referee recognition)
- **YOLOv8** (for object detection)
- **NumPy & Pandas** (for data processing)
- **Python** (for AI model development and integration)

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

## Contribution

Contributions are welcome! Feel free to fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the **MIT License**. See `LICENSE` for details.

## Contact

For any inquiries or support, contact: [[your-email@example.com](mailto\:your-email@example.com)]

