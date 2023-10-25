import numpy as np
import math

# Let's do MATH!

def find_bbox_centroid(xmin, ymin, xmax, ymax):
    # find the centroid of a bounding box
    xcoord = (xmax+xmin)/2
    ycoord = (ymax+ymin)/2

    return xcoord, ycoord

def find_distance_bbox(b1xmin, b1ymin, b1xmax, b1ymax, b2xmin, b2ymin, b2xmax, b2ymax):
    # find the euclidean distance between the centroids of two bounding boxes
    b1_centroid = find_bbox_centroid(b1xmin, b1ymin, b1xmax, b1ymax)
    b2_centroid = find_bbox_centroid(b2xmin, b2ymin, b2xmax, b2ymax)
    euclid_distance = np.linalg.norm(b1_centroid-b2_centroid)

    return euclid_distance

def find_angle(p1x, p1y, p2x, p2y):
    # find the angle in degrees of a line between point 1 and point 2
    dx = p2x - p1x
    dy = p2y - p1y

    radians = math.atan2(dy, dx)
    degrees = np.rad2deg(radians)

    if 315 <= degrees < 360 or 0 <= degrees < 45:
        direction = 'above'
    if 45 <= degrees < 135:
        direction = 'to the right'
    if 135 <= degrees < 225:
        direction = 'below'
    if 225 <= degrees < 315:
        direction = 'to the left'

    return degrees, direction

def find_quadrant(image, x, y):
    # given an image and a point determine which part of the image the point is in
    # 123
    # 456
    # 789
    xmin = 0
    xmax = image.width - 1
    ymin = 0
    ymax = image.height - 1
    if xmax % 3 == 0:
        xhash1 = xmax/3
        xhash2 = xhash1*2
    else:
        xhash1 = (xmax-(xmax%3))/3
        xhash2 = xhash1*2
    if ymax %3 == 0:
        yhash1 = ymax/3
        yhash2 = yhash1*2
    else:
        yhash1 = (ymax-(ymax%3))/3
        yhash2 = yhash1*2
    if x < xhash1:
        xpos = 'left'
    if xhash1 <= x <= xhash2:
        xpos = 'middle'
    if xhash2 < x <= xmax:
        xpos = 'right'
    if y < yhash1:
        ypos = 'top'
    if yhash1 <= y <= yhash2:
        ypos = 'middle'
    if yhash2 < y < ymax:
        ypos = 'bottom'
    pos = ypos + ' ' + xpos
    if pos == 'middle middle':
        return 'center'
    else:
        return pos