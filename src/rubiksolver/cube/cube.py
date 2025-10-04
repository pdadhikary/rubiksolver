from dataclasses import dataclass
from enum import Enum

import kociemba


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


class CubePosition(Enum):
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
    postion: CubePosition


class RubiksCube:
    EdgeMap: dict[CubeFace, list[Facelet]] = {
        CubeFace.UP: [
            Facelet(CubeFace.BACK, CubePosition.THREE),
            Facelet(CubeFace.BACK, CubePosition.TWO),
            Facelet(CubeFace.BACK, CubePosition.ONE),
            #
            Facelet(CubeFace.RIGHT, CubePosition.THREE),
            Facelet(CubeFace.RIGHT, CubePosition.TWO),
            Facelet(CubeFace.RIGHT, CubePosition.ONE),
            #
            Facelet(CubeFace.LEFT, CubePosition.ONE),
            Facelet(CubeFace.LEFT, CubePosition.TWO),
            Facelet(CubeFace.LEFT, CubePosition.THREE),
            #
            Facelet(CubeFace.FRONT, CubePosition.ONE),
            Facelet(CubeFace.FRONT, CubePosition.TWO),
            Facelet(CubeFace.FRONT, CubePosition.THREE),
        ],
        CubeFace.RIGHT: [
            Facelet(CubeFace.UP, CubePosition.NINE),
            Facelet(CubeFace.UP, CubePosition.SIX),
            Facelet(CubeFace.UP, CubePosition.THREE),
            #
            Facelet(CubeFace.BACK, CubePosition.ONE),
            Facelet(CubeFace.BACK, CubePosition.FOUR),
            Facelet(CubeFace.BACK, CubePosition.SEVEN),
            #
            Facelet(CubeFace.FRONT, CubePosition.THREE),
            Facelet(CubeFace.FRONT, CubePosition.SIX),
            Facelet(CubeFace.FRONT, CubePosition.NINE),
            #
            Facelet(CubeFace.DOWN, CubePosition.THREE),
            Facelet(CubeFace.DOWN, CubePosition.SIX),
            Facelet(CubeFace.DOWN, CubePosition.NINE),
        ],
        CubeFace.FRONT: [
            Facelet(CubeFace.UP, CubePosition.SEVEN),
            Facelet(CubeFace.UP, CubePosition.EIGHT),
            Facelet(CubeFace.UP, CubePosition.NINE),
            #
            Facelet(CubeFace.RIGHT, CubePosition.ONE),
            Facelet(CubeFace.RIGHT, CubePosition.FOUR),
            Facelet(CubeFace.RIGHT, CubePosition.SEVEN),
            #
            Facelet(CubeFace.LEFT, CubePosition.THREE),
            Facelet(CubeFace.LEFT, CubePosition.SIX),
            Facelet(CubeFace.LEFT, CubePosition.NINE),
            #
            Facelet(CubeFace.DOWN, CubePosition.ONE),
            Facelet(CubeFace.DOWN, CubePosition.TWO),
            Facelet(CubeFace.DOWN, CubePosition.THREE),
        ],
        CubeFace.DOWN: [
            Facelet(CubeFace.FRONT, CubePosition.SEVEN),
            Facelet(CubeFace.FRONT, CubePosition.EIGHT),
            Facelet(CubeFace.FRONT, CubePosition.NINE),
            #
            Facelet(CubeFace.RIGHT, CubePosition.SEVEN),
            Facelet(CubeFace.RIGHT, CubePosition.EIGHT),
            Facelet(CubeFace.RIGHT, CubePosition.NINE),
            #
            Facelet(CubeFace.LEFT, CubePosition.NINE),
            Facelet(CubeFace.LEFT, CubePosition.EIGHT),
            Facelet(CubeFace.LEFT, CubePosition.SEVEN),
            #
            Facelet(CubeFace.BACK, CubePosition.NINE),
            Facelet(CubeFace.BACK, CubePosition.EIGHT),
            Facelet(CubeFace.BACK, CubePosition.SEVEN),
        ],
        CubeFace.LEFT: [
            Facelet(CubeFace.UP, CubePosition.ONE),
            Facelet(CubeFace.UP, CubePosition.FOUR),
            Facelet(CubeFace.UP, CubePosition.SEVEN),
            #
            Facelet(CubeFace.FRONT, CubePosition.ONE),
            Facelet(CubeFace.FRONT, CubePosition.FOUR),
            Facelet(CubeFace.FRONT, CubePosition.SEVEN),
            #
            Facelet(CubeFace.BACK, CubePosition.THREE),
            Facelet(CubeFace.BACK, CubePosition.SIX),
            Facelet(CubeFace.BACK, CubePosition.NINE),
            #
            Facelet(CubeFace.DOWN, CubePosition.ONE),
            Facelet(CubeFace.DOWN, CubePosition.FOUR),
            Facelet(CubeFace.DOWN, CubePosition.SEVEN),
        ],
        CubeFace.BACK: [
            Facelet(CubeFace.UP, CubePosition.ONE),
            Facelet(CubeFace.UP, CubePosition.TWO),
            Facelet(CubeFace.UP, CubePosition.THREE),
            #
            Facelet(CubeFace.LEFT, CubePosition.ONE),
            Facelet(CubeFace.LEFT, CubePosition.FOUR),
            Facelet(CubeFace.LEFT, CubePosition.SEVEN),
            #
            Facelet(CubeFace.RIGHT, CubePosition.THREE),
            Facelet(CubeFace.RIGHT, CubePosition.SIX),
            Facelet(CubeFace.RIGHT, CubePosition.NINE),
            #
            Facelet(CubeFace.DOWN, CubePosition.SEVEN),
            Facelet(CubeFace.DOWN, CubePosition.EIGHT),
            Facelet(CubeFace.DOWN, CubePosition.NINE),
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
            center_idx = (cube_face.value * 9) + CubePosition.FIVE.value
            self.state[center_idx] = CubeLabel(cube_face.value)

        self.solution: str | None = None

    def isComplete(self) -> bool:
        try:
            if CubeLabel.UNLABELD not in self.state:
                solution = kociemba.solve(str(self))
                if isinstance(solution, str):
                    self.solution = solution
                    return True
        except ValueError:
            return False
        return False

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
            Facelet(face, CubePosition.TWO), Facelet(face, CubePosition.FOUR)
        )
        self._swapFacelets(
            Facelet(face, CubePosition.THREE), Facelet(face, CubePosition.SEVEN)
        )
        self._swapFacelets(
            Facelet(face, CubePosition.SIX), Facelet(face, CubePosition.EIGHT)
        )

    def _flipEdges(self, face: CubeFace) -> None:
        self._swapFacelets(RubiksCube.EdgeMap[face][0], RubiksCube.EdgeMap[face][2])
        self._swapFacelets(RubiksCube.EdgeMap[face][3], RubiksCube.EdgeMap[face][6])
        self._swapFacelets(RubiksCube.EdgeMap[face][4], RubiksCube.EdgeMap[face][7])
        self._swapFacelets(RubiksCube.EdgeMap[face][5], RubiksCube.EdgeMap[face][8])
        self._swapFacelets(RubiksCube.EdgeMap[face][9], RubiksCube.EdgeMap[face][11])

    def _flipFace(self, face: CubeFace) -> None:
        self._swapFacelets(
            Facelet(face, CubePosition.ONE), Facelet(face, CubePosition.THREE)
        )
        self._swapFacelets(
            Facelet(face, CubePosition.FOUR), Facelet(face, CubePosition.SIX)
        )
        self._swapFacelets(
            Facelet(face, CubePosition.SEVEN), Facelet(face, CubePosition.NINE)
        )

    def _swapFacelets(self, facelet1: Facelet, facelet2: Facelet) -> None:
        idx1 = RubiksCube.FaceletToIndex(facelet1)
        idx2 = RubiksCube.FaceletToIndex(facelet2)

        self.state[idx1], self.state[idx2] = self.state[idx2], self.state[idx1]

    @staticmethod
    def FaceletToIndex(facelet: Facelet) -> int:
        return (facelet.face.value * 9) + facelet.postion.value
