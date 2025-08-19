from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():

    xacro_path = "nav2_mobile_robot.xacro"

    robot_description = PathJoinSubstitution(
        [get_package_share_directory("nav2_mobile_robot"), xacro_path]
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": Command(["xacro ", robot_description])}],
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        output="screen",
        parameters=[{"robot_description": Command(["xacro ", robot_description])}],
    )

    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name",
            "diff_drive",
            "-x",
            "0",
            "-y",
            "0",
            "-z",
            "0.1",
            "-r",
            "0",
            "-p",
            "0",
            "-Y",
            "0",
            "-topic",
            "/robot_description",
        ],
        output="screen",
    )

    pkg_nav2_mobile_robot = get_package_share_directory("nav2_mobile_robot")
    gz_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH", value=[os.path.join(pkg_nav2_mobile_robot)]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
                )
            ]
        ),
        launch_arguments=[("gz_args", [" -r -v 4 maze.sdf"])],
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "lidar@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan",
            "/lidar/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked",
            "/odom/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V",
            "cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist",
            "/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model",
            "/model/diff_drive/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry",
        ],
        output="screen",
        remappings=[
            ("/model/diff_drive/odometry", "/odom"),
            ("/odom/tf", "/tf"),
        ],
    )

    rviz_file = "rviz.rviz"
    rviz_path = PathJoinSubstitution(
        [get_package_share_directory("nav2_mobile_robot"), rviz_file]
    )

    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_path],
    )

    return LaunchDescription(
        [
            gz_resource_path,
            robot_state_publisher_node,
            spawn,
            gazebo,
            bridge,
            rviz2_node,
        ]
    )
