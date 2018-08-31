from PIL import Image
import face_recognition
import numpy as np
import cv2 as cv
import json
import sys

#####################
# PRIMARY ALGORITHM #
#####################

#calibrate face box enlargement after detection
#(the original face coverage is often too small to create a 3d model)
TOP_SCALER = 0.56
SIDES_SCALER = 0.33

# Load the jpg file into a numpy array
image = face_recognition.load_image_file("/src/rawimage.jpg")

# Find all the faces in the image using a pre-trained convolutional neural network.
# This method is more accurate than the default HOG model, but it's slower
face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

print("found {} face(s) in this photograph.".format(len(face_locations)))

#these arrays facilitate the construction of imagemagick commands for cropping each face
face_values_cnn = []
crop_commands_cnn = [] 

for i in range(len(face_locations)):
    x = face_locations[i][3]
    y = face_locations[i][0]
    w = face_locations[i][1]-face_locations[i][3]
    h = face_locations[i][2]-face_locations[i][0]

    #add face x, y, width, and height to face_values_cnn
    face_values_cnn.append([x-int(w*SIDES_SCALER), y-int(h*TOP_SCALER), w+2*int(w*SIDES_SCALER), h+int(h*SIDES_SCALER)+int(h*TOP_SCALER)])

#create list of imagemagick commands to crop each face
for i in face_values_cnn:
    command = 'convert /data/rawimage.jpg -crop ' + str(i[2])+'x'+str(i[3])+'+'+str(i[0])+'+'+str(i[1])+" /tmp/cropped_face.jpg"
    crop_commands_cnn.append(command)


#########################
# ALTERNATIVE ALGORITHM #
#########################

#calibrate face box enlargement after detection
TOP_SCALER = 0.56
SIDES_SCALER = 0.28

#these arrays facilitate the construction of imagemagick commands for cropping each face
face_values_cv = []
crop_commands_cv = [] 

#opencv standard face classifiers
face_cascade = cv.CascadeClassifier('root/facedetection/argo-ml-demo/opencv_classifiers/haarcascade_frontalface_alt.xml')
eye_cascade = cv.CascadeClassifier('root/facedetection/argo-ml-demo/opencv_classifiers/haarcascade_eye.xml')

img = cv.imread('src/rawimage.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for i in range(len(faces)):

    x = faces[i, 0]
    y = faces[i, 1]
    w = faces[i, 2]
    h = faces[i, 3]

    #add face x, y, width, and height to face_values
    face_values_cv.append([x-int(w*SIDES_SCALER), y-int(h*TOP_SCALER), w+2*int(w*SIDES_SCALER), h+int(h*SIDES_SCALER)+int(h*TOP_SCALER)])

#create list of imagemagick commands to crop each face
for i in face_values_cv:
    command = 'convert /data/rawimage.jpg -crop ' + str(i[2])+'x'+str(i[3])+'+'+str(i[0])+'+'+str(i[1])+" /tmp/cropped_face.jpg"
    crop_commands_cv.append(command)


#dump the imagemagick commands corresponding to the algorithm that detected the most faces
if len(face_values_cv)>len(face_values_cnn):
    with open('/src/imagemagick_commands.json', 'w') as outfile:
        json.dump([i for i in crop_commands_cv], outfile)
else:
    with open('/src/imagemagick_commands.json', 'w') as outfile:
        json.dump([i for i in crop_commands_cnn], outfile)
