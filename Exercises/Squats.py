
import numpy as np


class Squats():
    
    def __init__(self, detector,img, count, direction):
        self.detector, self.img = detector, img
        self.count = count
        self.direction = direction
        self.MIN_ANGLE, self.MAX_ANGLE = 190, 270

    def get_left_leg_angle(self):
        left_leg_angle = self.detector.find_angle(self.img, 23, 25, 27) #23- left_hip, 25- left_knee, 27- left_ankle. Check Miscellanous/pose_landmarks.png
        return left_leg_angle

    def get_right_leg_angle(self):
        right_leg_angle = self.detector.find_angle(self.img, 24, 26, 28) #24- right_hip, 26- right_knee, 28- right_ankle
        return right_leg_angle
   
    def get_squats_count(self):
        self.percent_left_leg = np.interp(self.get_left_leg_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(0, 100)) #returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x.
        self.percent_right_leg = np.interp(self.get_right_leg_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(0, 100)) #returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x.
        self.percent = (self.percent_left_leg + self.percent_right_leg) / 2
        
        
        self.bar_left = np.interp(self.get_left_leg_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(650, 100))
        self.bar_right = np.interp(self.get_right_leg_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(650, 100))
        self.bar = (self.bar_left + self.bar_right) / 2

        self.color = (0, 255, 255)
        if self.percent_left_leg == 100 and self.percent_right_leg == 100:
            self.color = (0, 255, 0)
            if self.direction == "upwards":
                self.count += 0.5
                self.direction = "downwards"
        
        if self.percent_left_leg == 0 and self.percent_right_leg == 0:
            self.color = (0, 255, 0)
            if self.direction == "downwards":
                self.count += 0.5
                self.direction = "upwards"
        
        return self.count, self.direction


# 1) Foot Positioning
# 2) Hip Hinge
# 3) Hip and Ankle Flexibility

# hip, knees, ankle
