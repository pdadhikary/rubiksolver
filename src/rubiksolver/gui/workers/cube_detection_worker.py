import time

import cv2 as cv
import numpy as np
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QApplication

from rubiksolver.vision import (
    CubeDetectionParameters,
    CubeDetectionPipeline,
    CubeDetectionResult,
    FixedColorClassificationModel,
)


class CubeDectionWorker(QObject):
    dataReady = Signal(CubeDetectionResult)

    def __init__(self):
        super().__init__()
        self.running = False
        self.pausePipeline = False
        self.parameters = CubeDetectionParameters()
        self.pipeline = CubeDetectionPipeline(
            FixedColorClassificationModel(), self.parameters
        )

    def run(self):
        cap = cv.VideoCapture(0)

        if not cap.isOpened():
            print("Could not open Camera!")
            self.stop()

        self.running = True

        while self.running:
            ret, frame = cap.read()

            if not ret:
                print("Could not capture frame...")
                self.stop()
                break

            if self.pausePipeline:
                completeFrame = np.zeros_like(frame, dtype=np.uint8)
                result = CubeDetectionResult(
                    frame,
                    self.pipeline.getFinishedFrame(completeFrame),
                    0,
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                )
            else:
                self.pipeline.forward(frame)
                result = self.pipeline.result()

            self.dataReady.emit(result)
            QApplication.processEvents()
            time.sleep(0.033)

        cap.release()

    def stop(self):
        self.running = False

    def pause(self):
        self.pausePipeline = True

    def resume(self):
        self.pausePipeline = False

    @Slot(int)
    def setDenoiseDiameter(self, value: int) -> None:
        self.parameters.denoiseDiameter = value

    @Slot(int)
    def setDenoiseSigmaColor(self, value: int) -> None:
        self.parameters.denoiseSigmaColor = value

    @Slot(int)
    def setDenoiseSigmaSpace(self, value: int) -> None:
        self.parameters.denoiseSigmaSpace = value

    @Slot()
    def setCannyThreshold(self, value: tuple[int, int]) -> None:
        self.parameters.cannyLowerThreshold = value[0]
        self.parameters.cannyUpperThreshold = value[1]

    @Slot()
    def setFaceletAreaThreshold(self, value: tuple[int, int]) -> None:
        self.parameters.faceletAreaLowerThreshold = value[0]
        self.parameters.faceletAreaUpperThreshold = value[1]

    @Slot(int)
    def setFaceletContourAreaRatioThreshold(self, value: int) -> None:
        self.parameters.faceletCountourAreaRatioThreshold = value

    @Slot(int)
    def setFaceletBoundingBoxAspectRatioThreshold(self, value: int) -> None:
        self.parameters.faceletBoundingAspectRatioThreshold = value

    @Slot(int)
    def setHomographyRANSACMaxError(self, value: int) -> None:
        self.parameters.homographyRANSACMaxError = value
