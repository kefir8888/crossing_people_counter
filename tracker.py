import numpy as np
import math
import cv2

class Tracker:
    def __init__ (self, x1_, y1_, x2_, y2_, tracking_points_ = 8, ignore_th_ = 60):
        self.x1 = x1_
        self.y1 = y1_
        self.x2 = x2_
        self.y2 = y2_
        
        #self.k = (y2_ - y1_) / (x2_ - x1_)
        #self.b = 0
        self.tracking_points = tracking_points_
        self.ignore_th = ignore_th_
        
        self.people_num = 0
        self.closest_box = []
    
    def _find_distance (self, box):
        cx = (box [0] [0] + box [1] [0]) / 2
        cy = (box [0] [1] + box [1] [1]) / 2
        
        #distance = (self.k * cx - cy + self.b) / math.sqrt (self.k**2 + 1)
        
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2
        distance = ((y2 - y1) * cx - (x2 - x1) * cy + x2 * y1 - y2 * x1) / (math.sqrt ((y2 - y1)**2 + (x2 - x1)**2))
        
        if (distance > self.ignore_th):
            distance = 0
        
        return distance
    
    def add_measurement (self, boxes):
        #print ("boxes: ", boxes)
        
        if (len (boxes) > 0):
            closest = sorted (boxes, key=self._find_distance) [0]
            
            if (len (self.closest_box) < self.tracking_points):
                self.closest_box.append (closest)
            
            else:
                self.closest_box.pop (0)
                self.closest_box.append (closest)
            
            distances = [self._find_distance (box) for box in self.closest_box]
            
            p1 = sum (distances [: self.tracking_points // 2])
            p2 = sum (distances [self.tracking_points // 2 :])
            
            if (p1 * p2 < 0):
                if (p1 < 0):
                    self.people_num += 1

                else:
                    self.people_num -= 1
                
                self.closest_box.clear ()
    
    def get_people_num (self):
        return self.people_num
    
    def draw (self, img):
        result = img.copy ()
        h, w, _ = img.shape
        
        result = cv2.putText (result, str (self.people_num), (30, 100), cv2.FONT_HERSHEY_SIMPLEX,  
                   4, (0, 255, 0), 7, cv2.LINE_AA)
        
        #k = self.k
        #b = self.b
        
        #x1 = 0
        #y1 = b
        #x2 = w
        #y2 = k * w + b
        
        #if (y2 > h):
        #    x2 = (h-b) / k
        #    y2 = h
        
        cv2.line (result, (int (self.x1), int (self.y1)), (int (self.x2), int (self.y2)), (100, 200, 30), 5)
        
        for i in range (0, min (self.tracking_points // 2, len (self.closest_box))):
            box = self.closest_box [i]
            cv2.rectangle (result, box [0], box [1], (100, 200, 100), 5)
        
        return result