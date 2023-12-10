import cv2
import numpy as np
import delta_manager.camera as Camera


def click_event(event, u, v, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Pixel: ({u}, {v})')
        
        [x, y, z] = Camera.calculate_robot_XYZ(
            (u, v), 
            z_obj=0, 
            robot_capturing_coord=np.array([0,0,-37]),
            offset_valid=False
        )
        
        print(f'Robot: ({x:.2f}, {y:.2f}, {z:.2f})')

        homming_offset = [-14, 9, 0] - np.array([x, y, 0])

        print(f'new Robot coord for the point you clicked on: ({x + homming_offset[0]:.2f}, {y + homming_offset[1]:.2f}, {z:.2f})')
        np.save('./delta_manager/parameters/homming_offset.npy', homming_offset)

        cap.release()
        cv2.destroyAllWindows()
        exit(0)


cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

while True:
    _, frame = cap.read()

    # Image show
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 800, 600)
    cv2.setMouseCallback('image', click_event)
    cv2.imshow('image', frame)

    # Image save
    key_pressed = cv2.waitKey(1)
    if key_pressed == 27:   # Esc key
        break

cap.release()
cv2.destroyAllWindows()
