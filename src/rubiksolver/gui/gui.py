from os import makedirs, path

import cv2 as cv
import numpy as np
from PySide6.QtCore import QSize, QThread, Signal, Slot
from PySide6.QtGui import QImage, QPixmap, Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QMainWindow, QSizePolicy, QWidget

from rubiksolver.cube import (
    CubeFace,
    CubeLabel,
    CubePosition,
    Facelet,
    MoveTimeline,
    RubiksCube,
)
from rubiksolver.vision import CubeDetectionResult, PlanarCubeVisualizer
from rubiksolver.vision.vision import HSV

from .widgets import Cube3DViewerWidget, CubeDetectionControlPanel
from .workers import CubeDectionWorker


class CubeDetectionAppWindow(QMainWindow):
    PauseSignal = Signal()
    ResumeSignal = Signal()

    def __init__(self):
        super().__init__()
        self.cube = RubiksCube()
        self.visualizer = PlanarCubeVisualizer()
        self.videoSize = QSize(752, 450)
        self.cubeDetectionThread = QThread()
        self.detectionStarted = False
        self.cubeDetectionWorker = CubeDectionWorker()
        self.animTimeline: MoveTimeline | None = None
        self.setup()

        self.cubeDetectionWorker.moveToThread(self.cubeDetectionThread)
        self.cubeDetectionWorker.dataReady.connect(self.showResults)
        self.cubeDetectionThread.started.connect(self.cubeDetectionWorker.run)
        self.PauseSignal.connect(self.cubeDetectionWorker.pause)
        self.ResumeSignal.connect(self.cubeDetectionWorker.resume)

    def setup(self):
        self.photoLabel1 = QLabel()
        self.photoLabel1.setMinimumSize(self.videoSize)
        self.photoLabel1.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.photoLabel2 = QLabel()
        self.photoLabel2.setMinimumSize(self.videoSize)
        self.photoLabel2.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.controlPanel = CubeDetectionControlPanel()

        self.cubeViewer = Cube3DViewerWidget()

        self.controlPanel.denoiseDiameter_slider.setValue(
            self.cubeDetectionWorker.parameters._denoiseDiameter
        )
        self.controlPanel.denoiseDiameter_slider.valueChanged.connect(
            self.cubeDetectionWorker.setDenoiseDiameter
        )

        self.controlPanel.denoiseSigmaColor_slider.setValue(
            self.cubeDetectionWorker.parameters._denoiseSigmaColor
        )
        self.controlPanel.denoiseSigmaColor_slider.valueChanged.connect(
            self.cubeDetectionWorker.setDenoiseSigmaColor
        )

        self.controlPanel.denoiseSigmaSpace_slider.setValue(
            self.cubeDetectionWorker.parameters._denoiseSigmaSpace
        )
        self.controlPanel.denoiseSigmaSpace_slider.valueChanged.connect(
            self.cubeDetectionWorker.setDenoiseSigmaSpace
        )

        self.controlPanel.cannyThreshold_slider.setValue(
            (
                self.cubeDetectionWorker.parameters._cannyLowerThreshold,
                self.cubeDetectionWorker.parameters._cannyUpperThreshold,
            )
        )
        self.controlPanel.cannyThreshold_slider.valueChanged.connect(
            self.cubeDetectionWorker.setCannyThreshold
        )

        self.controlPanel.faceletAreaThreshold_slider.setValue(
            (
                self.cubeDetectionWorker.parameters._faceletAreaLowerThreshold,
                self.cubeDetectionWorker.parameters._faceletAreaUpperThreshold,
            )
        )
        self.controlPanel.faceletAreaThreshold_slider.valueChanged.connect(
            self.cubeDetectionWorker.setFaceletAreaThreshold
        )

        self.controlPanel.faceletContourAreaRatioThreshold_slider.setValue(
            self.cubeDetectionWorker.parameters._faceletContourAreaRatioThreshold
        )
        self.controlPanel.faceletContourAreaRatioThreshold_slider.valueChanged.connect(
            self.cubeDetectionWorker.setFaceletContourAreaRatioThreshold
        )

        self.controlPanel.faceletBoundingBoxAspectRatioThreshold_slider.setValue(
            self.cubeDetectionWorker.parameters._faceletBoundingBoxAspectRatioThreshold
        )
        self.controlPanel.faceletBoundingBoxAspectRatioThreshold_slider.valueChanged.connect(
            self.cubeDetectionWorker.setFaceletBoundingBoxAspectRatioThreshold
        )

        self.controlPanel.homographyRASACMaxError_slider.setValue(
            self.cubeDetectionWorker.parameters._homographyRANSACMaxError
        )
        self.controlPanel.homographyRASACMaxError_slider.valueChanged.connect(
            self.cubeDetectionWorker.setHomographyRANSACMaxError
        )

        self.cubeViewer.playButton.pressed.connect(self.playPressed)
        self.cubeViewer.nextButton.pressed.connect(self.nextPressed)
        self.cubeViewer.prevButton.pressed.connect(self.prevPressed)
        self.cubeViewer.resetButton.pressed.connect(self.resetPressed)

        container = QWidget(self)
        self.setCentralWidget(container)
        layout = QGridLayout(container)

        layout.addWidget(self.photoLabel1, 0, 0)
        layout.addWidget(self.cubeViewer, 0, 1)
        layout.addWidget(self.photoLabel2, 1, 0)
        layout.addWidget(self.controlPanel, 1, 1)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.detectionStarted:
            self.cubeDetectionThread.start()
            self.detectionStarted = True

    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        print("Stoping Threads and Workers...")
        self.cubeDetectionWorker.stop()
        self.cubeDetectionThread.quit()
        self.cubeDetectionThread.wait()
        self.detectionStarted = False

        self.cubeViewer.cleanup()
        event.accept()

    def showResults(self, result: CubeDetectionResult):
        self.updateCube(result)
        self.cubeViewer.cubeWidget.setCubeLabels(self.cube.state)
        frame = self.visualizer.visualize(result.frame, self.cube)
        frame = self.visualizer.highlight(frame, result)
        frame = cv.cvtColor(result.frame, cv.COLOR_BGR2RGB)
        edges = result.edges

        frame_image = QImage(
            frame.data,
            frame.shape[1],
            frame.shape[0],
            frame.strides[0],
            QImage.Format.Format_RGB888,
        )

        edges_image = QImage(
            edges.data,
            edges.shape[1],
            edges.shape[0],
            edges.strides[0],
            QImage.Format.Format_RGB888,
        )

        self.photoLabel1.setPixmap(
            QPixmap.fromImage(frame_image).scaled(
                self.photoLabel1.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.photoLabel2.setPixmap(
            QPixmap.fromImage(edges_image).scaled(
                self.photoLabel2.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def updateCube(self, result: CubeDetectionResult):
        if result.numFaceletsDetected != 9 or result.labels[4] == CubeLabel.UNLABELD:
            return

        self.saveMeanColors(result.mean_facelet_color)

        face = CubeFace(result.labels[4].value)
        for i in range(9):
            if result.labels[i] == CubeLabel.UNLABELD or i == 4:
                continue
            positon = CubePosition(i)
            self.cube.setFaceletLabel(Facelet(face, positon), result.labels[i])

            if self.cube.isComplete():
                self.onScanComplete()

    def saveMeanColors(self, mean_colors: list[HSV]):
        homedir = path.expanduser("~")
        path_to_npyfile = path.join(homedir, ".local", "share", "rubiksolver")

        if not path.exists(path_to_npyfile):
            makedirs(path_to_npyfile)

        filename = "meancolors.npy"

        colors_array = np.array(
            [
                (hsv_color.hue, hsv_color.saturation, hsv_color.value)
                for hsv_color in mean_colors
            ]
        )

        if path.exists(path.join(path_to_npyfile, filename)):
            previous_colors = np.load(path.join(path_to_npyfile, filename))
            colors_array = np.concatenate((previous_colors, colors_array))

        np.save(path.join(path_to_npyfile, filename), colors_array)

    def onScanComplete(self):
        self.PauseSignal.emit()
        self.animTimeline = self.cube.solution
        self.cubeViewer.playButton.setEnabled(True)
        self.cubeViewer.nextButton.setEnabled(True)
        self.cubeViewer.prevButton.setEnabled(True)

    @Slot()
    def playPressed(self):
        pass

    @Slot()
    def nextPressed(self):
        if self.animTimeline is None:
            return
        move = self.animTimeline.next()
        if move is None:
            return
        self.cube.applyMove(move)
        print(f"{move}: {self.cube}")
        self.cubeViewer.playMove(move, self.cube.state)

    @Slot()
    def prevPressed(self):
        if self.animTimeline is None:
            return
        move = self.animTimeline.prev()
        if move is None:
            return
        self.cube.applyMove(move)
        self.cubeViewer.playMove(move, self.cube.state)

    @Slot()
    def resetPressed(self):
        self.ResumeSignal.emit()
        self.cubeViewer.playButton.setDisabled(True)
        self.cubeViewer.nextButton.setDisabled(True)
        self.cubeViewer.prevButton.setDisabled(True)
        self.cube.reset()
