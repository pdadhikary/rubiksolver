from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget
from superqt import QLabeledRangeSlider, QLabeledSlider


class CubeDetectionControlPanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setup()

    def setup(self):
        layout = QGridLayout(self)

        self.denoiseDiameter_label = QLabel(text="Denoise Filter Diameter")
        self.denoiseDiameter_slider = QLabeledSlider(Qt.Orientation.Horizontal)
        self.denoiseDiameter_slider.setRange(1, 5)
        self.denoiseDiameter_slider.setEdgeLabelMode(
            QLabeledSlider.EdgeLabelMode.LabelIsValue
        )

        self.denoiseSigmaSpace_label = QLabel(text="Space Filter Sigma")
        self.denoiseSigmaSpace_slider = QLabeledSlider(
            Qt.Orientation.Horizontal,
        )
        self.denoiseSigmaSpace_slider.setRange(300, 1000)
        self.denoiseSigmaSpace_slider.setEdgeLabelMode(
            QLabeledSlider.EdgeLabelMode.LabelIsValue
        )

        self.denoiseSigmaColor_label = QLabel(text="Color Filter Sigma")
        self.denoiseSigmaColor_slider = QLabeledSlider(Qt.Orientation.Horizontal)
        self.denoiseSigmaColor_slider.setRange(300, 1000)
        self.denoiseSigmaColor_slider.setEdgeLabelMode(
            QLabeledSlider.EdgeLabelMode.LabelIsValue
        )

        self.cannyThreshold_label = QLabel(text="Canny Threshold")
        self.cannyThreshold_slider = QLabeledRangeSlider(Qt.Orientation.Horizontal)
        self.cannyThreshold_slider.setRange(10, 150)

        self.faceletAreaThreshold_label = QLabel(text="Facelet Area Threshold")
        self.faceletAreaThreshold_slider = QLabeledRangeSlider(
            Qt.Orientation.Horizontal
        )
        self.faceletAreaThreshold_slider.setRange(0, 300)

        self.faceletContourAreaRatioThreshold_label = QLabel(
            text="Facelet Contour Area Ratio Threshold"
        )
        self.faceletContourAreaRatioThreshold_slider = QLabeledSlider(
            Qt.Orientation.Horizontal
        )
        self.faceletContourAreaRatioThreshold_slider.setRange(0, 100)
        self.faceletContourAreaRatioThreshold_slider.setEdgeLabelMode(
            QLabeledSlider.EdgeLabelMode.LabelIsValue
        )

        self.faceletBoundingBoxAspectRatioThreshold_label = QLabel(
            text="Facelet Bounding Box Aspect Ratio Threshold"
        )
        self.faceletBoundingBoxAspectRatioThreshold_slider = QLabeledSlider(
            Qt.Orientation.Horizontal
        )
        self.faceletBoundingBoxAspectRatioThreshold_slider.setRange(0, 100)
        self.faceletBoundingBoxAspectRatioThreshold_slider.setEdgeLabelMode(
            QLabeledSlider.EdgeLabelMode.LabelIsValue
        )

        self.homographyRASACMaxError_label = QLabel(text="RANSAC Error Threshold")
        self.homographyRASACMaxError_slider = QLabeledSlider(
            Qt.Orientation.Horizontal,
        )
        self.homographyRASACMaxError_slider.setRange(0, 300)
        self.homographyRASACMaxError_slider.setEdgeLabelMode(
            QLabeledSlider.EdgeLabelMode.LabelIsValue
        )

        layout.addWidget(self.denoiseDiameter_label, 0, 0)
        layout.addWidget(self.denoiseDiameter_slider, 0, 1)

        layout.addWidget(self.denoiseSigmaColor_label, 1, 0)
        layout.addWidget(self.denoiseSigmaColor_slider, 1, 1)

        layout.addWidget(self.denoiseSigmaSpace_label, 2, 0)
        layout.addWidget(self.denoiseSigmaSpace_slider, 2, 1)

        layout.addWidget(self.cannyThreshold_label, 3, 0)
        layout.addWidget(self.cannyThreshold_slider, 3, 1)

        layout.addWidget(self.faceletAreaThreshold_label, 4, 0)
        layout.addWidget(self.faceletAreaThreshold_slider, 4, 1)

        layout.addWidget(self.faceletContourAreaRatioThreshold_label, 5, 0)
        layout.addWidget(self.faceletContourAreaRatioThreshold_slider, 5, 1)

        layout.addWidget(self.faceletBoundingBoxAspectRatioThreshold_label, 6, 0)
        layout.addWidget(self.faceletBoundingBoxAspectRatioThreshold_slider, 6, 1)

        layout.addWidget(self.homographyRASACMaxError_label, 7, 0)
        layout.addWidget(self.homographyRASACMaxError_slider, 7, 1)
