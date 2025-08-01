# 🧠 Personal Stress Meter

A real-time stress monitoring application that uses computer vision to track eye movements and estimate stress levels based on Eye Aspect Ratio (EAR) analysis.

## Features

- **Real-time Eye Tracking**: Uses MediaPipe to detect facial landmarks and calculate Eye Aspect Ratio
- **Stress Level Estimation**: Converts EAR measurements into stress levels (0.0 = relaxed, 1.0 = high stress)
- **Live Video Feed**: Shows your webcam feed with real-time stress overlay
- **Data Logging**: Automatically logs stress data to CSV file for analysis
- **Interactive Web Interface**: Built with Streamlit for easy use

## How It Works

The application tracks your eye openness using the Eye Aspect Ratio (EAR) formula:
- **Higher EAR values** (wider eyes) = Lower stress levels
- **Lower EAR values** (squinting/tired eyes) = Higher stress levels

The stress meter responds to:
- Squinting or partially closed eyes (increases stress)
- Frequent blinking (fluctuating stress)
- Droopy eyelids from fatigue (increases stress)
- Wide, alert eyes (decreases stress)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Keysej/Personal-Stress-Meter.git
   cd Personal-Stress-Meter
   ```

2. **Install required packages**:
   ```bash
   pip install streamlit opencv-python mediapipe numpy
   ```

## Usage

1. **Run the application**:
   ```bash
   streamlit run stress_meter.py
   ```

2. **Open your browser** and go to `http://localhost:8501`

3. **Allow camera access** when prompted

4. **Monitor your stress levels** in real-time on the video feed

## Data Output

The app automatically creates a `stress_log.csv` file with:
- Timestamp
- Average EAR value
- Calculated stress level

## Requirements

- Python 3.7+
- Webcam
- Good lighting for accurate face detection

## Technologies Used

- **Streamlit**: Web interface
- **OpenCV**: Computer vision and video processing
- **MediaPipe**: Face mesh detection and landmark extraction
- **NumPy**: Numerical computations

## Contributing

Feel free to fork this repository and submit pull requests for improvements!

## License

This project is open source and available under the MIT License. 