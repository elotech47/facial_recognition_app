""" REGISTER STUDENT """
import time
import csv
import datetime
import os
import cv2
import face_recognition


def get_student_details(name, department,face_id, phone):
    print("Getting Student Images ..... ")
    time.sleep(2)
    ts = time.time()
    Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    row = [face_id,department, name, Date, Time, phone]
    heading = ["Id","Department", "name", "Date", "Time","Phone"]
    
    if os.path.isfile('../StudentDetails/StudentDetails.csv'):
        with open('../StudentDetails/StudentDetails.csv', 'a+', newline = "") as csvFile:
            writer = csv.writer(csvFile)#, delimiter=',')
            #writer.writerow([i for i in heading])
            writer.writerows([row])#FFFFFF#FFFFFF
            csvFile.close()
    else:
        with open('../StudentDetails/StudentDetails.csv', 'w+', newline = "") as csvFile:
            writer = csv.writer(csvFile)#, delimiter=',')
            writer.writerow([i for i in heading])
            writer.writerows([row])#FFFFFF#FFFFFF
            csvFile.close()

    get_student_images(name, face_id=face_id, department=department)
    
def get_student_images(name, face_id, department):            
    print("Look at the camera ..............") 

    # Get a reference to webcam 
    video_capture = cv2.VideoCapture(0)

    # Initialize variables
    face_locations = []

    count = 0
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        frame = cv2.resize(frame, (0,0),fx = 0.8, fy=0.8)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        print(face_locations)
        # Display the results
    ##top, right, bottom, left
    #x,y,w,h
    #(left, top), (right, bottom)
        for top, right, bottom, left in face_locations:   
            # Draw a box around the face
            cv2.rectangle(frame, (left,top),(right,bottom), (0, 0, 255), 2)
            #img_frame = frame[x:x+w,y:y+h]
            img_frame = frame[top:bottom, left:right]
            cv2.imshow('Video', img_frame)
            #Save the capture image into the datasets folder
            image_path = os.path.join("../student_images", department)
            #print(image_path)
            if not os.path.exists(image_path):
                os.makedirs(image_path)
                image_path = os.path.join(image_path, name)
                os.makedirs(image_path)
                cv2.imwrite(image_path + "/" + name + "_" + face_id + '_' + str(count) + ".jpg", img_frame)
            else:
                image_path = os.path.join(image_path, name)
                #os.makedirs(image_path)
                cv2.imwrite(image_path + "/" + name + "_" + face_id + '_' + str(count) + ".jpg", img_frame)
            print(count)
            count += 1

            # Display the resulting image
            cv2.putText(frame, str(count), (top+left,bottom), 20, 1, (255,255,255), 4)
            #cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif count >= 10: # Take 50 `face sample and stop video
            break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()



name = input("Name: ")
department = input("Department: ")
face_id = input("S/N: ")
phone = input("Phone Number: ")

get_student_details(name, department, face_id, phone)