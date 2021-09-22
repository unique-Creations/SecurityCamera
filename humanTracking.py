import tensorflow as tf
import tensorflow_hub as hub
import matplotlib as plt


# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
import cv2

# For measuring the inference time.
import time
import camera_stream