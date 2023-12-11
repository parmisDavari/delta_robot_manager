# delta_robot_manager

## To use Delta and Gripper commands follow these instructions:

# import these libraries...

from delta_manager.delta_manager import DeltaManager

# Use the library using this line...

Delta = DeltaManager()

## Commands you can use:

# To use Gripper connect to it using its USB cable and turn its power on then...
# Use this line to connect to the Gripper 
Delta.connect_gripper()

## Gripper functions:

Delta.open_gripper()
Delta.open_gripper_aBit()
Delta.close_gripper()
Delta.close_gripper_with_feedback()
# returns the result of Grasping: "DoneGrasp" or "failed"
Delta.rotate_gripper(angle):
# On degree -90:90 (its ralative to the current angle)
Delta.force_gripper(force):
# int from 1 to 5000 
## un comment and ask Navid Asadi if you want to use. 
Delta.wait_till_done()

## Delta Parallel Robot(DPR) functions

Delta.go_home()
Delta.move(x, y, z)
# goes in 8 secs
Delta.move_with_time(x, y, z, t)
# Dont use times less than 3 seconds ask Navid Pasiar or Arvin Mohammadi if you want.
Delta.wait_till_done_robot()
x,y,z = Delta.read_forward()
Delta.delta_stop_server()

