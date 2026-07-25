import sys
import rclpy
from rclpy.executors import MultiThreadedExecutor

from .frontend.ihm_main_window import IHMWindow, QApplication
from .backend.ihm_node import IHMNode

from threading import Thread


def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)
    
    ihm_window: IHMWindow = IHMWindow()
    ihm_node: IHMNode = IHMNode(ihm_window)

    # Now we create a thread for the app, and let the ROS
    # node spin on the main thread
    executor = MultiThreadedExecutor()
    executor.add_node(ihm_node)

    thread = Thread(target=executor.spin)
    thread.start()
    ihm_node.get_logger().info("Spinning ROS node.")

    try:
        ihm_window.show()
        sys.exit(app.exec_())

    finally:
        ihm_node.get_logger().info("Shutting down ROS node.")
        ihm_node.destroy_node()
        executor.shutdown()

if __name__ == '__main__':
    main()