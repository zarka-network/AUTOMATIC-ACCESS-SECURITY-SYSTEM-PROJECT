import cv2
import numpy as np
import face_recognition
import os
import time
import ftplib
import pyaudio
import wave
import pyttsx3
import pyfirmata
from pyfirmata import Arduino, SERVO, INPUT, util

# Describe the settings of the electronic components related to Arduino board
ard_port = pyfirmata.Arduino('COM3')
Button = ard_port.digital[8]
Servo_motor = ard_port.digital[10]
Led1 = ard_port.digital[7]
Led2 = ard_port.digital[6]
iter = pyfirmata.util.Iterator(ard_port)
iter.start()
Button.mode = pyfirmata.INPUT
Servo_motor.mode = pyfirmata.SERVO

# set the servo motor in the initial satate (closed door)
for i in range (0, 110) :
    Servo_motor.write(i)

# set the path of the directory who contain the pictures
dir_path = "C:\\Users\\who_I_am\\Desktop\\Face_recognation_project\\users_pictures\\"
# make a list to stock the pictures on it 
images = []
# make a list to stock the names of the pictures on it
Names = []
# stock the path of each picture who exist under users_pictures directory in personList variable
personsList = os.listdir(dir_path)

# for loop to make itteration over all the pictures inside users_pictures directory
for pic in personsList:
    # read and save the pictures in r_picture
    r_picture = cv2.imread(f'{dir_path}/{pic}')
    # append the saved pictures in r_picture variable in images list
    images.append(r_picture)
    # name of the picture is taken with the extension too, we want just the name without extension ==> use os.path.splitext() to remove it
    # save the names under Names list without extensions
    Names.append(os.path.splitext(pic)[0])

# create a function to make encoding of the pictures under users_pictures by using face_recognation
# to describe the coordinations of the faces in the pictures

def getEncodings(image):
    # create a list to save the pictures encodings
    encodeList = []
    # make an iterration over the pictures stared in the images list
    for img in images:
        # read the pictures and convert them from BGR to RGB
        # face_recognation necessite RGB pictures
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# save all the pictures encodings in a variable
encodeListKnown = getEncodings(images)

# set the camera
cam = cv2.VideoCapture(0)
start_t = int(40)
for t in range (start_t, 0, -1):
    rep, img = cam.read()
    # Resize the frames taken from the video
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    # convert the color of the captured farmes from BGR to RGB
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    # make encoding to the captured frame from the video 
    faceCurentFrame = face_recognition.face_locations(imgS)
    encodeCurentFrame = face_recognition.face_encodings(imgS, faceCurentFrame)

    for encodeface, faceLoc in zip(encodeCurentFrame, faceCurentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeface)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeface)
        # the lower value define the right picture by using numpy library
        matchIndex = np.argmin(faceDis)
        # in this bloc we set the name and the rectangle of the over the face of the user
        if matches[matchIndex]:
            name = Names[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)
            cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,0,255), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            cv2.imshow('Face_recognition', img)
            cv2.waitKey(1)
         # THis statement will be executed in case if the user is not defineded in the local data base   
        else :
            name = "INCONNU".upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)
            cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,0,255), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            cv2.imshow('Face_recognition', img)
            cv2.waitKey(1)
cv2.destroyAllWindows()

# This statement will be executed in case if the user in known for the system by cheching the data base
if (name != "INCONNU") :

    # Inform the security part their is a known person in front of the door
    for i in range(0,3,1):
        user_message = (name + " à l'entrée!") 
        convert_text = pyttsx3.init()
        convert_text.say(user_message)
        convert_text.runAndWait()
    # Light up the front Led (Led1)
    for i in range(0, 10, 1):
        print(i)
        Led1.write(1)
        time.sleep(1)
        Led1.write(0)
    # Open the door automatically 
    for i in range (0, 15):
        Servo_motor.write(i)
    # wait for 5 seconds before closing the door
    time.sleep(5)
    # Close the door automatically 
    for i in range (0,110):
        Servo_motor.write(i)
    # Light up the inside led (Led2) for 10 seconds
    for i in range(0, 10, 1):
        print(i)
        Led2.write(1)
        time.sleep(1)
        Led2.write(0)

# The second traitement in case if the user is unknown        
elif (name == "INCONNU") :
    
    # Inform the security departement that their is an unknown in front of the door
    for i in range(0,3,1):
        user_message = ("un "+ name + " à l'entrée!") 
        convert_text = pyttsx3.init()
        convert_text.say(user_message)
        convert_text.runAndWait()
    
    # Get the name of the user
    fullname = input("Please enter your name:\n")

    # Get informations from the users
    # Handling the file by creating it and save informations in it
    file = open("C:\\Users\\who_I_am\\Desktop\\Face_recognation_project\\users_files\\{}.txt".format(fullname).replace(" ","_"), 'w')
    file.write(fullname)
    file.write('\n')
    file.write(input('Please enter your age:\n'))
    file.write('\n')
    file.write(input('Please enter your physical address:\n'))
    file.write('\n')
    file.write(input('Please enter your e-mail address:\n'))
    file.write('\n')
    file.write(input("What's your profession?\n"))
    file.write('\n')

    # open a session with ftp server
    session = ftplib.FTP('192.168.4.3', 'whoami_ftp', 'haz.127.0.0.1')
    file = open("C:\\Users\\who_I_am\\Desktop\\Face_recognation_project\\users_files\\{}.txt".format(fullname).replace(" ","_"), 'rb')
    #file = open("/home/whoami_ftp/face_recognation/{}.txt".format(fullname).replace(" ","_"), 'rb')
    session.storbinary('STOR {}.txt'.format(fullname), file)
    session.quit()

    # Face detection, take a picture of the user and stock it under the users_pictures directory to append the size of the data base
    haarcascade = cv2.CascadeClassifier('Haar_cascades\data\haarcascade_frontalface_alt2.xml')
    webcam = cv2.VideoCapture(0)
    for i in range(10,0,-1) :
        ret,frame = webcam.read()
        if ret == True :
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_coordinates = haarcascade.detectMultiScale(gray_frame)
    cv2.imshow('Face_Detection', frame)
    cv2.imwrite(dir_path+"\\{}.jpg".format(fullname), frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Light up the front Led (Led1)
    for i in range(0, 10, 1):
        print(i)
        Led1.write(1)
        time.sleep(1)
        Led1.write(0)
    # once the push_button is pressed the door will open automatically
    for i in range(0, 10, 1) :
        time.sleep(1)
        Butt_state = Button.read()
        print(Butt_state)
        if Butt_state is True :
            for i in range(0, 15):
                Servo_motor.write(i)
    # after 5 seconds the door will be closed automatically
    time.sleep(5)
    for i in range(0, 110):
        Servo_motor.write(i)
    # Light up the inside led (Led2) for 10 seconds
    for i in range (0, 10, 1):
        print(i)
        Led2.write(1)
        time.sleep(1)
        Led2.write(0)