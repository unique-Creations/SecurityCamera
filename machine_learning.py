import tensorflow as tf
import os
import six.moves.urllib as urllib
import tarfile

from Tensorflow.models.research.object_detection.utils import label_map_util

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


def get_detect_graph():
    graph = tf.Graph()
    with graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    return graph


def get_label_map():
    return label_map_util.load_labelmap(PATH_TO_LABELS)


def get_categories():
    return label_map_util.convert_label_map_to_categories(get_label_map(),
                                                          max_num_classes=NUM_CLASSES,
                                                          use_display_name=True)


def get_category_idx():
    return label_map_util.create_category_index(get_categories())



