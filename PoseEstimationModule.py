import enum
import cv2
import mediapipe as mp
import numpy as np
import time
from math import atan, atan2, degrees



class PoseDetector():
    """Class with methods to detect pose and find all this points for us."""

    def __init__(self, static_image_mode=False, smooth_landmarks=True, 
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) -> None:
        """Initializes a PoseDetector object.
        
        Args:
            static_image_mode: Whether to treat the input images as a batch of static
                and possibly unrelate images, or a video stream. If set to False, it 
                will try to detect the most prominent person in the very first images,
                and upon a successful detection further localizes the pose landmarks.
                If set to True, person detection runs every input image, ideal for 
                processing a batch of static, possibly unrelated, images. See 
                details in https://solutions.mediapipe.dev/pose#static_image_mode.
            upper_body_only: Whether to track the full set of 33 pose landmarks or
                only the 25 upper-body landmarks. See full details in
                https://solutions.mediapipe.dev/pose#static_image_mode.
            smooth_landmarks: If set to true, the solution filters pose landmarks 
                across different input images to reduce jitter.
            min_detection_confidence: Minimum confidence value ([0.0, 1.0]) from the
                person-detection model for the detection to be considered successful.
            min_tracking_confidence: Minimum confidence value ([0.0, 1.0]) from the
                landmark-tracking model for the pose landmarks to be considered tracked
                successfully, or otherwise person detection will be invoked automatically on the next input image. 
        """
        self.static_image_mode = static_image_mode
        # self.upper_body_only = upper_body_only
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mp_pose = mp.solutions.pose  #retreives pre-built/trained pose model from mp module.
        self.pose = self.mp_pose.Pose(static_image_mode = self.static_image_mode,
                                smooth_landmarks=self.smooth_landmarks, min_detection_confidence=self.min_detection_confidence, 
                                min_tracking_confidence=self.min_tracking_confidence)  #creates object of mp_pose class/model.
        
        self.pose = self.mp_pose.Pose(False, 1, True, False, True, 0.5,0.5)
        self.mp_draw = mp.solutions.drawing_utils #retreives mp solution for drawing utilities.


    def find_pose(self, img, draw=True):
    
        """Detects posture in an image.
        Args:
            img: the image.
            draw: Whether user wants to draw landmarks i.e display in the image or not.        
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #converts image from BGR colorspace to RGB colorspace since mediapipe uses RGB.
        self.results = self.pose.process(imgRGB)  #result ( coordinate locations of body part (x,y,z) , and visibility) from sending image to model for pose_landmark detection.
        # print(results.pose_landmarks)
        if self.results.pose_landmarks: #checks if landmark is detected.
            if draw: #checks whether draw is set to True.
                self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, 
                                            self.mp_pose.POSE_CONNECTIONS) #draws line connecting the detected landmarks (shown as dots) on image.

        return img     
        
    def find_landmarks(self, img, draw=True):
        """Gets landmarks of an image.
        Args:
            img: the image.
            draw: Whether user wants to draw landmarks i.e display in the image or not.        
        """
        self.landmarks =[]
        if self.results.pose_landmarks: #checks if landmark is detected.
            for id,landmark in enumerate(self.results.pose_landmarks.landmark): #extracts and labels info of each landmark.
                height, width, channel = img.shape  #
                # print(id, landmark)
                cx, cy = int(landmark.x*width), int(landmark.y*height) #calculates actual x and y values [in int since pixels are ints] since mp_pose returns a ratio of x & y to width and height respectively.
                self.landmarks.append([id,cx,cy])
                if draw:
                    cv2.circle(img,  (cx, cy), 15, (255, 0, 0), cv2.FILLED) #confirms and shows that pose detection is working properly by filling landmarks.
        return self.landmarks


    def find_angle(self, img, landmark1, landmark2, landmark3, draw=True):
        """Gets angle between three landmarks(points) in an image.
        Args:
            img: the image.
            landmark1: the first landmark.
            landmark2: the second landmark (fulcrum point).
            landmark3: the third landmark.
            draw: Whether user wants to draw landmarks i.e display in the image or not.        
        """

        # Retreive the coordinates of the three landmarks
        _,x1, y1 = self.landmarks[landmark1]  #retrieves the x and y coordinate of the landmark1
        _,x2, y2 = self.landmarks[landmark2]  #retrieves the x and y coordinate of the landmark2
        _,x3, y3 = self.landmarks[landmark3]  #retrieves the x and y coordinate of the landmark3


        # Calculate the angle between the landmarks (points).
        # angle = degrees(atan2(y3-y2, x3-x2) - 
        #                 atan2(y1-y2, x1-x2))    #convert from radians to degree (224 degrees)
        # if angle < 0:
        #     angle += 360

        #credit for method to calculate angle: https://manivannan-ai.medium.com/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd
        a = np.array([x1,y1])  
        b = np.array([x2,y2])
        c = np.array([x3,y3])

        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        angle = 360 - np.degrees(angle) #get exterior angle
        # print(angle)   #134 degrees



        #Draw to make sure landmarks(points) are being detected correctly.
        if draw:  
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3) #draw line (thickness:3) connecting landmark1 and landmark2
            cv2.line(img, (x2, y2), (x3, y3), (0, 255, 0), 3) #draw line (thickness:3) connecting landmark2 and landmark3
            
            cv2.circle(img,  (x1, y1), 10, (0, 0, 255), cv2.FILLED) #confirms and shows that that the landmark1 is being detected correctly by filling the landmark in the image.
            cv2.circle(img,  (x1, y1), 15, (0, 0, 255), 2) #draws a larger circle (thickness:2) over the filled circle
            cv2.circle(img,  (x2, y2), 10, (0, 0, 255), cv2.FILLED) #confirms and shows that that the landmark2 is being detected correctly by filling the landmark in the image.
            cv2.circle(img,  (x2, y2), 15, (0, 0, 255), 2) #draws a larger circle (thickness:2) over the filled circle
            cv2.circle(img,  (x3, y3), 10, (0, 0, 255), cv2.FILLED) #confirms and shows that that the landmark3 is being detected correctly by filling the landmark in the image.
            cv2.circle(img,  (x3, y3), 15, (0, 0, 255), 2) #draws a larger circle (thickness:2) over the filled circle

            cv2.putText(img, str(int(angle)), (x2-80, y2+10),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2) #place angle "text" close to middle point (x2, y2)
        return angle

def main():
    cap = cv2.VideoCapture('PoseVideos/armraise_1.mp4')
    previous_time = 0    



    while True:
        success, img = cap.read()

        pose_detector = PoseDetector()
        img = pose_detector.find_pose(img) #finds landmarks and draws line connecting them
        landmarks = pose_detector.find_landmarks(img, draw=False)
        if len(landmarks) != 0:
            print(landmarks[14]) #finds right elbow (landmark 14). Check pose_landmarks.png for more details
            cv2.circle(img, (landmarks[14][1], landmarks[14][2]), 1, (255, 0, 0), cv2.FILLED) #shows right elbow landmark on image


        current_time = time.time()
        fps = 1/(current_time - previous_time)  #calculates frame per second i.e. frame rate.
        previous_time = current_time

        cv2.putText(img, str(int(fps)), (70,50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)    #renders the text string (i.e.fps) in img.
        cv2.imshow("Image", img)    #displays image in img window.
        cv2.waitKey(1)  #displays the image for 1 milliseconds.



if __name__ == "__main__":
    main()