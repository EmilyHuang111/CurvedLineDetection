# Curved Line Detection with OpenCV

This project uses OpenCV to detect lines in images or video streams and visualize their locations, focusing on center-line detection through edge detection and Hough Transform. The program captures live video frames from the default camera, processes each frame to identify lines, and displays the results with additional graphical elements.

## Features
- **Grayscale and Blur Filters**: Converts images to grayscale and applies Gaussian and median blurs to reduce noise.
- **Canny Edge Detection**: Detects edges within specified regions of interest.
- **Hough Transform**: Detects lines in the masked edge-detected image.
- **Distance Filtering**: Connects lines based on specified distance thresholds.
- **Real-time Video Processing**: Continuously captures and processes frames from the default camera in real-time.

## Prerequisites
- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Math

Install the dependencies with:
```bash
pip install opencv-python numpy
