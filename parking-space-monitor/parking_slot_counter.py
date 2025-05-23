import cv2
import pickle
import pandas as pd
from datetime import datetime

# Read the image instead of video
image_path = 'input/parking_image.jpg'
frame = cv2.imread(image_path)
if frame is None:
    raise FileNotFoundError(f"Image not found at {image_path}")

with open('park_positions', 'rb') as f:
    park_positions = pickle.load(f)

font = cv2.FONT_HERSHEY_COMPLEX_SMALL

# Parking space parameters
width, height = 40, 19
full = width * height
empty = 0.10  # Threshold for empty space detection

def parking_space_counter(img_processed):
    global counter, occupied_counter
    counter = 0  # Available spaces (green)
    occupied_counter = 0  # Occupied spaces (red)
    
    for position in park_positions:
        x, y = position
        img_crop = img_processed[y:y + height, x:x + width]
        count = cv2.countNonZero(img_crop)
        ratio = count / full
        
        # More precise detection
        if ratio < empty:
            color = (0, 255, 0)  # Green for empty
            counter += 1
        else:
            color = (0, 0, 255)  # Red for occupied
            occupied_counter += 1
            
        cv2.rectangle(overlay, position, (position[0] + width, position[1] + height), color, -1)
        cv2.putText(overlay, "{:.2f}".format(ratio), (x + 4, y + height - 4), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

# Process the image
overlay = frame.copy()
img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

parking_space_counter(img_thresh)

alpha = 0.7
frame_new = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

# Set total slots to 396 and calculate occupied and available
total_slots = 396  # Fixed total number of slots
occupied_slots = occupied_counter
available_slots = total_slots - occupied_slots

# Create Excel file with the counts
data = {
    'Category': ['Total Slots', 'Occupied Slots', 'Available Slots'],
    'Count': [total_slots, occupied_slots, available_slots]
}
df = pd.DataFrame(data)

# Add timestamp to filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
excel_filename = f'parking_counts_{timestamp}.xlsx'
df.to_excel(excel_filename, index=False)
print(f"Excel file created: {excel_filename}")

# Display the information
w, h = 400, 90
cv2.rectangle(frame_new, (0, 0), (w, h), (255, 0, 255), -1)
cv2.putText(frame_new, f"Total Slots: {total_slots}", (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(frame_new, f"Occupied (Red): {occupied_slots}", (10, 60), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(frame_new, f"Available: {available_slots}", (10, 90), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow('frame', frame_new)
cv2.waitKey(0)
cv2.destroyAllWindows()
