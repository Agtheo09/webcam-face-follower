from cvzone.FaceDetectionModule import FaceDetector
import cv2 as cv
import pyvirtualcam

cap = cv.VideoCapture(0)
detector = FaceDetector()

faces = []

def filterFaces(bboxs):
    return [bbox for bbox in bboxs if bbox["score"][0] > 0.7]

frameH, frameW = cap.read()[1].shape[:2]

print(frameW, frameH)

with pyvirtualcam.Camera(width=frameW, height=frameH, fps=30) as cam:
    while True:
        frame = cap.read()[1]

        img, bboxs = detector.findFaces(frame)
        faces = filterFaces(bboxs=bboxs)

        if len(faces) > 0:
            center = faces[0]["center"]

            cv.circle(img, center, 5, (255, 0, 255), cv.FILLED)

        # cv.imshow("Image", img)
        cam.send(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        cam.sleep_until_next_frame()
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv.destroyAllWindows()