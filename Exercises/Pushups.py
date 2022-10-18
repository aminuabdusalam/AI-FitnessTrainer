import numpy as np


class Pushups():
    
    def __init__(self, detector,img, count, direction):
        self.detector, self.img = detector, img
        self.count = count
        self.direction = direction
        self.MIN_ANGLE, self.MAX_ANGLE = 200, 285

    def  get_legs_angle(self):
        pass 

    def get_left_arm_angle(self):
        left_arm_angle = self.detector.find_angle(self.img, 11, 13, 15)
        return left_arm_angle

    def get_right_arm_angle(self):
        right_arm_angle = self.detector.find_angle(self.img, 12, 14, 16)
        return right_arm_angle

    def get_arms_angle(self):
        self.left_arm_angle = self.detector.find_angle(self.img, 11, 13, 15)
        self.right_arm_angle = self.detector.find_angle(self.img, 12, 14, 16)
        

    def get_pushups_count(self):
        self.percent_left_arm = np.interp(self.get_left_arm_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(0, 100)) #returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x.
        self.percent_right_arm = np.interp(self.get_right_arm_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(0, 100)) #returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x.
        self.percent = (self.percent_left_arm + self.percent_right_arm) / 2
        
        
        self.bar_left = np.interp(self.get_left_arm_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(650, 100))
        self.bar_right = np.interp(self.get_right_arm_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(650, 100))
        self.bar = (self.bar_left + self.bar_right) / 2

        self.color = (0, 255, 255)
        if self.percent_left_arm == 100 and self.percent_right_arm == 100:
            self.color = (0, 255, 0)
            if self.direction == "upwards":
                self.count += 0.5
                self.direction = "downwards"
        
        if self.percent_left_arm == 0 and self.percent_right_arm == 0:
            self.color = (0, 255, 0)
            if self.direction == "downwards":
                self.count += 0.5
                self.direction = "upwards"
        
        return self.count, self.direction