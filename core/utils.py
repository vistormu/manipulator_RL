import numpy as np
import os
import shutil


def to_radians(angle) -> float:
    return angle*np.pi / 180


def to_degrees(angle) -> float:
    return angle*180 / np.pi


def delete_files(path: str) -> None:
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def normalize(value, min_value, max_value):
    normalized_value = value/(max_value - min_value)

    return normalized_value
