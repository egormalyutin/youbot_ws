from os.path import join

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_youbot_gz = get_package_share_directory("youbot_gazebo")
    pkg_youbot_description = get_package_share_directory("youbot_description")
    # pkg_youbot_moveit2 = get_package_share_directory("youbot_moveit2")
    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")

    world = join(pkg_youbot_gz, "worlds", "playground.sdf")

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")
        ),
        # launch_arguments={"gz_args": f"-r gpu_lidar_sensor.sdf"}.items(),
        # launch_arguments={"gz_args": f"-r empty.sdf"}.items(),
        launch_arguments={"gz_args": f"-r {world}"}.items(),
        # launch_arguments={"gz_args": f"-r empty.sdf"}.items(),
    )

    description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            join(pkg_youbot_description, "launch", "youbot_description.launch.py")
        ),
        launch_arguments={"use_sim_time": "true"}.items(),
    )

    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        # arguments=[
        #     "-d",
        #     join(pkg_bringup, "config", "diff_drive.rviz"),
        # ],
        # condition=IfCondition(LaunchConfiguration("rviz")),
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[
            {
                "config_file": join(pkg_youbot_gz, "config", "ros_gz_bridge.yaml"),
                "qos_overrides./tf_static.publisher.durability": "transient_local",
            }
        ],
        output="screen",
    )

    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name",
            "robot",
            "-topic",
            "robot_description",
            "-x",
            "0.0",
            "-y",
            "1.0",
            "-z",
            "0.5",
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "rviz", default_value="true", description="Open RViz."
            ),
            gz_sim,
            # bridge,
            # publisher,
            # rviz,
            spawn,
            description,
            bridge,
            rviz2,
        ]
    )
