# AWS RoboMaker Hospital World — ROS Jazzy / Gazebo Harmonic Port

This package is forked from [aws-robotics/aws-robomaker-hospital-world](https://github.com/aws-robotics/aws-robomaker-hospital-world) (branch: `fix-floor-friction-ros2`).

It has been ported to **ROS 2 Jazzy** and **Gazebo Harmonic (Ignition Gazebo 8)**.

![Model: Hospital World](docs/images/hospital_world.jpg)

### Supported versions
| ROS | Gazebo |
|-----|--------|
| ROS 2 Jazzy | Gazebo Harmonic (Ignition Gazebo 8) |

> **Note:** `python3` and `python3-pip` are required to run this world. On Ubuntu 24.04 (PEP 668), `pip` must be invoked with `--break-system-packages` — this is handled automatically by `setup.sh` and `CMakeLists.txt`.

---

## Major changes from the original

### `setup.sh` and `CMakeLists.txt`
- Added `--break-system-packages` to `pip install` (Ubuntu 24.04 / PEP 668)

### `worlds/hospital.world`
- Added required Gazebo Harmonic world-level system plugins:
  - `ignition-gazebo-physics-system`
  - `ignition-gazebo-sensors-system` (with `ogre2` render engine)
  - `ignition-gazebo-scene-broadcaster-system`
  - `ignition-gazebo-user-commands-system`
  - `ignition-gazebo-log-system`
  - `ignition-gazebo-imu-system`

---

## 3D Models included in this Gazebo World

| Model (/models)       | Picture           |
| :------------- |:-------------:|
| **aws_robomaker_hospital_elevator_01_car, aws_robomaker_hospital_elevator_01_door, aws_robomaker_hospital_elevator_01_portal**     | ![Model: Elevator](docs/images/elevator.png) |
| **aws_robomaker_hospital_curtain_closed_01, aws_robomaker_hospital_curtain_half_open_01, aws_robomaker_hospital_curtain_open_01**     | ![Model: Curtains](docs/images/curtains.png) |
| **aws_robomaker_hospital_nursesstation_01**    | ![Model: Nurses Station](docs/images/nurses_station.png)
| **aws_robomaker_hospital_hospitalsign_01**    | ![Model: Hospital Sign](docs/images/hospital_sign.png)
| **aws_robomaker_hospital_floor_01_floor**    | ![Model: Hospital Floor](docs/images/hospital_floor.png)
| **aws_robomaker_hospital_floor_01_walls**    | ![Model: Hospital Walls and Layout](docs/images/hospital_walls.png)
| **aws_robomaker_hospital_floor_01_ceiling**    | ![Model: Ceiling](docs/images/hospital_ceiling.png)

We also reference the following models from https://app.ignitionrobotics.org/fuel/models:

*XRayMachine, IVStand, BloodPressureMonitor, BPCart, BMWCart, CGMClassic, StorageRack, Chair, InstrumentCart1, Scrubs, PatientWheelChair, WhiteChipChair, TrolleyBed, SurgicalTrolley, PotatoChipChair, VisitorKidSit, FemaleVisitorSit, AdjTable, MopCart3, MaleVisitorSit, Drawer, OfficeChairBlack, ElderLadyPatient, ElderMalePatient, InstrumentCart2, MetalCabinet, BedTable, BedsideTable, AnesthesiaMachine, TrolleyBedPatient, Shower, SurgicalTrolleyMed, StorageRackCovered, KitchenSink, Toilet, VendingMachine, ParkingTrolleyMin, PatientFSit, MaleVisitorOnPhone, FemaleVisitor, MalePatientBed, StorageRackCoverOpen, ParkingTrolleyMax*


# Setup

Download Fuel models and install Python dependencies:

```bash
chmod +x setup.sh
./setup.sh
```

# Building

```bash
rosdep install --from-paths . --ignore-src -r -y
colcon build --packages-select aws_robomaker_hospital_world
```

# ROS 2 Launch with Gazebo viewer (without a robot)

```bash
source install/setup.bash
ros2 launch aws_robomaker_hospital_world view_hospital.launch.py
```

# Include the world from another launch file

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    hospital_launch_path = os.path.join(
        get_package_share_directory('aws_robomaker_hospital_world'), 'launch')
    hospital_world_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([hospital_launch_path, '/hospital.launch.py'])
    )
    ld = LaunchDescription()
    ld.add_action(hospital_world_cmd)
    return ld
```

# Load directly into Gazebo Harmonic (without ROS 2)

```bash
chmod +x setup.sh
./setup.sh
export GZ_SIM_RESOURCE_PATH=$(pwd)/models:$(pwd)/fuel_models
gz sim worlds/hospital.world
```

