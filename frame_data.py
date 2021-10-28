# TODO: finish implementation
# cv2 for debugging
from cv2 import circle


def person_counter(obj_list):
    count = 0
    for obj in obj_list:
        if obj == 1:
            count += 1
    return count


def get_categ_names(classes, scores, cat_idx):
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


def person_coordinates(score, image, boxes):
    # TODO: Associate coordinates with object
    # TODO: Get center coordinate of box
    # TODO: get accurate center coordinate
    width, height = image.shape[:2]
    true_boxes = boxes[0][score[0] > .5]
    for i in range(true_boxes.shape[0]):
        y_min = true_boxes[i, 0] * height
        x_min = true_boxes[i, 1] * width
        y_max = true_boxes[i, 2] * height
        x_max = true_boxes[i, 3] * width
        box_width = x_max - x_min
        box_height = y_max - y_min
        cx, cy = (int(box_width // 2), int(box_height // 2))
        circle(image, (cx, cy), 7, (255, 255, 255), -1)