import numpy as np
import cv2
import time

print ("imports")

#from IPython.display import clear_output

def get_available_cameras (upper_bound = 10, lower_bound = 0):
    available = []
    
    for i in range (lower_bound, upper_bound):
        cap = cv2.VideoCapture (i)
    
        if (cap.isOpened ()):
            available.append (i)
    
        cap.release ()
    
    return available

#print (get_available_cameras ())

print("cam")
cam1 = cv2.VideoCapture (0)

print ("started")

while (True):
    print ("it")
    ret1, frame1 = cam1.read ()
    
    cv2.waitKey (1)
    
    ker_sz = 19
    
    frame = frame1# - cv2.morphologyEx (frame1, cv2.MORPH_OPEN, np.ones ((ker_sz, ker_sz), np.uint8))
    #frame = cv2.morphologyEx (frame1, cv2.MORPH_OPEN, np.ones ((ker_sz, ker_sz), np.uint8))
    
    #frame = frame1 + 100
    
    #resized = cv2.resize (frame, (960, 720))
    
    cv2.imshow ("frame", frame)
    
    time.sleep (0.01)
    
    if (cv2.waitKey (1) & 0xFF == ord('q')):
        break

cam1.release ()

cv2.destroyAllWindows()