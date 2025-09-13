import os
import json
import pandas as pd
from PIL import Image

# Paths to your data
frames_dir = 'frames7'
positions_dir = '../positions'

# Create lists to hold the data
data = []

# Collect all available steps
frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
for frame_file in frame_files:
    step_id = frame_file.split('_')[1].split('.')[0]  # Extract "00001" from "frame_00001.png"
    pos_file = f"step_{step_id}.json"
    
    frame_path = os.path.join(frames_dir, frame_file)
    pos_path = os.path.join(positions_dir, pos_file)

    if not os.path.exists(pos_path):
        continue  # skip if position file is missing

    # Load positions
    with open(pos_path, 'r') as f:
        pos_data = json.load(f)
    
    
    # Assume 2 herders and 5 targets
    if len(pos_data["herders"]) < 2 or len(pos_data["targets"]) < 5:
        continue  # skip if not enough agents

    row = {
        "image_path": frame_path
    }

    # Add herder positionsa
    # Add normalized herder positions
    for i in range(2):
        x = pos_data["herders"][i][0]
        y = pos_data["herders"][i][1]
        row[f"herder{i+1}_x"] = (x + 30) / 60
        row[f"herder{i+1}_y"] = (y + 30) / 60

    # Add normalized target positions
    for i in range(5):
        x = pos_data["targets"][i][0]
        y = pos_data["targets"][i][1]
        row[f"target{i+1}_x"] = (x + 30) / 60
        row[f"target{i+1}_y"] = (y + 30) / 60


    data.append(row)

# Convert to DataFrame and save
df = pd.DataFrame(data)
df.to_csv("herder_target_dataset7.csv", index=False)
print(f"Dataset saved with {len(df)} samples.")
