import cv2


def gstreamer_pipeline(capture_width=3280, capture_height=2464, display_width=820, display_height=616,
                       framerate=21,
                       flip_method=0):
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
    stream = None
    isJetson = False

    def __init__(self, isJetson=False):
        self.isJetson = isJetson
        if isJetson:
            self.stream = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
            print("------Jetson Nano camera initialized------")
        else:
            self.stream = cv2.VideoCapture(0)

    def get_stream(self):
        return self.stream.read()

    def display_stream(self, image):
        return cv2.imshow('object detection', cv2.resize(image, (900, 800)))

    def get_key(self, key=25):
        return cv2.waitKey(key)

    def __del__(self):
        if self.isJetson:
            self.stream.release()
        cv2.destroyAllWindows()
        print("------Camera deleted------")
