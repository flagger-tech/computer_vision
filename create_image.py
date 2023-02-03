import os
import time
import cv2

# get all file with .mp4 prefix
folder = "/Users/murilobarbosa/Desktop/wonk/videos"
results = []
results += [each for each in os.listdir(f"{folder}") if each.endswith(".mp4")]

for i in results:
    start = time.time()
    cap = cv2.VideoCapture(f'{folder}/{i}')
    count = 0
    success = True
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    if fps > 0:
        frame_interval = 3 * fps
    else:
        frame_interval = 30  # default value

    while success:
        success, image = cap.read()
        if not success:
            break
        if count % frame_interval == 0:
            cv2.imwrite(f'/Users/murilobarbosa/Desktop/wonk/images/{i[:-11]}_{count}.jpg', image)
            # cv2.imshow("Frame", image)
        count += 1

    os.remove(f'{folder}/{i}')

    cap.release()
