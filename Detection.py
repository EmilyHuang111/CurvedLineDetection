import cv2 as cv #import necessary libraries for image processing
import numpy as np
import math #import the math library necessary for the center line detection

def detect_lines(image):
    #https://www.geeksforgeeks.org/python-opencv-cv2-cvtcolor-method/ example 2 line 5
    # Convert the input image to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    #https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html example 2 line 24
    # Apply Gaussian blur to the grayscale image
    gray_blur = cv.GaussianBlur(gray, (15, 15), 0)

    # https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html example 3 line 25
    # Apply median blur to further reduce noise
    median_blur = cv.medianBlur(gray_blur, 5)

    #https://docs.opencv.org/3.4/d7/de1/tutorial_js_canny.html example 1 line 5
    # Apply Canny edge detection to detect edges in the image
    canny_image = cv.Canny(median_blur, 100, 20)

    #https://www.geeksforgeeks.org/numpy-zeros-python/ example 1 line 1
    # Create a mask for the region of interest (ROI)
    roi = np.zeros(image.shape[:2], dtype="uint8")

    #https://www.geeksforgeeks.org/python-opencv-cv2-rectangle-method/ example 1 line 9
    # Define a rectangle for the ROI
    cv.rectangle(roi, (400, 400), (950, 950), 1, -1)

    #https://medium.com/featurepreneur/performing-bitwise-operations-on-images-using-opencv-6fd5c3cd72a7 example 1 line 6
    # Apply the mask to the Canny edge-detected image
    mask = cv.bitwise_and(canny_image, canny_image, mask=roi)

    # Draw a rectangle on the original image to visualize the ROI
    cv.rectangle(image, (400, 400), (950, 950), (255, 0, 255), 5)

    #https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html example 2 line 12
    # Apply Hough Transform to detect lines in the masked image
    lines = cv.HoughLinesP(mask, 1, np.pi / 180, threshold=10, minLineLength=10, maxLineGap=15)

    #https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/ examples 2 and 3 line 17
    # Check if any lines were detected
    if lines is not None:
        # Initialize lists to store line endpoints and slopes
        lines_list = []
        slopes = []
        # Iterate over each detected line
        for line in lines:
            # Extract coordinates of the endpoints
            x1, y1, x2, y2 = line[0]
            # Add line endpoints to the list
            lines_list.append(line[0])
            # Draw the line on the image
            cv.line(image, (x1, y1), (x2, y2), (0, 255, 0), 15)  # Green color, 15 pixels thick
            # Calculate the slope of the line (avoiding division by zero)
            slope = 0
            if x2 - x1 != 0:
                slope = (y2 - y1) / (x2 - x1)
            # Add the slope to the list of slopes
            slopes.append(slope)
            
        # https://www.w3resource.com/python-exercises/python-basic-exercise-73.php example 1 line 1    
        # https://datascience.stackexchange.com/questions/77256/how-to-find-slope-of-curve-at-certain-points example 2 line 7
        # https://docs.opencv.org/3.4/dc/da5/tutorial_py_drawing_functions.html example 1 line 5
        # Loop over each pair of slopes
        for i in range(len(slopes)):
            for j in range(len(slopes)):
                # Extract coordinates of endpoints for both lines
                x1, y1, x2, y2 = lines_list[i]
                x3, y3, x4, y4 = lines_list[j]
                # Calculate slopes of both lines, adding a small value to avoid division by zero
                slope1 = (y2 - y1) / (x2 - x1 + 0.00001)
                slope2 = (y4 - y3) / (x4 - x3 + 0.00001)
                # Calculate average slope between the two lines
                slope = 0.5 * (slope1 + slope2)
                # Calculate distance between the lines
                dist = abs(y1 - y3 - slope * (x1 - x3)) / math.sqrt(slope * slope + 1)
                # Check if the distance is greater than a threshold
                if dist > 230 and dist < 270:
                    # Draw a line connecting the midpoints of the two lines on the image
                    cv.line(image, ((x1 + x3) // 2, (y1 + y3) // 2), ((x2 + x4) // 2, (y2 + y4) // 2), (0, 0, 255),
                            15)  # Red color, 15 pixels thick
