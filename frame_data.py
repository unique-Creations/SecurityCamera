# cv2 for debugging
from cv2 import circle


def person_counter(obj_list):
    """
    Counts the number of persons detected within the frame.

    :param obj_list: array of objects detected as integers (1 or 0).
    :return: number of persons detected in the frame
    """
    count = 0
    for obj in obj_list:
        if obj == 1:
            count += 1
    return count


def get_categ_names(classes, scores, cat_idx):
    """
    Uses object names detect by TensorFlow and returns an int array to distinguish person from other objects.

    :param classes: array of classes detected
    :param scores: score of classes detected
    :param cat_idx: indexes of classes detected
    :return: array of objects detected. 1 if person, else 0
    """
    objects = []
    threshold = 0.6
    for index, value in enumerate(classes[0]):
        if scores[0, index] > threshold:
            name = (cat_idx.get(value)).get('name')
            if name == 'person':
                objects.append(1)
            else:
                objects.append(0)
    return objects


def person_coordinates(score, image, boxes, center: (float, float)):
    """
    Calculates center coordinates of the person boxes within the frame.

    :param score: array of category scores
    :param image: frame read from camera
    :param boxes: 2D matrix of object boxes detected
    :param center: center coordinates of frame
    :return: center coordinate of person boxes or center coordinate if 0 objects present
    """
    height, width = image.shape[:2]
    true_boxes = boxes[0][score[0] > .5]
    if len(true_boxes) > 0:
        for i in range(true_boxes.shape[0]):
            y_min = true_boxes[i, 0] * height
            x_min = true_boxes[i, 1] * width
            y_max = true_boxes[i, 2] * height
            x_max = true_boxes[i, 3] * width
            box_width = x_max - x_min
            box_height = y_max - y_min

            if box_height == box_width:
                cx, cy = (int(box_width // 2), int(box_height // 2))
            else:
                cx, cy = (int((x_max + y_min) / 2), int((y_max + x_min) / 2))

            # For debugging purposes
            # Comment out on Jetson Nano
            circle(image, (cx, cy), 6, (255, 0, 0), 2)
            return cx, cy
    return center
