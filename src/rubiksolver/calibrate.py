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

    # plt.scatter(H, S, c=colors_RGB.squeeze() / 255)
    # plt.xlabel("Hue")
    # plt.ylabel("Saturation")

    fig = plt.figure()
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122, projection="polar")

    ax1.scatter(H, S, c=colors_RGB.squeeze() / 255)
    ax1.set_xlabel("Hue")
    ax1.set_ylabel("Saturation")

    ax2.set_rmax(255)
    ax2.set_thetamin(0)
    ax2.set_rticks([0, 50, 100, 150, 200, 250])
    ax2.set_thetagrids(np.arange(0, 360, 45), np.round(np.linspace(0, 180, 9)[:-1], 1))
    ax2.set_rlabel_position(0)
    ax2.scatter((H * np.pi) / 90, S, c=colors_RGB.squeeze() / 255)

    fig.suptitle("Average Hue vs Saturation of Detected Facelets")

    plt.show()
