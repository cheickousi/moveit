import rospy
from sensor_msgs.msg import Joy
from xarm.wrapper import XArmAPI

# Global variable to store the latest joystick state
latest_joy_msg = None

# Initialize the xArm API
arm = XArmAPI('192.168.1.1')  # Replace with your xArm's IP address
arm.motion_enable(enable=True)
arm.set_mode(1)
arm.set_state(state=0)


def joy_callback(msg):
    global latest_joy_msg
    latest_joy_msg = msg

    # Control the xArm based on the joystick input
    angles = [msg.axes[0] * 100, 0, 0, 0, 0, 0, 0]
    arm.set_servo_angle_j(angles)


def main():
    global latest_joy_msg

    # Initialize the ROS node
    rospy.init_node('xarm5_teleop')

    # Subscribe to the joystick topic
    rospy.Subscriber('joy', Joy, joy_callback)

    # Create a rate limiter
    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        # If we haven't received a joystick message yet, skip this iteration
        if latest_joy_msg is None:
            continue

        # Sleep to maintain the desired rate
        rate.sleep()


if __name__ == '__main__':
    main()
