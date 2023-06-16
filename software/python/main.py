from cvzone.FaceDetectionModule import FaceDetector
import cv2 as cv
import pyvirtualcam
import serial
import numpy as np
import time

# Arduino Staff
arduino = serial.Serial("COM4", 9600, timeout=.1)

def writeDataToSerial(pos=[500, 500]):
    strToSend = f"{pos[0]}:{pos[1]}"
    
    print(strToSend)

    arduino.write(bytes(strToSend, 'utf-8'))

cap = cv.VideoCapture(0)
detector = FaceDetector()

faces = []

def filterFaces(bboxs):
    return [bbox for bbox in bboxs if bbox["score"][0] > 0.7]

frameDimensions = cap.read()[1].shape[:2]
frameW, frameH = frameDimensions

# with pyvirtualcam.Camera(width=frameH, height=frameW, fps=30) as cam:
while True:
    # Read Frame From Webcam
    frame = cap.read()[1]

    # FInd Faces
    img, bboxs = detector.findFaces(frame)
    faces = filterFaces(bboxs=bboxs)


    if len(faces) > 0:

        # Capture Center X, Y
        center = np.array(faces[0]["center"])
        
        # Map Values Between 0-1000
        x = (center[0] / frameH) * 1000
        y = (center[1] / frameW) * 1000

        # Send Positions To Arduino
        writeDataToSerial(pos=[round(x), round(y)])

        # Draw Center Point
        cv.circle(img, center, 5, (255, 0, 255), cv.FILLED)
    # Send Frame To Virtual Cam
    # cam.send(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    # cam.sleep_until_next_frame()
    
    cv.imshow('View', img)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()