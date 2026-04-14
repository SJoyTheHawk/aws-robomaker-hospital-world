import os

import launch
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory('aws_robomaker_hospital_world')

    world_file_name = "hospital.world"
    world = os.path.join(pkg_share, 'worlds', world_file_name)

    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    # Point Gazebo Harmonic to the local model directories
    set_gz_resource_path = AppendEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=os.pathsep.join([
            os.path.join(pkg_share, 'models'),
            os.path.join(pkg_share, 'fuel_models'),
        ])
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': PythonExpression([
                '"' + world + ' -r" if "',
                LaunchConfiguration('gui'),
                '" == "true" else "' + world + ' -r -s"'
            ]),
        }.items()
    )

    return launch.LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value=world,
            description='SDF world file'
        ),
        DeclareLaunchArgument(
            name='gui',
            default_value='false'
        ),
        set_gz_resource_path,
        gz_sim,
    ])


if __name__ == '__main__':
    generate_launch_description()
