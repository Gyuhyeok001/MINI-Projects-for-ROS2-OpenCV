import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')
        self.publisher_ = self.create_publisher(Image, '/image_raw', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)  # 1Hz
        self.bridge = CvBridge()
        self.image_path = os.path.expanduser('~/test_image.jpg')

    def timer_callback(self):
        img = cv2.imread(self.image_path)
        if img is None:
            self.get_logger().error('Image not found at {}'.format(self.image_path))
            return
        msg = self.bridge.cv2_to_imgmsg(img, encoding='bgr8')
        self.publisher_.publish(msg)
        self.get_logger().info('📤 Published test image')

def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()