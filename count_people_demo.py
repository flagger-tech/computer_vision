import os
import time
from datetime import date

import cv2
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load the environment variables from the .env file
load_dotenv()

# get data from .env
engine = os.getenv('engine')
weights = os.getenv('weight')
cfg = os.getenv('cfg')

engine = create_engine(engine)
conn = engine.connect()

today = date.today()
start = time.time()

# Load YOLO model
net = cv2.dnn.readNet(weights, cfg)

cap = cv2.VideoCapture(0)
count = 0
success = True
fps = int(cap.get(cv2.CAP_PROP_FPS))
n = 0.25
limit = n * 60  # n minutes in seconds

if fps > 0:
    frame_interval = 3 * fps
else:
    frame_interval = 30  # default value

results = []

while success and time.time() - start < limit:
    success, image = cap.read()
    if not success:
        break
    if count % frame_interval == 0:
        cv2.imwrite(f'/Users/murilobarbosa/Desktop/wonk/demo/images/01_01_01_{today}_{count}.jpg', image)
        results.append(f"01_01_01_{today}_{count}.jpg")
    count += 1

# Destroy all the windows
cap.release()
cv2.destroyAllWindows()

cities = ["Vila Nova de Famalicão"]
cities_id = [1]

# Loop through file paths
people_counted = []
comp_id = []
loc_id = []
cam_id = []
dates = []
company = []

# Loop through file paths
for file_path in results:
    # Define input image
    image = cv2.imread(f"/Users/murilobarbosa/Desktop/wonk/demo/images/{file_path}")

    # Get image dimensions
    (height, width) = image.shape[:2]

    # Define the neural network input
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Perform forward propagation
    output_layer_name = net.getUnconnectedOutLayersNames()
    output_layers = net.forward(output_layer_name)

    # Initialize list of detected people
    people = []

    # Loop over the output layers
    for output in output_layers:
        # Loop over the detections
        for detection in output:
            # Extract the class ID and confidence of the current detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Only keep detections with a high confidence
            if class_id == 0 and confidence > 0.60:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Add the detection to the list of people
                people.append((x, y, w, h))

    # Append results to lists
    people_counted.append(len(people) // 4)
    comp_id.append(file_path[:2])
    loc_id.append(file_path[6:8])
    cam_id.append(file_path[3:5])
    dates.append(f"{file_path[9:13]}-{file_path[14:16]}-{file_path[17:19]}")
    # os.remove(f"/Users/murilobarbosa/Desktop/wonk/demo/images/{file_path}")

for i in comp_id:
    company.append('1676546594620x486205763845292540' if int(i) == 1 else '1571517282871x719253102817289193')

location = [cities[cities_id.index(city_id)] if city_id in cities_id else '' for city_id in [int(i) for i in loc_id]]

data = pd.DataFrame({
    'camera_slug': list(set(cam_id)),
    'company': list(set(company)),
    'date': list(set(dates)),
    'impressions': sum(people_counted) / fps,
    'location': list(set(location))
})

data.set_index('camera_slug', inplace=True)

# Insert the dataframe into the table
data.to_sql(
    name='wonk',
    con=conn,
    if_exists='append',
    index=True
)

# Commit the changes and close the connection
conn.commit()
conn.close()
