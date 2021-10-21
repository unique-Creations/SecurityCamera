'''
Title:
Author:
Date:
Code version:
Availability: https://pythonprogramming.net/video-tensorflow-object-detection-api-tutorial/
'''
import numpy as np
import os
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
import cv2

cap = cv2.VideoCapture(0)

from Tensorflow.models.research.object_detection.utils import label_map_util
from Tensorflow.models.research.object_detection.utils import visualization_utils as vis_util

MODEL_NAME = 'ssd_mobilenet_v1_coco_2018_01_28'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

PATH_TO_LABELS = os.path.join('Tensorflow/models/research/object_detection/data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():

    file_name = os.path.basename(file.name)
    if 'frozen_inference_graph.pb' in file_name:
        tar_file.extract(file, os.getcwd())

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def person_counter(score, name):
    final_score = np.squeeze(score)
    count = 0
    for i in range(100):
        if name == 'person':
            if scores is None or final_score[i] > 0.5:
                count = count + 1
    return count


def person_coordinates(score, image):
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


# # Detection
with detection_graph.as_default():
    with tf.compat.v1.Session(graph=detection_graph) as sess:
        while True:
            ret, image_np = cap.read()
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
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
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=2)
            person_coordinates(scores, image_np_expanded)
            # TODO: Get category names of all boxes in frame.
            print(person_counter(score=scores, name=(category_index.get(1)).get('name')))
            cv2.imshow('object detection', cv2.resize(image_np, (900, 800)))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
