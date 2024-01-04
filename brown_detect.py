#library
import numpy as np
import argparse
import cv2 

def detect_toast(img):
    
    # pre-processing

    is_toast_detected = False
    img = cv2.imread('photos/practise.jpg')
    new_width = 250
    new_height = 250
    # Resize the image
    resized_image = cv2.resize(img, (new_width, new_height))
    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
    lower_brown = np.array([10, 50, 50])
    upper_brown = np.array([30, 255, 255])
    # lower_brown = np.array([15, 30, 58])
    # upper_brown = np.array([0, 25, 58])
    brown_mask = cv2.inRange(hsv_image, lower_brown, upper_brown)
    if cv2.countNonZero(brown_mask) > 0:
        is_toast_detected = True
        brown_regions = cv2.bitwise_and(resized_image, resized_image, mask = brown_mask)
        # thresh, image = cv2.threshold(brown_regions, 127, 255, 0)
        contours, _ = cv2.findContours(brown_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        object_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 200:
                object_contours.append(cnt)
        for c in object_contours:
            # print("1")
            # cv2.polylines(img, [c], True, (0,0,255),2)
            rect = cv2.minAreaRect(c)
            (x, y), (w, h), angle = rect
            box = np.intp(cv2.boxPoints(rect))
            cv2.polylines(resized_image, [box], True, (255, 0 , 0), 2)
            cv2.circle(resized_image, (int(x), int(y)), 5, (0, 255, 0), -1)
    else:
        is_toast_detected = False
    cv2.imshow('Original Image', resized_image)
    cv2.imshow('Brown Regions', brown_regions)
    cv2.waitKey(0)
    cv2.destroyAllWindows()