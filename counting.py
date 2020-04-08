import numpy as np
import cv2
import time
from IPython.display import clear_output

import sys
sys.path.append("./robotics_course/modules/")

import input_output
import processor
import tracker

#inp = input_output.Source ("example_02.mp4")
inp = input_output.Source ("1")
#inp = cv2.VideoCapture (1)

out = input_output.Writer ("tracking1.mp4", 1200, 798, fps_ = 3)
#out = input_output.Writer ("tracking1.mp4", 1280, 640)

det = processor.Processors()

det.add_processor("people_extraction")

#det.add_filter (processor.resize (), "people_extraction", "resize")
#det.add_filter(processor.gaussian_blur(5), "people_extraction", "blur")
det.add_filter(processor.custom_operation (lambda img: cv2.medianBlur (img, 7), "median_blur"), "people_extraction", "blur")

det.add_filter (processor.colorspace_to_colorspace ("RGB", "BGR"),
                "people_extraction", "colorspace_change1")
det.add_filter (processor.colorspace_to_colorspace ("RGB", "HSV"),
                "people_extraction", "colorspace_change2")

det.add_filter(processor.background_subtraction(None, 5), "people_extraction", "background_subtraction")
det.add_filter (processor.inrange ((100, 100, 20), (255, 255, 255)), "people_extraction", "inrange_rgb")
det.add_filter(processor.morphology ("open"), "people_extraction", "erosion")

det.add_filter(processor.filter_connected_components(area_low_ = 1930), "people_extraction", "filter_cc")
det.add_filter(processor.max_area_cc_bbox(3), "people_extraction", "boxes")

#det.add_processor("human_extraction")
#det.add_filter (processor.inrange ((0, 0, 0), (105, 105, 105)), "human_extraction", "inrange_rgb")
#det.add_filter(processor.morphology ("open"), "human_extraction", "erosion")
#det.add_filter(processor.filter_connected_components(area_low_ = 1230), "human_extraction", "filter_cc")

tracker = tracker.Tracker (250, 0, 250, 400)

while (True):
    _, frame = inp.get_frame ()
    
    det.process(frame, "people_extraction")
    
    boxes = det.get_stages ("people_extraction") [-1]
    tracker.add_measurement (boxes)
    people_num = tracker.get_people_num ()
    tracker_frame = tracker.draw (frame)
    
    stages = det.get_stages_picts ("people_extraction", ["colorspace_change1",
                                   "colorspace_change2", "blur",
                                   "background_subtraction", "inrange_rgb", "filter_cc", "boxes"])
    
    output_frame = input_output.form_grid(stages + [tracker_frame], window_x_sz=1200)
    #print (output_frame.shape)
    
    cv2.imshow ("people detection", output_frame)
    
    out.write (output_frame)
    
    time.sleep (0.01)
    
    if (cv2.waitKey (1) & 0xFF == ord('q')):
        break

cv2.destroyAllWindows()