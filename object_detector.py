import cv2
import numpy as np
import tensorflow as tf
import pin_controls as pins
import machine_learning

from Tensorflow.models.research.object_detection.utils import visualization_utils as vis_util


# gstreamer_pipeline returns a GStreamer pipeline for capturing from camera
# Defaults to 1280x720 @ 30fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen


def gstreamer_pipeline(capture_width=3280, capture_height=2464, display_width=820, display_height=616, framerate=21,
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


cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

label_map = machine_learning.get_label_map()
categories = machine_learning.get_categories()
category_index = machine_learning.get_category_idx()
detection_graph = machine_learning.get_detect_graph()
# gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.6)

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)


def person_counter(obj_list):
    count = 0
    for obj in obj_list:
        if obj == 1:
            count += 1
    return count


def get_categ_names(classes, scores):
    objects = []
    threshold = 0.6
    for index, value in enumerate(classes[0]):
        if scores[0, index] > threshold:
            name = (category_index.get(value)).get('name')
            if name == 'person':
                objects.append(1)
            else:
                objects.append(0)
    return objects


def person_coordinates(score, image, boxes):
    # TODO: Check Accuracy of coordinates
    width, height = image.shape[:2]
    true_boxes = boxes[0][score[0] > .5]
    for i in range(true_boxes.shape[0]):
        y_min = true_boxes[i, 0] * height
        y_min = "{:.2f}".format(y_min)
        x_min = true_boxes[i, 1] * width
        x_min = "{:.2f}".format(x_min)
        y_max = true_boxes[i, 2] * height
        y_max = "{:.2f}".format(y_max)
        x_max = true_boxes[i, 3] * width
        x_max = "{:.2f}".format(x_max)

        print(f'Top left: {x_min, y_min}')
        print(f'Bottom right: {x_max, y_max}')


def main():
    with detection_graph.as_default():
        with tf.compat.v1.Session(graph=detection_graph) \
                as sess:
            while True:
                ret, image = cap.read()
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                # Actual detection.
                try:
                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                except TypeError:
                    cap.release()
                    print("TypeError: Capture released.")
                # Visualization of the results of a detection.
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=2)
                (h, w) = image.shape[:2]
                cx, cy = (w // 2, h // 2)
                person_coordinates(scores, image, boxes)
                print(f'Center: {cx, cy}')
                objects = get_categ_names(classes, scores)
                print(objects)
                # TODO: Get category names of all boxes in frame.
                print(person_counter(objects))
                # print(person_counter(score=scores, name=(category_index.keys()).get('name')), scores)
                if person_counter(objects) > 0:
                    pins.led_on()
                else:
                    pins.led_off()

                # cv2.imshow('object detection', cv2.resize(image, (900, 800)))
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    break


if __name__ == "__main__":
    main()
