# delta_robot_manager
# To use Delta and Gripper commands follow these instructions:
## Import this library
```
from delta_manager.delta_manager import DeltaManager
```
## Use the library using this line...
```
Delta = DeltaManager()
```
# Commands you can use:

## Write this line to connect to the Gripper 
>[!NOTE]
> Connect to the Gripper using its USB cable and turn its power on

>[!Caution]
> DO NOT REMOVE THE USB CABLE WHILE THE POWER IS ON
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
Delta.close_gripper_with_feedback()
```
>[!NOTE]
> Returns the result of Grasping: "DoneGrasp" or "failed"

### Gripper rotate:
```
Delta.rotate_gripper(angle):
```
> [!NOTE]
> Angle in degree -90:90 (it is relative to the current angle)

### Gripper force:
```
Delta.force_gripper(force):
```
>[!NOTE]
> int from 1 to 5000 uncomment it from delta_manager.py and ask Navid Asadi if you want to use.

### Gripper wait:
```
Delta.wait_till_done()
```
# Delta Parallel Robot(DPR) functions:
>[!NOTE]
> Connect to Taarlabs WIFI

### Delta home:
```
Delta.go_home()
```
### Delta move:
```
Delta.move(x, y, z)
```
>[!NOTE]
>Moves in 8 seconds

### Delta move with the given time:
```
Delta.move_with_time(x, y, z, t)
```
>[!WARNING]
> Don't use times less than 3 seconds ask Navid Pasiar or Arvin Mohammadi if you want.

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
>[!IMPORTANT]
> Move the robot to (0,0,-37)
>
## To correct robots homming Error run set_homming_offset.py, click on the corner of the grid on the robots base.
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Images/Calibration_offset_correction.jpg">
  <source media="(prefers-color-scheme: light)" srcset="Images/Calibration_offset_correction.jpg">
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="Images/Calibration_offset_correction.jpg">
</picture>


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
## To convert (U, V) pixel coordinates to (X, Y, Z) Delta Parallel Robot use:
```
using_fom_flag = input("Are you using fom?(Y/N)")
if using_fom_flag.upper() == "Y":
    z_fom = 2
else:
    z_fom = 0
z_obj = 1.9 # Put your objects height here

[x, y, z] = Camera.pixel_to_robot_coordinates(
    (u, v), 
    camera_height=48.8,
    z_obj = z_fom + z_obj, 
    gripper='2f85',
    robot_capturing_coord=np.array(Delta.read_forward())
)
z -= z_obj # if the height of your objects is short
# else z -= 2 or 3 cm

```
