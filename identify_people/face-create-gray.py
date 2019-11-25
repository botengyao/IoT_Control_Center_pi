import cv2
import sys
import os

# Get user supplied values
cascPath = "/home/pi/IoT_Control_Center_pi/training-data/haarcascade_frontalface_default.xml"

# For each person, one face id
face_id = 3
# Initialize sample face image
count = 0

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)
#------STEP-1--------
#get the directories (one directory for each subject) in data folder
data_folder_path = "/home/pi/IoT_Control_Center_pi/identify_people/training-data"
dirs = os.listdir(data_folder_path)
print(dirs)
 
#let's go through each directory and read images within it
for dir_name in dirs:
#our subject directories start with letter 's' so
#ignore any non-relevant directories if any
   if not dir_name.startswith("s"):
      continue;
 
#------STEP-2--------
#extract label number of subject from dir_name
#format of dir name = slabel
#, so removing letter 's' from dir_name will give us label
   label = int(dir_name.replace("s", ""))
 
#build path of directory containing images for current subject subject
#sample subject_dir_path = "training-data/s1"
   subject_dir_path = data_folder_path + "/" + dir_name
   print(subject_dir_path)
#get the images names that are inside the given subject directory
   subject_images_names = os.listdir(subject_dir_path)
   face_id = face_id+1
 
#------STEP-3--------
#go through each image name, read image, 
#detect face and add face to list of faces
   for image_name in subject_images_names:
 
#ignore system files like .DS_Store
      if image_name.startswith("."):
         continue;
 
#build image path
#sample image path = training-data/s1/1.pgm
      image_path = subject_dir_path + "/" + image_name
      print(image_path)
#read image
      image = cv2.imread(image_path)
    
#display an image window to show the image 
      #cv2.imshow("Training on image...", image)
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
      faces = faceCascade.detectMultiScale( 
      gray, 
      scaleFactor=1.1, 
      minNeighbors=4, 
      minSize=(30, 30), 
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
         cv2.destroyAllWindows()
   count = 1
