import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
from pyautogui import press

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0) #Start capturing the video
anterior = 0
lasttotal=0 #Count for how many instants the person is looking at or away from the camera
sleep(15) #Time provided to start playing video in VLC player. Press the pause button manually in the player

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    ) #Detect the faces present in the frame

    # If there are no faces present incement the count starting from 0 every 0.2 seconds
    if len(faces)==0:
        if lasttotal<0:
            lasttotal=1
        else:

            lasttotal+=1
    #If there are faces decrement the count starting from 0
    else:
        if lasttotal>0:
            lasttotal=-1
        else:
            lasttotal-=1

    if lasttotal==5 or lasttotal==-5: #If you observe that the viewer is looking away from screen(or come back to it) for 1 sec, press pause (or play)
        press('space') #pause or play

    #Exit button
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    sleep(0.2)

video_capture.release()
cv2.destroyAllWindows()
