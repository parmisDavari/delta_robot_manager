# delta_robot_manager
# To use Delta and Gripper commands follow these instructions:
## Import these libraries...
```
from delta_manager.delta_manager import DeltaManager
```
## Use the library using this line...
```
Delta = DeltaManager()
```
# Commands you can use:

## To use Gripper connect to it using its USB cable and turn its power on then use this line to connect to the Gripper 
```
Delta.connect_gripper()
```
## Gripper functions:
### Gripper open:
```
Delta.open_gripper()
```
### Gripper open a bit:
```
Delta.open_gripper_aBit()
```
### Gripper close:
```
Delta.close_gripper()
```
### Gripper close with feedback:
```
Delta.close_gripper_with_feedback() # Returns the result of Grasping: "DoneGrasp" or "failed"
```
### Gripper rotate:
```
Delta.rotate_gripper(angle): # On degree -90:90 (its ralative to the current angle)
```
### Gripper force:
```
Delta.force_gripper(force): # int from 1 to 5000 uncomment and ask Navid Asadi if you want to use. 
```
### Gripper wait:
```
Delta.wait_till_done()
```
# Delta Parallel Robot(DPR) functions(connect to Taarlabs WIFI):
### Delta home:
```
Delta.go_home()
```
### Delta move:
```
Delta.move(x, y, z) # Moves in 8 seconds
```
### Delta move with given time:
```
Delta.move_with_time(x, y, z, t) # Dont use times less than 3 seconds ask Navid Pasiar or Arvin Mohammadi if you want.
```
### Delta wait till done:
```
Delta.wait_till_done_robot()
```
### Delta End Effector coordinates:
```
x,y,z = Delta.read_forward()
```
### Delta stop server:
```
Delta.delta_stop_server()
```

# To use camera coordinates to move Delta follow these instructions:

## To correct robots homming Error move the robot to (0,0,-37) and Run set_homming_offset.py ,click on the corner of the grid on robots base.
! [Correct the homming offset](Images/Calibration_offset_correction.jpg)

## Import these libraries
```
import cv2
import numpy as np
import delta_manager.camera as Camera
from delta_manager.delta_manager import DeltaManager
```
## Get video input from DPRs camera
```
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

while True:
    _, frame = cap.read()

    # Undistort the frame
    frame = Camera.undistort(frame)    
```
## To convert (U,V) pixel coordinate to (X,Y,Z) Delta Parallel Robot use:
```
using_fom_flag = input("Are you using fom?(Y/N)")
if using_fom_flag.upper() == "Y":
    z_fom = 2
else:
    z_fom = 0
z_obj = 1.9 # put your objects height here

[x, y, z] = Camera.pixel_to_robot_coordinates(
    (u, v), 
    camera_height=48.8,
    z_obj = z_fom + z_obj, 
    gripper='2f85',
    robot_capturing_coord=np.array(Delta.read_forward())
)
z -= z_obj # if your objects height is short
# else z -= 2 or 3 cm

```