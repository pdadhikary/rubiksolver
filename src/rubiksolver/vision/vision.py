from abc import ABC, abstractmethod
from dataclasses import dataclass

import cv2 as cv
import numpy as np
from cv2.typing import MatLike, Rect, RotatedRect

from rubiksolver.cube import CubeLabel


@dataclass
class HSV:
    hue: int
    saturation: int
    value: int


@dataclass
class HSV_Range:
    lower: HSV
    upper: HSV


@dataclass
class CubeDetectionResult:
    frame: MatLike
    edges: MatLike
    numFaceletsDetected: int
    facelet_contours: list[MatLike]
    facelet_contour_bb: list[Rect]
    facelet_contour_rotated_bb: list[RotatedRect]
    facelet_contour_rotated_bb_points: list[MatLike]
    labels: list[CubeLabel]


@dataclass
class CubeDetectionParameters:
    _denoiseDiameter: int = 5
    _denoiseSigmaSpace: int = 580
    _denoiseSigmaColor: int = 580
    _cannyLowerThreshold: int = 30
    _cannyUpperThreshold: int = 60
    _faceletAreaLowerThreshold: int = 50
    _faceletAreaUpperThreshold: int = 170
    _faceletContourAreaRatioThreshold: int = 75
    _faceletBoundingBoxAspectRatioThreshold: int = 75
    _homographyRANSACMaxError: int = 130

    @property
    def denoiseDiameter(self) -> int:
        return self._denoiseDiameter

    @denoiseDiameter.setter
    def denoiseDiameter(self, value: int) -> None:
        self._denoiseDiameter = value

    @property
    def denoiseSigmaSpace(self) -> float:
        return self._denoiseSigmaSpace / 10.0

    @denoiseSigmaSpace.setter
    def denoiseSigmaSpace(self, value: int) -> None:
        self._denoiseSigmaSpace = value

    @property
    def denoiseSigmaColor(self) -> float:
        return self._denoiseSigmaColor / 10.0

    @denoiseSigmaColor.setter
    def denoiseSigmaColor(self, value: int) -> None:
        self._denoiseSigmaColor = value

    @property
    def cannyLowerThreshold(self) -> int:
        return self._cannyLowerThreshold

    @cannyLowerThreshold.setter
    def cannyLowerThreshold(self, value: int) -> None:
        self._cannyLowerThreshold = value

    @property
    def cannyUpperThreshold(self) -> int:
        return self._cannyUpperThreshold

    @cannyUpperThreshold.setter
    def cannyUpperThreshold(self, value: int) -> None:
        self._cannyUpperThreshold = value

    @property
    def faceletAreaLowerThreshold(self) -> float:
        return self._faceletAreaLowerThreshold / 100.0

    @faceletAreaLowerThreshold.setter
    def faceletAreaLowerThreshold(self, value: int) -> None:
        self._faceletAreaLowerThreshold = value

    @property
    def faceletAreaUpperThreshold(self) -> float:
        return self._faceletAreaUpperThreshold / 100.0

    @faceletAreaUpperThreshold.setter
    def faceletAreaUpperThreshold(self, value: int) -> None:
        self._faceletAreaUpperThreshold = value

    @property
    def faceletCountourAreaRatioThreshold(self) -> float:
        return self._faceletContourAreaRatioThreshold / 100.0

    @faceletCountourAreaRatioThreshold.setter
    def faceletCountourAreaRatioThreshold(self, value: int) -> None:
        self._faceletContourAreaRatioThreshold = value

    @property
    def faceletBoundingAspectRatioThreshold(self) -> float:
        return self._faceletBoundingBoxAspectRatioThreshold / 100.0

    @faceletBoundingAspectRatioThreshold.setter
    def faceletBoundingAspectRatioThreshold(self, value: int) -> None:
        self._faceletBoundingBoxAspectRatioThreshold = value

    @property
    def homographyRANSACMaxError(self) -> float:
        return float(self._homographyRANSACMaxError)

    @homographyRANSACMaxError.setter
    def homographyRANSACMaxError(self, value: int) -> None:
        self._homographyRANSACMaxError = value


class ColorClassificationModel(ABC):
    @abstractmethod
    def classify(self, hsv: HSV) -> CubeLabel:
        pass


class FixedColorClassificationModel(ColorClassificationModel):
    ColorLabelMap: dict[CubeLabel, HSV_Range] = {
        CubeLabel.UP: HSV_Range(HSV(0, 0, 130), HSV(180, 90, 255)),
        CubeLabel.RIGHT: HSV_Range(HSV(95, 150, 90), HSV(130, 255, 255)),
        CubeLabel.FRONT: HSV_Range(HSV(160, 100, 90), HSV(180, 255, 255)),
        CubeLabel.DOWN: HSV_Range(HSV(20, 100, 90), HSV(35, 255, 255)),
        CubeLabel.LEFT: HSV_Range(HSV(40, 100, 90), HSV(80, 255, 255)),
        CubeLabel.BACK: HSV_Range(HSV(5, 140, 150), HSV(15, 255, 255)),
    }

    def classify(self, hsv: HSV) -> CubeLabel:
        for label in FixedColorClassificationModel.ColorLabelMap.keys():
            range = FixedColorClassificationModel.ColorLabelMap[label]

            if FixedColorClassificationModel._hsvInRange(hsv, range.lower, range.upper):
                return label

        print(hsv)
        return CubeLabel.UNLABELD

    @staticmethod
    def _hsvInRange(color: HSV, lower: HSV, upper: HSV) -> bool:
        if not (
            lower.saturation <= color.saturation <= upper.saturation
            and lower.value <= color.value <= upper.value
        ):
            return False

        if lower.hue <= upper.hue:
            return lower.hue <= color.hue <= upper.hue
        else:
            return color.hue <= upper.hue or color.hue >= lower.hue


class CubeDetectionPipeline:
    def __init__(
        self,
        faceletColorClassifier: ColorClassificationModel,
        parameters: CubeDetectionParameters,
    ):
        self.faceletColorClassifier = faceletColorClassifier
        self.frame: MatLike | None = None
        self.parameters: CubeDetectionParameters = parameters

    def forward(self, frame: MatLike) -> None:
        self.frame = frame

    def result(self) -> CubeDetectionResult:
        if self.frame is None:
            raise RuntimeError(
                "Need to set frame before calling result(). "
                "Use forward(frame) to set the frame."
            )

        frame_preprocessed = self.preprocessFrame(self.frame)
        frame_edges = self.getCannyEdges(frame_preprocessed)
        candidates = self.findCandidateFacelets(frame_edges)
        facelets = self.faceletCandidateRANSAC(candidates)
        labels = self.labelFacelets(self.frame, facelets)

        rects: list[Rect] = [cv.boundingRect(facelet) for facelet in facelets]
        rects_rotated: list[RotatedRect] = [
            cv.minAreaRect(facelet) for facelet in facelets
        ]

        rects_rotated_points: list[MatLike] = [
            np.array(cv.boxPoints(rect), dtype=np.int32) for rect in rects_rotated
        ]

        frame_edges = cv.cvtColor(frame_edges, cv.COLOR_GRAY2BGR)

        return CubeDetectionResult(
            self.frame,
            frame_edges,
            len(facelets),
            facelets,
            rects,
            rects_rotated,
            rects_rotated_points,
            labels,
        )

    def preprocessFrame(self, frame: MatLike) -> MatLike:
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_denoise = cv.bilateralFilter(
            frame_gray,
            d=self.parameters.denoiseDiameter,
            sigmaSpace=self.parameters.denoiseSigmaSpace,
            sigmaColor=self.parameters.denoiseSigmaColor,
        )
        return frame_denoise

    def getCannyEdges(self, frame: MatLike) -> MatLike:
        edges = cv.Canny(
            frame,
            threshold1=self.parameters.cannyLowerThreshold,
            threshold2=self.parameters.cannyUpperThreshold,
        )
        edges_dialated = cv.dilate(
            edges, cv.getStructuringElement(cv.MORPH_RECT, (2, 2)), iterations=3
        )
        return edges_dialated

    def findCandidateFacelets(self, edges: MatLike) -> list[MatLike]:
        contours, _ = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        total_area = edges.shape[0] * edges.shape[1]

        def facelet_criteria(cont: MatLike) -> RotatedRect | None:
            area = cv.contourArea(cont)
            area_norm = (area / total_area) * 100

            if (
                area_norm < self.parameters.faceletAreaLowerThreshold
                or area_norm > self.parameters.faceletAreaUpperThreshold
            ):
                return None

            rect: RotatedRect = cv.minAreaRect(cont)
            w, h = rect[1]
            min_bb_area = w * h
            area_ratio = area / min_bb_area

            if area_ratio < self.parameters.faceletCountourAreaRatioThreshold:
                return None

            aspect_ratio = min(w, h) / max(w, h)

            if aspect_ratio < self.parameters.faceletBoundingAspectRatioThreshold:
                return None

            return rect

        candidates = [
            candidate for candidate in contours if facelet_criteria(candidate)
        ]

        if len(candidates) == 0:
            return candidates

        facelet_mask = np.zeros(edges.shape, dtype=np.uint8)
        facelet_mask = cv.drawContours(facelet_mask, candidates, -1, (255,), cv.FILLED)

        candidates, _ = cv.findContours(
            facelet_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )

        return list(candidates)

    def faceletCandidateRANSAC(self, candidates: list[MatLike]) -> list[MatLike]:
        if len(candidates) <= 4:
            return candidates

        def centroid(candidate: MatLike) -> tuple[int, int]:
            moments = cv.moments(candidate)
            return (
                int(moments["m10"] / (moments["m00"] + 1e-5)),
                int(moments["m01"] / (moments["m00"] + 1e-5)),
            )

        centroids = np.array(
            [centroid(candidate) for candidate in candidates], dtype=np.float32
        )

        best_inliers: list[int] = []
        grid = CubeDetectionPipeline.homographyGrid()
        for _ in range(100):
            indices = np.random.choice(len(centroids), 4, replace=False)
            H, _ = cv.findHomography(grid[:4], centroids[indices], cv.RANSAC, 5.0)

            if H is None:
                continue

            projected = cv.perspectiveTransform(grid.reshape(-1, 1, 2), H).reshape(
                -1, 2
            )

            errors = np.linalg.norm(centroids[:, None] - projected[None, :], axis=2)
            min_err = np.min(errors, axis=1)

            inliers = [
                i
                for i, e in enumerate(min_err)
                if e < self.parameters.homographyRANSACMaxError
            ]
            if len(inliers) > len(best_inliers):
                best_inliers = inliers

                if len(inliers) == 9:
                    break

        num_inliers = len(best_inliers)

        best_inliers = sorted(best_inliers, key=lambda i: centroids[i][1])

        if num_inliers >= 3:
            best_inliers[:3] = sorted(best_inliers[:3], key=lambda i: centroids[i][0])

        if num_inliers >= 6:
            best_inliers[3:6] = sorted(best_inliers[3:6], key=lambda i: centroids[i][0])
        else:
            best_inliers[3:] = sorted(best_inliers[3:], key=lambda i: centroids[i][0])

        if num_inliers > 6:
            best_inliers[6:] = sorted(best_inliers[6:], key=lambda i: centroids[i][0])

        return [candidates[i] for i in best_inliers]

    def labelFacelets(self, frame: MatLike, facelets: list[MatLike]) -> list[CubeLabel]:
        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        results: list[CubeLabel] = []

        for facelet in facelets:
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            cv.drawContours(mask, [facelet], -1, (255,), -1)

            pixels = frame_hsv[mask == 255]

            med = np.median(pixels, axis=0)
            hsv = HSV(*(tuple(map(int, med))))

            results.append(self.faceletColorClassifier.classify(hsv))

        return results

    @staticmethod
    def homographyGrid() -> np.ndarray:
        return np.array(
            [
                [-1.0, -1.0],
                [0.0, -1.0],
                [1.0, -1.0],
                [-1.0, 0.0],
                [0.0, 0.0],
                [1.0, 0.0],
                [-1.0, 1.0],
                [0.0, 1.0],
                [1.0, 1.0],
            ]
        )
