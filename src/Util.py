import math
from datetime import datetime


def get_distance(x1, y1, x2, y2):
    headingX = x2 - x1
    headingY = y2 - y1
    return math.sqrt((headingX * headingX) + (headingY * headingY))


def get_diff(target_time):
    diff = datetime.now() - target_time
    return diff.total_seconds() * 1e+6 + diff.microseconds


def is_uptodate(target_time):
    return get_diff(target_time) < 1e+6
