'''
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
'''
from time import sleep
from picamera import PiCamera

def open_preview():
    with PiCamera() as camera:
        camera.resolution = (600, 600)

        camera.start_preview()
        for i in range(100):
            sleep(0.6)
            camera.capture(str(i) + "ziran" + ".jpg", resize=(600, 600))

if __name__ == '__main__':
    open_preview()