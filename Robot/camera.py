from Robot import cap
import cv2
import numpy as np

def find_centroid():
    _, frame = cap.read()
    frame = cv2.flip(frame, 0)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    low_red = np.array([161, 155, 40])
    high_red = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_frame, low_red, high_red)
    
    _, thresh = cv2.threshold(mask, 127, 255, 0)
    M = cv2.moments(thresh)
    if M["m00"] > 10000:
        cX = (M["m10"] / M["m00"]) / frame.shape[1]
        cY = (M["m01"] / M["m00"]) / frame.shape[0]
    else:
        cX = 0.5
        cY = 0.5
    
    cv2.imshow("WoW", frame)
    key = cv2.waitKey(10)
    if key==27:
        return -1,-1
    else:
        return cX, cY