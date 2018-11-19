import cv2
import numpy as np


def getBoundingBoxOfImage(image):

    if image is None:
        return

    min_x = min_y = 0
    max_x = image.shape[0]
    max_y = image.shape[1]





def getSingleMaxBoundingBoxOfImage(image):
    """
    Calculate the coordinates(x, y, w, h) of single maximizing bounding rectangle boxing of grayscale image
    of character, in order to using this bounding box to select the region of character.
    :param image: grayscale image of character.
    :return: coordinates(x, y, w, h) of single maximizing bounding boxing.
    """
    if image is None:
        return None

    HEIGHT = image.shape[0]
    WIDTH = image.shape[1]

    # moments
    im2, contours, hierarchy = cv2.findContours(image, 1, 2)

    minx = WIDTH
    miny = HEIGHT
    maxx = 0
    maxy = 0
    # Bounding box
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        print(x, y, w, h)

        if w > 0.99 * WIDTH and h > 0.99 * HEIGHT:
            continue
        minx = min(x, minx)
        miny = min(y, miny)
        maxx = max(x + w, maxx)
        maxy = max(y + h, maxy)

    return minx, miny, maxx - minx, maxy - miny