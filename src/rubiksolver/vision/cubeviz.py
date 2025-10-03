import cv2 as cv
from cv2.typing import MatLike

from rubiksolver.cube import CubeFace, CubeLabel, CubePositon, Facelet, RubiksCube

from .vision import CubeDetectionResult


class PlanarCubeVisualizer:
    ColorMap: dict[CubeLabel, tuple[int, int, int]] = {
        CubeLabel.UP: (255, 255, 255),
        CubeLabel.RIGHT: (255, 200, 15),
        CubeLabel.FRONT: (95, 60, 255),
        CubeLabel.DOWN: (70, 255, 255),
        CubeLabel.LEFT: (90, 255, 150),
        CubeLabel.BACK: (32, 114, 243),
        CubeLabel.UNLABELD: (0, 0, 0),
    }

    LabelMap: dict[CubeLabel, str] = {
        CubeLabel.UP: "White",
        CubeLabel.RIGHT: "Blue",
        CubeLabel.FRONT: "Red",
        CubeLabel.DOWN: "Yellow",
        CubeLabel.LEFT: "Green",
        CubeLabel.BACK: "Orange",
        CubeLabel.UNLABELD: "???",
    }

    def __init__(
        self,
        colorMap: dict[CubeLabel, tuple[int, int, int]] | None = None,
        labelMap: dict[CubeLabel, str] | None = None,
        padX: int = 20,
        padY: int = 20,
        faceletSize: int = 10,
        faceGutter: int = 5,
        faceMargin: int = 5,
    ):
        if colorMap is None:
            self.colorMap = PlanarCubeVisualizer.ColorMap
        else:
            self.colorMap = colorMap

        if labelMap is None:
            self.labelMap = PlanarCubeVisualizer.LabelMap
        else:
            self.labelMap = labelMap

        self.padX = padX
        self.padY = padY
        self.faceletSize = faceletSize
        self.faceGutter = faceGutter
        self.faceMargin = faceMargin

        self.faceSize = 3 * (self.faceletSize + self.faceGutter) + self.faceMargin
        self.faceMap: dict[CubeFace, tuple[int, int]] = {
            CubeFace.UP: (self.padX + self.faceSize, self.padY),
            CubeFace.RIGHT: (
                self.padX + (2 * self.faceSize),
                self.padY + self.faceSize,
            ),
            CubeFace.FRONT: (
                self.padX + self.faceSize,
                self.padY + self.faceSize,
            ),
            CubeFace.DOWN: (
                self.padX + self.faceSize,
                self.padY + (2 * self.faceSize),
            ),
            CubeFace.LEFT: (self.padX, self.padY + self.faceSize),
            CubeFace.BACK: (
                self.padX + (3 * self.faceSize),
                self.padY + self.faceSize,
            ),
        }

    def visualize(self, frame: MatLike, cube: RubiksCube) -> MatLike:
        for face in CubeFace:
            topX, topY = self.faceMap[face]
            for r in range(3):
                startY = topY + r * (self.faceletSize + self.faceGutter)
                for c in range(3):
                    startX = topX + c * (self.faceletSize + self.faceGutter)
                    color = self.colorMap[
                        cube.getFaceletLabel(Facelet(face, CubePositon(r * 3 + c)))
                    ]
                    frame = cv.rectangle(
                        frame,
                        (startX, startY, self.faceletSize, self.faceletSize),
                        color,
                        cv.FILLED,
                    )

        return frame

    def highlight(self, frame: MatLike, result: CubeDetectionResult) -> MatLike:
        cv.drawContours(
            frame,
            result.facelet_contour_rotated_bb_points,
            -1,
            (255, 255, 255),
            3,
        )

        for label, rect in zip(
            result.labels,
            result.facelet_contour_bb,
        ):
            text = self.labelMap[label]
            font = cv.FONT_HERSHEY_SIMPLEX
            scale = 0.4

            (text_width, text_height), _ = cv.getTextSize(text, font, scale, 1)
            x, y, _, _ = rect
            padding = 3

            frame = cv.rectangle(
                frame,
                (
                    x - padding,
                    y - text_height - (2 * padding),
                    text_width + (2 * padding),
                    text_height + (2 * padding),
                ),
                (255, 255, 255),
                cv.FILLED,
            )

            frame = cv.putText(frame, text, (x, y - padding), font, scale, (0, 0, 0))

        return frame
