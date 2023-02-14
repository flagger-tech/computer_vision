import cv2
import time

start_time = time.time()

# n minutes in seconds
n = 1
limit = n * 60

cap = cv2.VideoCapture(0)
count = 0
success = True
fps = int(cap.get(cv2.CAP_PROP_FPS))

if fps > 0:
    frame_interval = 3 * fps
else:
    frame_interval = 30  # default value

while success and time.time() - start_time < limit:
    success, image = cap.read()
    if not success:
        break
    if count % frame_interval == 0:
        cv2.imwrite(f'/Users/murilobarbosa/Desktop/wonk/demo/images/{count}.jpg', image)
        cv2.imshow("Frame", image)
    count += 1
