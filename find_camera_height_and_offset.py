import cv2
import numpy as np
import delta_manager.camera as Camera
from delta_manager.delta_manager import DeltaManager

def get_distance(point1, point2):
    return np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 + (point1[2]-point2[2])**2)

pixel1 = None
pixel2 = None

def get_distance_in_robot(pixel1, pixel2, camera_height, z_obj):
    point1 = Camera.pixel_to_robot_coordinates(
        pixel1, 
        camera_height=camera_height,
        z_obj=z_obj, 
        gripper='2f85',
        robot_capturing_coord = np.array(Delta.read_forward())
    )
    point2 = Camera.pixel_to_robot_coordinates(
        pixel2, 
        camera_height=camera_height,
        z_obj=z_obj, 
        gripper='2f85',
        robot_capturing_coord = np.array(Delta.read_forward())
    )
    return get_distance(point1, point2)

def click_event(event, u, v, flags, params):
    global pixel1, pixel2
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel1 = (u, v)
        print(f'Pixel1: {pixel1}')
    elif event == cv2.EVENT_RBUTTONDOWN:
        pixel2 = (u, v)
        print(f'Pixel2: {pixel2}')
        
        z_obj = 0
        camera_height = 50
        camera_height_defult = 50
        distance = get_distance_in_robot(pixel1, pixel2, camera_height_defult, z_obj)
        print(f'distance: {distance}')

        desired_distance = 9
        while np.abs(distance - desired_distance) > 0.01:
            if distance > desired_distance:
                camera_height -= 0.1
            else:
                camera_height += 0.1
            distance = get_distance_in_robot(pixel1, pixel2, camera_height, z_obj)
            print(f'distance: {distance}')

        
        [x, y, z] = Camera.pixel_to_robot_coordinates(
            pixel1, 
            z_obj = 0,
            camera_height = camera_height,
            robot_capturing_coord = np.array(Delta.read_forward()),
            offset_valid = False
        )
        
        print(f'Robot: ({x:.2f}, {y:.2f}, {z:.2f})')

        homming_offset = [-14, 9, camera_height] - np.array([x, y, 0])

        print(f'new Robot coord for the point you clicked on: ({x + homming_offset[0]:.2f}, {y + homming_offset[1]:.2f}, {z:.2f})')
        np.save('./delta_manager/parameters/homming_offset.npy', homming_offset)

        print(f'camera_height: {camera_height}')

Delta = DeltaManager()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

image_counter = 0

while True:
    _, frame = cap.read()

    # Undistort the frame
    frame = Camera.undistort(frame)
    
    # Image show
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 800, 600)
    cv2.setMouseCallback('image', click_event)
    cv2.imshow('image', frame)

    # Image save
    key_pressed = cv2.waitKey(1)
    if key_pressed == 27:   # Esc key
        break
    elif key_pressed == ord('f'):
        current_position = Delta.read_forward()
        print(f'Current position: {current_position}')
    elif key_pressed == ord('h'): 
        Delta.go_home()

cap.release()
cv2.destroyAllWindows()
