"""
Author: Ernesto Ruiz

"""
import camera
import frame_data as data
import numpy as np
import tensorflow as tf
import pin_controls as pins
import machine_learning
import os

from object_detection.utils import visualization_utils as vis_util

# Free up ram on Jetson Nano
os.system("watch -n 1 free -m")
cam = camera.Camera(isJetson=True)

label_map = machine_learning.get_label_map()
categories = machine_learning.get_categories()
category_index = machine_learning.get_category_idx()
detection_graph = machine_learning.get_detect_graph()
# gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.6)

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)


def main():
    with detection_graph.as_default():
        with tf.compat.v1.Session(graph=detection_graph) \
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

                # Actual detection.
                try:
                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                except TypeError:
                    cam.__del__()
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
                data.person_coordinates(scores, image, boxes, (cx, cy))
                print(f'Center: {cx, cy}')
                objects = data.get_categ_names(classes, scores, category_index)
                print(objects)
                # TODO: Get category names of all boxes in frame.
                print(data.person_counter(objects))
                # print(person_counter(score=scores, name=(category_index.keys()).get('name')), scores)
                if data.person_counter(objects) > 0:
                    pins.led_on()
                else:
                    pins.led_off()

                # cam.get_stream()
                if cam.get_key() & 0xFF == ord('q'):
                    break
    cam.__del__()
    pins.terminate()


if __name__ == "__main__":
    main()
