# SecurityCamera
## Introduction
The auto-tracking security system consists of a camera and security light which detects movement and
centers the camera and light onto a human shaped object. Security lights on the system are then activated 
and the camera/lights tracks the person keeping them centered in both peripherals.

## Getting Started

### Jetson Nano Setup
To begin, please follow steps for installing OpenCV 4.5 on the Jetson Nano, which are provided 
[here](https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html).

```commandline
pip install -r requirements.txt
```
Packages installed:  

| Package  | Version  |
|---       |---       |
|  Python  |  3.9.7   |
|  Tensorflow | 2.5.0 |
| Opencv-python  | 4.5.3.56  |
|  Numpy   | 1.20.3   |
|  Pillow  | 8.3.2    |
|  Jupyterlab | 3.1.12|

### GPIO pin configuration

| Direction  | Enable Pin  | Step Pin  |
|---         |---          |---        |
|Left | 12  |  11 |
|Right| 15  |  13 |
|Up   | 31  |  32 |
|Down | 19  |  21 |
| LED | 7   | -






