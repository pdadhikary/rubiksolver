from os import path

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

path_to_npyfile = path.join(path.expanduser("~"), ".local", "share", "rubiksolver")
filename = "meancolors.npy"


def main():
    if not path.exists(path.join(path_to_npyfile, filename)):
        print(f"Calibration data not found. {filename} not found at {path_to_npyfile}")
        return

    colors = np.load(path.join(path_to_npyfile, filename)).astype(np.uint8)
    colors_HSV = np.expand_dims(colors, 0)
    colors_RGB = cv.cvtColor(colors_HSV, cv.COLOR_HSV2RGB)
    H, S, _ = cv.split(colors_HSV)

    plt.scatter(H, S, c=colors_RGB.squeeze() / 255)
    plt.xlabel("Hue")
    plt.ylabel("Saturation")

    plt.show()
