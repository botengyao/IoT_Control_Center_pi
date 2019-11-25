import cv2
import sys
import numpy as np
from time import sleep
from picamera import PiCamera
import io
from picamera.array import PiRGBArray
import mqtt-sub

#print("Found {0} faces!".format(len(faces)))
def fact_detection():   
    global recognizer
    cascPath = "/home/pi/IoT_Control_Center_pi/training-data/haarcascade_frontalface_default.xml"
    #recognizer = cv2.face.LBPHFaceRecognizer_create()
    #recognizer.read('/home/pi/IoT_Control_Center_pi/identify_people/trainner.yml')
    # Initialize sample face image
    Id = 0
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    total_ziran = 0
    with PiCamera() as camera:
        camera.resolution = (608, 608)
        rawCapture = PiRGBArray(camera, size=( 608, 608 ) )
        #stream = io.BytesIO()
        for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):
            image = frame.array    
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        # Detect the face in the image
            faces = faceCascade.detectMultiScale(gray)
            print("Found {0} faces!".format(len(faces)))
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                Id, conf=recognizer.predict(gray[y:y+h,x:x+w])
                if(Id==4 and conf < 75):
                    Id = "Ziran"
                elif(Id==5 and conf < 75):
                    Id =  "Boteng"
                else:
                    Id = "No permission"
                print(Id)
                cv2.putText(image, str(Id), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
                print(Id, conf)
            if Id == "Ziran" or Id == "Boteng":
                return True
            else:
                rawCapture.truncate( 0 )
                print("waiting for open")
            #sleep(1)

def start_face_detection():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('/home/pi/IoT_Control_Center_pi/identify_people/trainner.yml')
    while True:     
        if fact_detection():
            print("Success!")
            a = input("Please input continue")
        if a == "q":
            break






