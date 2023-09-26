import cv2
import numpy as np
import PySimpleGUI as psg
import delta_manager.camera as Camera
from delta_manager.delta_manager import DeltaManager


def click_event(event, u, v, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Pixel: ({u}, {v})')

        z_obj = 0
        # print(Delta.read_forward())

        [x, y, z] = Camera.calculate_robot_XYZ(
            (u, v), 
            z_obj, 
            robot_capturing_coord=np.array([0,0,-37]),
            offset_valid=True
        )

        print(f'Robot: ({x:.2f}, {y:.2f}, {z:.2f})')

        Delta.move(x, y, z)


Delta = DeltaManager()
Delta.connect_gripper()

cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

image_counter = 0

while True:
    _, frame = cap.read()

    # Undistort the frame
    undist_frame = Camera.undistort(frame)
    
    # Image show
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 800, 600)
    cv2.setMouseCallback('image', click_event)
    cv2.imshow('image', frame)

    # Image save
    key_pressed = cv2.waitKey(1)
    if key_pressed == 27:   # Esc key
        break
    elif key_pressed == ord(' '): 
        cv2.imwrite('./Images/image'+str(image_counter)+'.jpg', frame)
        print(f'image {image_counter} saved.')
        image_counter += 1
    elif key_pressed == ord('o'):
        Delta.open_gripper()
    elif key_pressed == ord('c'):
        Delta.close_gripper()
    elif key_pressed == ord('h'): 
        Delta.go_home()

cap.release()
cv2.destroyAllWindows()
