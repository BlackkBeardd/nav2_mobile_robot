from setuptools import find_packages, setup

package_name = "nav2_mobile_robot"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            "share/" + package_name,
            [
                "launch/display.launch.py",
                "launch/gazebo.launch.py",
                "launch/slam.launch.py",
                "urdf/nav2_mobile_robot.xacro",
                "urdf/gazebo_control.xacro",
                "urdf/lidar.xacro",
                "urdf/nav2_mobile_robot_macro.xacro",
                "urdf/odom_plugin.xacro",
                "rviz/rviz.rviz",
                "worlds/maze.sdf",
                "config/slam.yaml",
            ],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="blackbeard",
    maintainer_email="abubakarmughal92@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [],
    },
)
