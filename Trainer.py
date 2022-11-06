import cv2
import numpy as np
import PoseEstimationModule as pem
import time
from Exercises import Curls, Pushups, Squats
from Text2SpeechSpeech2Text import text_to_speech, speech_to_text 
from threading import Thread

exercises, choice, response = ["curls", "push ups", "squats"], "", ["",""]
while choice not in exercises:
    # choice = input("Enter the kind of exercise ('help' to view available exercises): ").lower()
    text_to_speech("Say your choice of exercise or say help to view available exercises.")
    choice = speech_to_text()
    if choice[0] == "p":
        text_to_speech("Did you mean push ups? Say Yes or No")
        response = [speech_to_text(), "push ups"]
    if choice[0] == "s":
        text_to_speech("Did you mean squats? Say Yes or No")
        response = [speech_to_text(), "squats"]
    if choice[0] == "c":
        text_to_speech("Did you mean curls? Say Yes or No")
        response = [speech_to_text(), "curls"]
    if choice[0] == "h":
        text_to_speech("Did you mean to ask for help? Say Yes or No")
        response = [speech_to_text(), "help"]
    
    if response[0][:3] == "yes":
        choice = response[1]
        
    if choice == "help":
        text_to_speech("available exercises include" + exercises)
        # print("available exercises include", exercises)
    elif choice not in exercises:
        text_to_speech("Maybe missing an 's' or a character? Say 'help' to view available exercises.")
        # print("Maybe missing an 's' or a character? ('help' to view available exercises)")

# choice = "squats"
trainer_videos = {"curls":"curls.mp4", "push ups":"pushups.mp4", "squats":"squats.mp4"}


cap = cv2.VideoCapture("TrainerVideos/" + trainer_videos[choice]) #capture video

# # For webcam input:
# cap = cv2.VideoCapture(0)

pose_detector = pem.PoseDetector()

count, counts = 0, set()
direction = "upwards" #assigns direction of curl as upward
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
        
        if choice == "curls":
            exercise = Curls.Curls(pose_detector, img, count, direction)            
            count, direction = exercise.get_curls_count()

        if choice == "push ups":
            exercise = Pushups.Pushups(pose_detector, img, count, direction)            
            count, direction = exercise.get_pushups_count()

        if choice == "squats":
            exercise = Squats.Squats(pose_detector, img, count, direction)            
            count, direction = exercise.get_squats_count()

        print(count)
    
        if (count not in counts) and (count == int(count)):
            counts.add(int(count))
           
        # Draw Bar
        cv2.rectangle(img, (1100,100), (1175,650), exercise.color, 4) #draws unfilled rectangle that dynamic bar is going to be placed in.
        cv2.rectangle(img, (1100,int(exercise.bar)), (1175,650),exercise.color, cv2.FILLED) #draws rectangle whose size changes depending on the bar value.
        cv2.putText(img, str(int(exercise.percent)) + "%", (1100, 75),
                    cv2.FONT_HERSHEY_PLAIN, 4, exercise.color,4)    #renders the text string (i.e.percent) in img.
            

        # Draw Curl Count
        cv2.rectangle(img, (0,500), (200,720), (0,255, 0), cv2.FILLED) #draws a filled rectangle (bar) that the exercise count is going to be placed in.
        cv2.putText(img, str(int(count)), (25, 700),
                    cv2.FONT_HERSHEY_PLAIN, 15, (255,255,255),25)    #renders the text string (i.e.count) in img.
            
        current_time = time.time()
        fps = 1/(current_time - previous_time)  #calculates frame per second i.e. frame rate.
        previous_time = current_time
        cv2.putText(img, "fps= " + str(int(fps)), (50, 100),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),5)    #renders the text string (i.e.fps) in img.

        if (count not in counts) and (count == int(count)):
            counts.add(int(count))
        
            t2s_thread = Thread(
                    target=text_to_speech, args=(str(int(count)))
                )
           
            t2s_thread.start()
            t2s_thread.join()

    cv2.imshow("Image", img)
    cv2.waitKey(1)


