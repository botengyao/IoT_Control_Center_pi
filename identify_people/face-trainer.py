import cv2,os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create(neighbors=10)
detector= cv2.CascadeClassifier("/home/pi/IoT_Control_Center_pi/training-data/haarcascade_frontalface_default.xml");

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #create empth face list
    faceSamples=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        print(imagePath)
        Id=int(os.path.split(imagePath)[-1].split(".")[0])
        print(Id)
        # extract the face from the training image sample
        faces=detector.detectMultiScale(imageNp)

        #If a face is there then append that in the list as well as Id of it
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    return faceSamples,Ids


faces,Ids = getImagesAndLabels('/home/pi/IoT_Control_Center_pi/identify_people/DataSet')
recognizer.train(faces, np.array(Ids))
recognizer.write('/home/pi/IoT_Control_Center_pi/identify_people/trainner.yml')
