# Rubiksolver

https://github.com/user-attachments/assets/437902a8-08ce-4c79-a4a9-40c0c7fcf09c

▶️ [Watch the Demo on YouTube](https://www.youtube.com/watch?v=abj7ubu9g8o)

______________________________________________________________________

## Description

**Rubiksolver** is a simple GUI-based computer vision application that detects
and solves a Rubik’s Cube in real time.

______________________________________________________________________

## Computer Vision Pipeline

I use **Canny edge detection** to extract individual facelets from the video frame.
To reliably distinguish cube facelets from background objects, the program only
accepts contours that meet specific **aspect-ratio** and **size thresholds**,
which are adjustable from the GUI.

To further eliminate erroneous facelet candidates, I project the candidates onto
a grid and select those with the lowest error after **100 RANSAC iterations**.

Finally, to correctly label each facelet by its face color, I use the **aggregate
mean hue and saturation** of its pixels to classify colors. I found this model
to be fairly robust and invariant to lighting changes compared to RGB-based approaches.

![Color Calibration Image](./images/calibration.png)

The figure above shows the aggregate mean hue and saturation of each facelet’s
pixels across multiple runs under different lighting conditions.
As you can see, a very simple thresholding model suffices to classify each
facelet by color.

______________________________________________________________________

## Installation

To run the app, you’ll need to have [`uv`](https://docs.astral.sh/uv/)
installed on your system.
If you don’t already have it, follow the
[installation instructions here](https://docs.astral.sh/uv/getting-started/installation/).

```bash
git clone https://github.com/pdadhikary/rubiksolver.git
cd rubiksolver
uv sync
```

The above commands will clone the repository and install all required
dependencies in a virtual Python environment.
Once setup is complete, you can start the program with:

```bash
uv run rubiksolver
```

## Usage

When scanning their Rubik's cube the user should hold up each face of the cube
to the webcam. By convention we assume that the white face is UP and the yellow
face is DOWN. When scanning the white face, the red face is DOWN and it should
be UP when scanning the yellow face.

Once the scan is complete press the `Play` button to animate the solution steps.
You can also step through each of the moves using the `Previous` and `Next` buttons.

### Control Panel Sliders

```text
- Denoise Filter Diameter                           Size of the denoise filter kernel.


- Color Filter Sigma                                The colorSigma parameter for the
                                                    bilateral filter.

                                                    A larger value means more smoothing
                                                    of the image as pixels with more
                                                    different color values are averaged
                                                    together. A smaller value correlates
                                                    to less smoothing and edges are better
                                                    preserved.


- Space Filter Sigma                                The spaceSigma parameter of the
                                                    bilateral filter.

                                                    A larger value means more smoothing as
                                                    a wider neighbourhood of pixels is
                                                    considered. Whereas a smaller value
                                                    give a more localized smoothing.


- Canny Threshold                                   The upper and lower thershold for the
                                                    Canny edge detection hysteresis step.

                                                    Lower values correspond to the weaker
                                                    edges present in the image and higher
                                                    values represent more pronounced edges.


- Facelet Area Threshold                            Size thershold of candidate facelets
                                                    contours.

                                                    This option can be used to eliminate
                                                    erroneous contours from the background
                                                    by eliminating contours that are either
                                                    too small or too large. The size is the
                                                    percentage of screen space.


- Facelet Contour Area Ratio Threshold              The width to height ratio of contours
                                                    to consider as candidates.

                                                    This value can be changed to elimate
                                                    contours that are not square-ish.


- Facelet Bounding Box Aspect Ratio Threshold       Metric for how well the contour
                                                    fits/occupies the bounding box.

                                                    This can be changed to allow for
                                                    facelets that are not perfectly square,
                                                    i.e, may have rounded edges or are
                                                    circular.


- RANSAC Error Threshold                            Metrix for how well the detected
                                                    contours fit in a 3x3 grid.

                                                    Used to filter out outlier/erroneous
                                                    contours that may be present in the
                                                    background.
```
