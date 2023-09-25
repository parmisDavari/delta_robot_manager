import cv2
import numpy as np
import PySimpleGUI as psg
import delta_manager.client as Client
import delta_manager.camera as Camera
import delta_manager.delta as Delta


def click_event(event, u, v, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Pixel: ({u}, {v})')

        [x, y, z] = Camera.calculate_robot_XYZ(
            (u, v), 
            z_obj, 
            robot_capturing_coord
        )
        
        print(f'Robot: ({x:.2f}, {y:.2f}, {z:.2f})')
        
        Client.order("move", f'{x},{y},{z}')


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

image_counter = 0

while True:
    _, frame = cap.read()

    # Undistort the frame
    undist_frame = Camera.undistort(frame)
    
    # Set object x, y, z coordinates
    z_obj  = 0
    robot_capturing_coord = np.array([0,0,-37])

    # Image show
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 1080, 950)
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

cap.release()
cv2.destroyAllWindows()
