import cv2
import time
import PoseEstimationModule as pem


cap = cv2.VideoCapture('PoseVideos/pushup_1.mp4')
previous_time = 0    


while True:
    success, img = cap.read()

    pose_detector = pem.PoseDetector()
    img = pose_detector.find_pose(img) #finds landmarks and draws line connecting them
    landmarks = pose_detector.find_landmarks(img, draw=False)
    if len(landmarks) != 0:
        print(landmarks[14]) #finds right elbow landmark
        cv2.circle(img, (landmarks[14][1], landmarks[14][2]), 1, (255, 0, 0), cv2.FILLED) #shows right elbow landmark on image


    current_time = time.time()
    fps = 1/(current_time - previous_time)  #calculates frame per second i.e. frame rate.
    previous_time = current_time

    cv2.putText(img, str(int(fps)), (70,50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)    #renders the text string (i.e.fps) in img.
    cv2.imshow("Image", img)    #displays image in img window.
    cv2.waitKey(1)  #displays the image for 1 milliseconds.