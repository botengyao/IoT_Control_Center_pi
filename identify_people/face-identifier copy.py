import cv2
import sys
import numpy as np

# Get user supplied values
imagePath = '/home/pi/IoT_Control_Center_pi/identify_people/Test/test8.png'
cascPath = "/home/pi/IoT_Control_Center_pi/training-data/haarcascade_frontalface_default.xml"

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/IoT_Control_Center_pi/identify_people/trainner.yml')
#font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
# For each person, one face id
#face_id = 5

# Initialize sample face image
Id = 0

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=3,
    minSize=(60, 60),
    #flags = cv2.cv.CV_HAAR_SCALE_IMAGE
)
print("Found {0} faces!".format(len(faces)))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Increment sample face image
    Id, conf=recognizer.predict(gray[y:y+h,x:x+w])
    print(conf)
    print(Id)
    if(Id==4 and conf < 80):
         Id = "Ziran"
    elif(Id==5 and conf < 80):
         Id =  "Boteng"
    else:
         Id = "No permission"
    print(Id)
    cv2.putText(image, str(Id), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
    print(Id, conf)

        # Display the video frame, with bounded rectangle on the person's face
    cv2.imshow('frame', image)

#cv2.imshow("Faces found", image)
cv2.waitKey(0)


