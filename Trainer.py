import cv2
import numpy as np
import PoseEstimationModule as pem
import time



cap = cv2.VideoCapture("TrainerVideos/curls.mp4") #capture video

pose_detector = pem.PoseDetector()

while True:
    # success, img = cap.read()
    # img = cv2.resize(img, (1280, 720)) #resize video
    img = cv2.imread("TrainerVideos/curls2.jpg") #read test image
    img = pose_detector.find_pose(img, False)  #find pose but do not draw so as to focus on the three points angle is going to be calculated for.
    landmarks = pose_detector.find_landmarks(img, False) #find landmarks 
    # print(landmarks)
    if len(landmarks) != 0: #check that landmarks were found
        #find angle for left arm
        pose_detector.find_angle(img, 11, 13, 15)
        #find angle for right arm
        pose_detector.find_angle(img, 12, 14, 16)

    cv2.imshow("Image", img)
    cv2.waitKey(1)