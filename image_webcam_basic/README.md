# image_webcam_basic
ROS2 + OpenCV // Practice Project 

---

## Features

- `image_pub_node`: Publishes a fixed image (`test_image.jpg`) repeatedly to the `/image_raw` topic
- `image_sub_node`: Subscribes to `/image_raw`, converts the image to grayscale using OpenCV, and displays it

---

## Environment

- Ubuntu 22.04  
- ROS2 Humble  
- Python 3.10  
- OpenCV + cv_bridge  
- VS Code (optional)  

---

## How to Run

### 1. Build the ROS2 workspace
cd ~/ros2_ws
colcon build
source install/setup.bash

---

Result Preview

