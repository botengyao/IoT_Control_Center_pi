import cv2
import sys

# Get user supplied values
#imagePath = '/home/pi/IoT_Control_Center_pi/training-data/image4.jpg'
imagePath = '/home/pi/IoT_Control_Center_pi/training-data/DSC02292.JPG'
cascPath = "/home/pi/IoT_Control_Center_pi/training-data/haarcascade_frontalface_default.xml"

# For each person, one face id
face_id = 1

# Initialize sample face image
count = 0

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(100, 100),
    #flags = cv2.cv.CV_HAAR_SCALE_IMAGE
)
print("Found {0} faces!".format(len(faces)))
print(faces)
# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Increment sample face image
    count += 1
        # Save the captured image into the datasets folder
    cv2.imwrite(str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        # Display the video frame, with bounded rectangle on the person's face
    #cv2.imshow('frame', image)

#cv2.imshow("Faces found", image)
cv2.waitKey(0)
