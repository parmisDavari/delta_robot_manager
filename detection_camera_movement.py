import cv2
from delta_manager.object_detector import *
import numpy as np
from delta_manager.camera import *
from delta_manager.delta_manager import DeltaManager
# from brown_detect import detect_toast


# Load Aruco detector
parameters = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000) # changed it from 50 to 1000


# Load Object Detector
detector = HomogeneousBgDetector()

# Load Cap
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# global variables
center_of_holes_X, center_of_holes_Y = 0, 0       
toaster_holes_detected = False
brown_toastes_detected = False
height_of_toaster = 19

Delta = DeltaManager()
Delta.connect_gripper()


final_center_of_bottom_toaster_hole_Y, final_center_of_toaster_holes_X = 0, 0

def dimension_approved(object_width, object_height):
        if ((object_height > 18.7 or object_height == 18.7) and (object_height < 20.5 or object_height == 20.5)):
                if ((object_width > 12 or object_width == 12) and (object_width < 14 or object_width == 14)):
                        return True
                else:
                        return False
        else:
                return False
            
            

            
while True:
    _, img = cap.read()
    img = undistort(img)
    # Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    if corners:

        # Draw polygon around the marker
        int_corners = np.intp(corners)
        cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners[0], True)

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 4 # changed from 20 to 4

        contours = detector.detect_objects(img)
        
        
        # Draw objects boundaries
        for cnt in contours:
            # Get rect
            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), angle = rect
            
            # Get Width and Height of the Objects by applying the Ratio pixel to cm
            object_width = w / pixel_cm_ratio
            object_height = h / pixel_cm_ratio
            
            
            # Calculate the distance between midpoints
            
            
            if(dimension_approved(object_width, object_height)):
                
                # Some constant values to calculate the center of main holes of the toaster
                constant = 3
                
                # center_of_big_hole_X, center_of_big_hole_Y = x, y 
                toaster_holes_detected = True
                
                three_cm_to_pixels = constant * pixel_cm_ratio
                center_of_toaster_holes_X = x
                center_of_bottom_toaster_hole_Y = y + three_cm_to_pixels
                center_of_top_toaster_hole_Y = y - three_cm_to_pixels
                
                # draw the middle point of the toaster holes as well
                cv2.circle(img, (int(center_of_toaster_holes_X), int(center_of_bottom_toaster_hole_Y)), 5, (6, 255, 235), -1)
                cv2.circle(img, (int(center_of_toaster_holes_X), int(center_of_top_toaster_hole_Y)), 5, (6, 255, 235), -1)
                
                
                # send the middle point coordinates to  a function that controlles the robot movement
                key = cv2.waitKey(1)
                if key == ord('a'):
                    [x_robot, y_robot, z_robot] = calculate_robot_XYZ((int(center_of_toaster_holes_X), int(center_of_bottom_toaster_hole_Y)),
                                height_of_toaster, '2f85')
                    final_center_of_bottom_toaster_hole_Y, final_center_of_toaster_holes_X = center_of_bottom_toaster_hole_Y, center_of_toaster_holes_X
                    
                    
                # Display rectangle
                box = cv2.boxPoints(rect)
                box = np.intp(box)
                cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.polylines(img, [box], True, (255, 0, 0), 2)
                cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
                cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
                
                # before detecting the toasts, the gripper needs to move
                
                detect_toast(img) #the function didn't work in the file check it


    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()