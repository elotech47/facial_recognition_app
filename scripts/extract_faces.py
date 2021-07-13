from imutils import paths
import face_recognition
import pickle
import cv2
import os

def extract_faces():
    imagePaths = list(paths.list_images("../student_images"))
    knownEncodings = []
    knownNames = []

    #print(imagePaths)
    # loop over the image path
    for (i, imagePath) in enumerate(imagePaths):
        #print(imagePath)
        name = imagePath.split(os.path.sep)[-2]
        print(name)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #USe face_recognition to locate faces
        boxes = face_recognition.face_locations(rgb,model='hog')
        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)
        # loop over the encodings
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
    #save emcodings along with their names in dictionary data
    data = {"encodings": knownEncodings, "names": knownNames}
    #use pickle to save data into a file for later use
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data))
    f.close()