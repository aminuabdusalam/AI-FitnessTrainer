import numpy as np

class Curls():

    def __init__(self, detector,img, count, direction, left_arm = True, right_arm = False):
        self.detector, self.img = detector, img
        self.left_arm, self.right_arm = left_arm, right_arm
        self.count = count
        self.direction = direction #assigns direction of curl as upward
        self.MIN_ANGLE, self.MAX_ANGLE = 210, 315

    def get_left_arm_angle(self):
        left_arm_angle = self.detector.find_angle(self.img, 11, 13, 15)
        return left_arm_angle

    def get_right_arm_angle(self):
        right_arm_angle = self.detector.find_angle(self.img, 12, 14, 16)
        return right_arm_angle

    def get_curls_count(self):
        if self.left_arm:
            self.percent = np.interp(self.get_left_arm_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(0, 100)) #returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x.
            self.bar = np.interp(self.get_left_arm_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(650, 100))  
        
        if self.right_arm:
            self.percent = np.interp(self.get_right_arm_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(0, 100)) #returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x.
            self.bar = np.interp(self.get_right_arm_angle(),(self.MIN_ANGLE, self.MAX_ANGLE),(650, 100))
        
        
        self.color = (0, 255, 255)
        if self.percent == 100:
            self.color = (0, 255, 0)
            if self.direction == "UP":
                self.count += 0.5
                self.direction = "DOWN"
        
        if self.percent == 0:
            self.color = (0, 255, 0)
            if self.direction == "DOWN":
                self.count += 0.5
                self.direction = "UP"
        
        return self.count, self.direction

    

    