import numpy as np
import tensorflow as tf

# Change to object_detector.py for Jetson Nano
import webcam_test_mac
import machine_learning

from Tensorflow.models.research.object_detection.utils import visualization_utils as vis_util

# Change to object_detector.py for Jetson Nano
cap = webcam_test_mac.camera_stream()

label_map = machine_learning.get_label_map()
categories = machine_learning.get_categories()
category_index = machine_learning.get_category_idx()
detection_graph = machine_learning.get_detect_graph()


def person_counter(score, name, scores):
    final_score = np.squeeze(score)
    count = 0
    for i in range(100):
        if name == 'person':
            if scores is None or final_score[i] > 0.5:
                count = count + 1
    return count


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
        with tf.compat.v1.Session(graph=detection_graph) as sess:
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
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
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
                # TODO: Get category names of all boxes in frame.
                # print(person_counter(score=scores, name=(category_index.keys()).get('name')), scores)
                webcam_test_mac.cv2.imshow('object detection', webcam_test_mac.cv2.resize(image, (900, 800)))
                if webcam_test_mac.cv2.waitKey(25) & 0xFF == ord('q'):
                    webcam_test_mac.cv2.destroyAllWindows()
                    break


if __name__ == "__main__":
    main()