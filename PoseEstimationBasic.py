import enum
import cv2
import mediapipe as mp
import time



mpPose = mp.solutions.pose  #retreives pre-built/trained pose model from mp module.
pose = mpPose.Pose()  #creates object of mpPose class/model.
mpDraw = mp.solutions.drawing_utils #retreives mp solution for drawing utilities.

cap = cv2.VideoCapture('PoseVideos/armraise_1.mp4')
previous_time = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #converts image from BGR colorspace to RGB colorspace since mediapipe uses RGB.
    results = pose.process(imgRGB)  #result ( coordinate locations of body part (x,y,z) , and visibility) from sending image to model for pose_landmark detection.
    # print(results.pose_landmarks)
    if results.pose_landmarks: #checks if landmark is detected.
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS) #draws line connecting the detected landmarks (shown as dots) on image.
        for id,landmark in enumerate(results.pose_landmarks.landmark): #extracts and labels info of each landmark.
            height, width, channel = img.shape  #
            print(id, landmark)
            cx, cy = int(landmark.x*width), int(landmark.y*height) #calculates actual x and y values [in int since pixels are ints] since mpPose returns a ratio of x & y to width and height respectively.
            cv2.circle(img,  (cx, cy), 4, (255, 0, 0), cv2.FILLED) #confirms and shows that pose detection is working properly by filling landmarks.
    

    current_time = time.time()
    fps = 1/(current_time - previous_time)  #calculates frame per second i.e. frame rate.
    previous_time = current_time

    cv2.putText(img, str(int(fps)), (70,50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)    #renders the text string (i.e.fps) in img.
    cv2.imshow("Image", img)    #displays image in img window.
    cv2.waitKey(1)  #displays the image for 1 milliseconds.