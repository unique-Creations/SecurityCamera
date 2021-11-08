"""
Author: Ernesto Ruiz

object_detector_test is used to test code on MacBook Pro M1 before pushing to Jetson Nano.
"""
import numpy as np
import tensorflow as tf
import os, psutil
import machine_learning
import frame_data
import camera

from object_detection.utils import visualization_utils as vis_util

# Initialize camera class
cam = camera.Camera(isJetson=False)

label_map = machine_learning.get_label_map()
categories = machine_learning.get_categories()
category_index = machine_learning.get_category_idx()
detection_graph = machine_learning.get_detect_graph()

gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.5)
gpus = tf.config.list_physical_devices('GPU')

if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
# To determine the amount of RAM consumption
process = psutil.Process(os.getpid())


def main():
    with detection_graph.as_default():
        with tf.compat.v1.Session(graph=detection_graph, config=tf.compat.v1.ConfigProto(gpu_options=gpu_options)) \
                as sess:
            while True:
                ret, image = cam.get_stream()
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

                # run detection.
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

                frame_data.person_coordinates(scores, image, boxes, (cx, cy))
                print(f'Center: {cx, cy}')

                objects = frame_data.get_categ_names(classes, scores, category_index)
                print(objects)
                print(frame_data.person_counter(objects))

                # Determine RAM Usage as percentage.
                ram_usage = (process.memory_info().rss / psutil.virtual_memory().total) * 100
                print(f'RAM USAGE: {ram_usage}')
                cam.display_stream(image)
                if cam.get_key() & 0xFF == ord('q'):
                    cam.__del__()
                    break


if __name__ == "__main__":
    main()
