# parking-space-monitor-opencv

 **Parking Slot Detection**

## Project Structure

├── input/                          # Folder containing parking image
│   └── parking_image.jpg
|
├── park_positions                  # Saved parking slot coordinates (Pickle file)
|
├── parking_counts_YYYYMMDD_HHMMSS.xlsx  # Auto-generated Excel report
|
├── parking_slot_counter.py         # Counts and displays slot status
|
├── parking_slot_picker.py          # Tool to mark parking slots

## 🔧 How It Works

1. **Mark Slots**

python parking_slot_picker.py

- Left-click and drag to mark a line of parking slots.
- Right-click on a slot to remove it.
- All slot positions are saved automatically in `park_positions`.

2. **Count Slots**

python parking_slot_counter.py

- Displays the parking lot with color-coded slots:
  - 🟩 Green: Available
  - 🟥 Red: Occupied
- Saves the slot status results to an Excel file with a timestamp.


## ✅ Requirements

Install required packages with:

pip install opencv-python pandas openpyxl

