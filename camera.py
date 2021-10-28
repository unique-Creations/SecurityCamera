"""
Author: Ernesto Ruiz

The camera class allows user to communicate with camera connected to the device. Currently compatible with
Apple devices and Jetson Nano.
"""
import cv2


def gstreamer_pipeline(capture_width=3280, capture_height=2464, display_width=820, display_height=616,
                       framerate=21,
                       flip_method=0):
    """gstreamer_pipeline returns a GStreamer pipeline for capturing from camera
    Defaults to 1280x720 @ 30fps
    Flip the image by setting the flip_method (most common values: 0 and 2)
    display_width and display_height determine the size of the window on the screen

    :param capture_width: Width of video captured by lens.
    :param capture_height: Height of video captured by lens.
    :param display_width: Width od visual display
    :param display_height: Height of visual display
    :param framerate: Frame rate of lens.
    :param flip_method: int value of video orientation. (0-2)
    :return: nvarguscamerasrc ! video/x-raw(memory:NVMM),
            width=(int)%d, height=(int)%d,
            format=(string)NV12, framerate=(fraction)%d/1 !
            nvvidconv flip-method=%d !
            video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx !
            videoconvert ! video/x-raw, format=(string)BGR ! appsink
    """

    return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
    )


class Camera:

    def __init__(self, isJetson=False):
        self.__isJetson = isJetson
        if isJetson:
            self.__stream = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
            print("------Jetson Nano camera initialized------")
        else:
            self.__stream = cv2.VideoCapture(0)

    def get_stream(self):
        return self.__stream.read()

    def display_stream(self, image):
        return cv2.imshow('object detection', cv2.resize(image, (900, 800)))

    def get_key(self, key=25):
        return cv2.waitKey(key)

    def __del__(self):
        """
        Camera Destructor

        - Release VideoCapture
        - Destroy all cv2 windows
        """
        if self.__isJetson:
            self.__stream.release()
        cv2.destroyAllWindows()
        print("------Camera deleted------")
