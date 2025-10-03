from dataclasses import dataclass
from enum import Enum


class CubeFace(Enum):
    UP = 0
    RIGHT = 1
    FRONT = 2
    DOWN = 3
    LEFT = 4
    BACK = 5


class CubeLabel(Enum):
    UNLABELD = -1
    UP = 0
    RIGHT = 1
    FRONT = 2
    DOWN = 3
    LEFT = 4
    BACK = 5


class CubePositon(Enum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8


@dataclass
class Facelet:
    face: CubeFace
    postion: CubePositon


class RubiksCube:
    EdgeMap: dict[CubeFace, list[Facelet]] = {
        CubeFace.UP: [
            Facelet(CubeFace.BACK, CubePositon.THREE),
            Facelet(CubeFace.BACK, CubePositon.TWO),
            Facelet(CubeFace.BACK, CubePositon.ONE),
            #
            Facelet(CubeFace.RIGHT, CubePositon.THREE),
            Facelet(CubeFace.RIGHT, CubePositon.TWO),
            Facelet(CubeFace.RIGHT, CubePositon.ONE),
            #
            Facelet(CubeFace.LEFT, CubePositon.ONE),
            Facelet(CubeFace.LEFT, CubePositon.TWO),
            Facelet(CubeFace.LEFT, CubePositon.THREE),
            #
            Facelet(CubeFace.FRONT, CubePositon.ONE),
            Facelet(CubeFace.FRONT, CubePositon.TWO),
            Facelet(CubeFace.FRONT, CubePositon.THREE),
        ],
        CubeFace.RIGHT: [
            Facelet(CubeFace.UP, CubePositon.NINE),
            Facelet(CubeFace.UP, CubePositon.SIX),
            Facelet(CubeFace.UP, CubePositon.THREE),
            #
            Facelet(CubeFace.BACK, CubePositon.ONE),
            Facelet(CubeFace.BACK, CubePositon.FOUR),
            Facelet(CubeFace.BACK, CubePositon.SEVEN),
            #
            Facelet(CubeFace.FRONT, CubePositon.THREE),
            Facelet(CubeFace.FRONT, CubePositon.SIX),
            Facelet(CubeFace.FRONT, CubePositon.NINE),
            #
            Facelet(CubeFace.DOWN, CubePositon.THREE),
            Facelet(CubeFace.DOWN, CubePositon.SIX),
            Facelet(CubeFace.DOWN, CubePositon.NINE),
        ],
        CubeFace.FRONT: [
            Facelet(CubeFace.UP, CubePositon.SEVEN),
            Facelet(CubeFace.UP, CubePositon.EIGHT),
            Facelet(CubeFace.UP, CubePositon.NINE),
            #
            Facelet(CubeFace.RIGHT, CubePositon.ONE),
            Facelet(CubeFace.RIGHT, CubePositon.FOUR),
            Facelet(CubeFace.RIGHT, CubePositon.SEVEN),
            #
            Facelet(CubeFace.LEFT, CubePositon.THREE),
            Facelet(CubeFace.LEFT, CubePositon.SIX),
            Facelet(CubeFace.LEFT, CubePositon.NINE),
            #
            Facelet(CubeFace.DOWN, CubePositon.ONE),
            Facelet(CubeFace.DOWN, CubePositon.TWO),
            Facelet(CubeFace.DOWN, CubePositon.THREE),
        ],
        CubeFace.DOWN: [
            Facelet(CubeFace.FRONT, CubePositon.SEVEN),
            Facelet(CubeFace.FRONT, CubePositon.EIGHT),
            Facelet(CubeFace.FRONT, CubePositon.NINE),
            #
            Facelet(CubeFace.RIGHT, CubePositon.SEVEN),
            Facelet(CubeFace.RIGHT, CubePositon.EIGHT),
            Facelet(CubeFace.RIGHT, CubePositon.NINE),
            #
            Facelet(CubeFace.LEFT, CubePositon.NINE),
            Facelet(CubeFace.LEFT, CubePositon.EIGHT),
            Facelet(CubeFace.LEFT, CubePositon.SEVEN),
            #
            Facelet(CubeFace.BACK, CubePositon.NINE),
            Facelet(CubeFace.BACK, CubePositon.EIGHT),
            Facelet(CubeFace.BACK, CubePositon.SEVEN),
        ],
        CubeFace.LEFT: [
            Facelet(CubeFace.UP, CubePositon.ONE),
            Facelet(CubeFace.UP, CubePositon.FOUR),
            Facelet(CubeFace.UP, CubePositon.SEVEN),
            #
            Facelet(CubeFace.FRONT, CubePositon.ONE),
            Facelet(CubeFace.FRONT, CubePositon.FOUR),
            Facelet(CubeFace.FRONT, CubePositon.SEVEN),
            #
            Facelet(CubeFace.BACK, CubePositon.THREE),
            Facelet(CubeFace.BACK, CubePositon.SIX),
            Facelet(CubeFace.BACK, CubePositon.NINE),
            #
            Facelet(CubeFace.DOWN, CubePositon.ONE),
            Facelet(CubeFace.DOWN, CubePositon.FOUR),
            Facelet(CubeFace.DOWN, CubePositon.SEVEN),
        ],
        CubeFace.BACK: [
            Facelet(CubeFace.UP, CubePositon.ONE),
            Facelet(CubeFace.UP, CubePositon.TWO),
            Facelet(CubeFace.UP, CubePositon.THREE),
            #
            Facelet(CubeFace.LEFT, CubePositon.ONE),
            Facelet(CubeFace.LEFT, CubePositon.FOUR),
            Facelet(CubeFace.LEFT, CubePositon.SEVEN),
            #
            Facelet(CubeFace.RIGHT, CubePositon.THREE),
            Facelet(CubeFace.RIGHT, CubePositon.SIX),
            Facelet(CubeFace.RIGHT, CubePositon.NINE),
            #
            Facelet(CubeFace.DOWN, CubePositon.SEVEN),
            Facelet(CubeFace.DOWN, CubePositon.EIGHT),
            Facelet(CubeFace.DOWN, CubePositon.NINE),
        ],
    }

    StrLabel: dict[CubeLabel, str] = {
        CubeLabel.UNLABELD: "X",
        CubeLabel.UP: "U",
        CubeLabel.RIGHT: "R",
        CubeLabel.FRONT: "F",
        CubeLabel.DOWN: "D",
        CubeLabel.LEFT: "L",
        CubeLabel.BACK: "B",
    }

    def __init__(self) -> None:
        self.numFacelets = 9 * 6
        self.state: list[CubeLabel] = [
            CubeLabel.UNLABELD for _ in range(self.numFacelets)
        ]
        for cube_face in CubeFace:
            center_idx = (cube_face.value * 9) + CubePositon.FIVE.value
            self.state[center_idx] = CubeLabel(cube_face.value)

    def rotateFrontCW(self) -> None:
        self._rotateFaceCW(CubeFace.FRONT)

    def rotateFrontCCW(self) -> None:
        self._rotateFaceCCW(CubeFace.FRONT)

    def rotateBackCW(self) -> None:
        self._rotateFaceCW(CubeFace.BACK)

    def rotateBackCCW(self) -> None:
        self._rotateFaceCCW(CubeFace.BACK)

    def rotateUpCW(self) -> None:
        self._rotateFaceCW(CubeFace.UP)

    def rotateUpCCW(self) -> None:
        self._rotateFaceCCW(CubeFace.UP)

    def rotateDownCW(self) -> None:
        self._rotateFaceCW(CubeFace.DOWN)

    def rotateDownCCW(self) -> None:
        self._rotateFaceCCW(CubeFace.DOWN)

    def rotateLeftCW(self) -> None:
        self._rotateFaceCW(CubeFace.LEFT)

    def rotateLeftCCW(self) -> None:
        self._rotateFaceCCW(CubeFace.LEFT)

    def rotateRightCW(self) -> None:
        self._rotateFaceCW(CubeFace.RIGHT)

    def rotateRightCCW(self) -> None:
        self._rotateFaceCCW(CubeFace.RIGHT)

    def setFaceletLabel(self, facelet: Facelet, facelet_label: CubeLabel) -> None:
        self.state[RubiksCube.FaceletToIndex(facelet)] = facelet_label

    def getFaceletLabel(self, facelet: Facelet) -> CubeLabel:
        return self.state[RubiksCube.FaceletToIndex(facelet)]

    def __str__(self):
        return "".join([RubiksCube.StrLabel[label] for label in self.state])

    def _rotateFaceCW(self, face: CubeFace) -> None:
        self._transposeFace(face)
        self._transposeEdges(face)
        self._flipFace(face)
        self._flipEdges(face)

    def _rotateFaceCCW(self, face: CubeFace) -> None:
        self._flipFace(face)
        self._flipEdges(face)
        self._transposeFace(face)
        self._transposeEdges(face)

    def _transposeEdges(self, face: CubeFace) -> None:
        self._swapFacelets(RubiksCube.EdgeMap[face][0], RubiksCube.EdgeMap[face][6])
        self._swapFacelets(RubiksCube.EdgeMap[face][1], RubiksCube.EdgeMap[face][7])
        self._swapFacelets(RubiksCube.EdgeMap[face][2], RubiksCube.EdgeMap[face][8])

        self._swapFacelets(RubiksCube.EdgeMap[face][3], RubiksCube.EdgeMap[face][9])
        self._swapFacelets(RubiksCube.EdgeMap[face][4], RubiksCube.EdgeMap[face][10])
        self._swapFacelets(RubiksCube.EdgeMap[face][5], RubiksCube.EdgeMap[face][11])

    def _transposeFace(self, face: CubeFace) -> None:
        self._swapFacelets(
            Facelet(face, CubePositon.TWO), Facelet(face, CubePositon.FOUR)
        )
        self._swapFacelets(
            Facelet(face, CubePositon.THREE), Facelet(face, CubePositon.SEVEN)
        )
        self._swapFacelets(
            Facelet(face, CubePositon.SIX), Facelet(face, CubePositon.EIGHT)
        )

    def _flipEdges(self, face: CubeFace) -> None:
        self._swapFacelets(RubiksCube.EdgeMap[face][0], RubiksCube.EdgeMap[face][2])
        self._swapFacelets(RubiksCube.EdgeMap[face][3], RubiksCube.EdgeMap[face][6])
        self._swapFacelets(RubiksCube.EdgeMap[face][4], RubiksCube.EdgeMap[face][7])
        self._swapFacelets(RubiksCube.EdgeMap[face][5], RubiksCube.EdgeMap[face][8])
        self._swapFacelets(RubiksCube.EdgeMap[face][9], RubiksCube.EdgeMap[face][11])

    def _flipFace(self, face: CubeFace) -> None:
        self._swapFacelets(
            Facelet(face, CubePositon.ONE), Facelet(face, CubePositon.THREE)
        )
        self._swapFacelets(
            Facelet(face, CubePositon.FOUR), Facelet(face, CubePositon.SIX)
        )
        self._swapFacelets(
            Facelet(face, CubePositon.SEVEN), Facelet(face, CubePositon.NINE)
        )

    def _swapFacelets(self, facelet1: Facelet, facelet2: Facelet) -> None:
        idx1 = RubiksCube.FaceletToIndex(facelet1)
        idx2 = RubiksCube.FaceletToIndex(facelet2)

        self.state[idx1], self.state[idx2] = self.state[idx2], self.state[idx1]

    @staticmethod
    def FaceletToIndex(facelet: Facelet) -> int:
        return (facelet.face.value * 9) + facelet.postion.value
