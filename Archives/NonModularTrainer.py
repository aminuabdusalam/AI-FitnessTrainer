import cv2
import numpy as np
import PoseEstimationModule as pem
import time
from Exercises import Curls



cap = cv2.VideoCapture("TrainerVideos/curls.mp4") #capture video

pose_detector = pem.PoseDetector()

count = 0
direction = "UP" #assigns direction of curl as upward
previous_time = 0

while True:
    success, img = cap.read()
    if not success: #break if video or image has ended
        break
    img = cv2.resize(img, (1280, 720)) #resize video
    # img = cv2.imread("TrainerVideos/curls2.jpg") #read test image
    img = pose_detector.find_pose(img, False)  #find pose but do not draw so as to focus on the three points angle is going to be calculated for.
    landmarks = pose_detector.find_landmarks(img, False) #find landmarks 
    # print(landmarks)
        
    if len(landmarks) != 0: #check that landmarks were found
        #find angle for left arm
        left_arm_angle = pose_detector.find_angle(img, 11, 13, 15)
        MIN_ANGLE, MAX_ANGLE = 210, 315        
        percent = np.interp(left_arm_angle,(MIN_ANGLE, MAX_ANGLE),(0, 100)) #returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x.
        bar = np.interp(left_arm_angle, (MIN_ANGLE, MAX_ANGLE),(650, 100))
        

        # print(left_arm_angle, percent)

        # #check for the dumbbell curls
        color = (0, 255, 255)
        if percent == 100:
            color = (0, 255, 0)
            if direction == "UP":
                count += 0.5
                direction = "DOWN"
        
        if percent == 0:
            color = (0, 255, 0)
            if direction == "DOWN":
                count += 0.5
                direction = "UP"
        print(count)

        # curls = Curls.Curls(pose_detector, img)
        # count += curls.get_curls_count()
        # print(count)



        # Draw Bar
        cv2.rectangle(img, (1100,100), (1175,650), color, 4) #draws unfilled rectangle that dynamic bar is going to be placed in.
        cv2.rectangle(img, (1100,int(bar)), (1175,650),color, cv2.FILLED) #draws rectangle whose size changes depending on the bar value.
        cv2.putText(img, str(int(percent)) + "%", (1100, 75),
                    cv2.FONT_HERSHEY_PLAIN, 4, color,4)    #renders the text string (i.e.percent) in img.
            

        # Draw Curl Count
        cv2.rectangle(img, (0,500), (200,720), (0,255, 0), cv2.FILLED) #draws a filled rectangle (bar) that the curls count is going to be placed in.
        cv2.putText(img, str(int(count)), (25, 700),
                    cv2.FONT_HERSHEY_PLAIN, 15, (255,255,255),25)    #renders the text string (i.e.count) in img.
            
        current_time = time.time()
        fps = 1/(current_time - previous_time)  #calculates frame per second i.e. frame rate.
        previous_time = current_time
        cv2.putText(img, "fps= " + str(int(fps)), (50, 100),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),5)    #renders the text string (i.e.fps) in img.
      


        #find angle for right arm
        #right_arm_angle = pose_detector.find_angle(img, 12, 14, 16)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


