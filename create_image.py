import os
import cv2

# get all file with .mp4 prefix
folder = "/Users/murilobarbosa/Desktop/wonk/videos"
results = []
results += [each for each in os.listdir(f"{folder}") if each.endswith(".mp4")]

# for loop that capture and save each 3s of video
for i in results:
    # read video
    cap = cv2.VideoCapture(f'{folder}/{i}')
    count = 0
    success = True
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # define the interval in seconds
    if fps > 0:
        frame_interval = 3 * fps
    else:
        frame_interval = 30  # default value

    # create images from video
    while success:
        success, image = cap.read()
        if not success:
            break
        if count % frame_interval == 0:
            cv2.imwrite(f'/Users/murilobarbosa/Desktop/wonk/images/{i[:-11]}_{count}.jpg', image)
        count += 1

    # delete all videos in this folder
    os.remove(f'{folder}/{i}')
    cap.release()
