import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class ColorPubNode(Node):
    def __init__(self):
        super().__init__('color_publisher')
        self.publisher_ = self.create_publisher(Image, 'image_raw', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.cap = cv2.VideoCapture('/home/lee/ros2_projects/color_tracking/test/test_images/redball.mp4')
        self.br = CvBridge()

    def timer_callback(self):
        if not self.cap.isOpened():
            self.get_logger().warn("VideoCapture not opened. Trying to reinitialize...")
            self.cap.open('/home/lee/ros2_projects/color_tracking/test/test_images/redball.mp4')

        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warn('Cannot read frame. Rewinding...')
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return


        # Convert frame to HSV for color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define red color range (in two parts in HSV space)
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        # Create masks for red areas
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Denoise mask
        mask = cv2.medianBlur(mask, 5)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Select the largest contour assuming it's the ball
            largest = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(largest)
            center = (int(x), int(y))
            radius = int(radius)

            if radius > 5:
                # Draw tracking circle and center dot
                cv2.circle(frame, center, radius, (0, 255, 0), 2)
                cv2.circle(frame, center, 3, (255, 0, 0), -1)

        # Convert to ROS Image message and publish
        img_msg = self.br.cv2_to_imgmsg(frame, "bgr8")
        self.publisher_.publish(img_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ColorPubNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
