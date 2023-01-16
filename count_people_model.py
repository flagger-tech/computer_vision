import datetime
import cv2
import imutils

width = 800
text_in = 0
text_out = 0


def test_intersection_in(x, y):
    res = -450 * x + 400 * y + 157500
    if -550 <= res < 550:
        print(str(res))
        return True
    return False


def test_intersection_out(x, y):
    res = -450 * x + 400 * y + 180000
    if -550 <= res <= 550:
        print(str(res))
        return True
    return False


camera = cv2.VideoCapture("test1.mov")
# camera = cv2.VideoCapture(0)

firstFrame = None

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied text
    grabbed, frame = camera.read()
    text = "Unoccupied"

    # if the frame could not be grabbed, then we have reached the end of the video
    if not grabbed:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=width)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours in the image
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 12000:
            continue
        # compute the bounding box for the contour, draw it on the frame, and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.line(frame, (width // 2, 0), (width, 450), (250, 0, 1), 2)  # blue line
        cv2.line(frame, (width // 2 - 50, 0), (width - 50, 450), (0, 0, 255), 2)  # red line

        rectagle_center_point = ((x + x + w) // 2, (y + y + h) // 2)
        cv2.circle(frame, rectagle_center_point, 1, (0, 0, 255), 5)

        if test_intersection_in((x + x + w) // 2, (y + y + h) // 2):
            text_in += 1

        if test_intersection_out((x + x + w) // 2, (y + y + h) // 2):
            text_out += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.putText(frame, "In: {}".format(str(text_in)), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Out: {}".format(str(text_out)), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)

# cleanup the camera and close any open windows
camera.release()
# cv2.destroyAllWindows()
