
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import SetEnvironmentVariable, DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch_ros.actions import Node

def generate_launch_description():

    robot_name = 'tb'
    robot_pos = {'x': '2', 'y': '1', 'z': '0',
                 'R': '0', 'P': '0', 'Y': '0'}
    
    robot_model_package_path = get_package_share_directory('turtlebot3_gazebo') # for robot state publisher
    robot_sdf = os.path.join(robot_model_package_path, 'models', 'turtlebot3_waffle', 'model.sdf')
    robot_urdf = os.path.join(robot_model_package_path, 'urdf', 'turtlebot3_waffle.urdf')

    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    remappings = [('/tf', 'tf'), ('/tf_static', 'tf_static')]


    
    with open(robot_urdf, 'r') as infp:
        robot_description = infp.read()

    start_robot_state_publisher_cmd = Node(
        #condition=IfCondition(use_robot_state_pub),
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        #namespace=namespace,
        output='screen',
        parameters=[{'use_sim_time': use_sim_time,
                     'robot_description': robot_description}],
        remappings=remappings
    )#remappings=remappings)
  
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )
    
    start_gazebo_spawner_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        arguments=[
            '-entity', robot_name,
            '-file', robot_sdf,
            #'-robot_namespace', namespace,
            '-x', robot_pos['x'], '-y', robot_pos['y'], '-z', robot_pos['z'],
            '-R', robot_pos['R'], '-P', robot_pos['P'], '-Y', robot_pos['Y']
        ])


    # Add the commands to the launch description
    ld = LaunchDescription()

    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(start_robot_state_publisher_cmd)
    #ld.add_action(joint_state_publisher_node)
    ld.add_action(start_gazebo_spawner_cmd)
    


    return ld