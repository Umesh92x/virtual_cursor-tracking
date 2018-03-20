# Using Android IP Webcam video .jpg stream (tested) in Python2 OpenCV3

import urllib.request
import cv2
import numpy as np
import time

# Stream Video with OpenCV from an Android running IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam)
# Code Adopted from http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera

import cv2
import urllib.request
import numpy as np
import sys
import pyautogui
import tkinter as tk
root = tk.Tk()
from pynput.mouse import Button,Controller
mouse=Controller()
sx = root.winfo_screenwidth()
sy = root.winfo_screenheight()
(camx,camy)=(620,444)
SCREEN_X, SCREEN_Y = pyautogui.size()
hoststr = "http://192.168.1.2:4747/mjpegfeed?640x480"
pyautogui.moveTo(500,500)
print ('Streaming ' + hoststr)

stream=urllib.request.urlopen(hoststr)
bytes=b''
lower_blue=np.array([136,87,111],dtype='uint8')
upper_blue=np.array([180,255,245],dtype='uint8')
while True:

    bytes+=stream.read(1024)

    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')


    if a!=-1 and b!=-1:
        #print(("hvghvbn"))
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]

        frame= cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_32F)
        frame = cv2.resize(frame, (620,444))
        frame=cv2.flip(frame,1)
        #cv2.imshow('hoststr', frame)
        #TODO

        #ret, frame = i.read()
        HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(HSV, lower_blue,upper_blue)
        HSV_red = cv2.bitwise_and(frame, frame, mask=mask)

        kernelOpen = np.ones((2, 2))
        kernelClose = np.ones((10, 10))
        opening = cv2.morphologyEx(HSV_red, cv2.MORPH_OPEN, kernelOpen)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelClose)
        maskE = cv2.erode(mask, None, iterations=0)
        maskD=cv2.dilate(maskE,None,iterations=0)

        _, cnts, h = cv2.findContours(maskD.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            ((x1, y1), radius) = cv2.minEnclosingCircle(c)
            x1 = int(x + w / 2)
            y1 = int(y + h / 2)
            cx=x1
            cy=y1

            cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)
            mouseLoc1,mouseLoc2 = ((cx * sx / camx), (cy * sy / camy))
            print(mouseLoc1,'and',mouseLoc2)
            mouse.position =(int(mouseLoc1),int(mouseLoc2))
            #pyautogui.moveTo(mouseLoc)
            cv2.moveWindow('frame',200,200)
            cv2.imshow('frame', frame)

            cv2.waitKey(1)

if __name__=='__main__':
    print('successfull')
