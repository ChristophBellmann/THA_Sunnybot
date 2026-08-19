import cv2
import numpy as np  # Make sure numpy is imported

class SpotCam:
    def __init__(self):
        self.overlay_text = ""

    def process_image(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)  # Threshold to get the bright areas
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours of the bright areas
        total_area = img.shape[0] * img.shape[1]  # Calculate the percentage of bright areas
        bright_area = sum(cv2.contourArea(c) for c in contours)
        bright_percentage = (bright_area / total_area) * 100

        location_text = "Location: "
        if contours:
            max_contour = max(contours, key=cv2.contourArea)  # Get the bounding box of the largest contour
            x, y, w, h = cv2.boundingRect(max_contour)
            center_x = x + w // 2
            normalized_center_x = (center_x / img.shape[1]) * 200 - 100

            if normalized_center_x < -20:
                location_text += "Left"
            elif normalized_center_x > 20:
                location_text += "Right"
            else:
                location_text += "Middle"

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw the bounding box on the image

            height_text = f'{h} px'
            width_text = f'{w} px'
            area_text = f'{w * h} px^2'
        else:
            location_text += "Not found"
            height_text = width_text = area_text = ''
            normalized_center_x = 0  # Default value if no bright area is found

        direction_text = f'{normalized_center_x:.2f}'

        self.overlay_text = (
            f'Brightness: {bright_percentage:.2f}%\n'
            f'{location_text}\n'
            f'Height: {height_text}\n'
            f'Width: {width_text}\n'
            f'Area: {area_text}\n'
            f'Direction: {direction_text}'
        )

        return bright_percentage, location_text, height_text, width_text, area_text, direction_text, normalized_center_x

    def get_overlay_text(self):
        return self.overlay_text
