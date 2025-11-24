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


class CubeMove(Enum):
    U = 0
    UPRIME = 1
    R = 2
    RPRIME = 3
    F = 4
    FPRIME = 5
    D = 6
    DPRIME = 7
    L = 8
    LPRIME = 9
    B = 10
    BPRIME = 11


class MoveTimeline:
    MoveReverse = {
        CubeMove.U: CubeMove.UPRIME,
        CubeMove.UPRIME: CubeMove.U,
        CubeMove.R: CubeMove.RPRIME,
        CubeMove.RPRIME: CubeMove.R,
        CubeMove.F: CubeMove.FPRIME,
        CubeMove.FPRIME: CubeMove.F,
        CubeMove.D: CubeMove.DPRIME,
        CubeMove.DPRIME: CubeMove.D,
        CubeMove.L: CubeMove.LPRIME,
        CubeMove.LPRIME: CubeMove.L,
        CubeMove.B: CubeMove.BPRIME,
        CubeMove.BPRIME: CubeMove.B,
    }

    def __init__(self, moves: list[CubeMove]):
        self.moves = moves
        self.currentPosition = 0
        self.numMoves = len(moves)

    def next(self) -> CubeMove | None:
        if self.currentPosition >= self.numMoves:
            return None
        move = self.moves[self.currentPosition]
        self.currentPosition += 1
        return move

    def prev(self) -> CubeMove | None:
        if self.currentPosition <= 0:
            return None

        self.currentPosition -= 1
        move = self.MoveReverse[self.moves[self.currentPosition]]
        return move


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
            Facelet(CubeFace.DOWN, CubePosition.SEVEN),
            Facelet(CubeFace.DOWN, CubePosition.FOUR),
            Facelet(CubeFace.DOWN, CubePosition.ONE),
        ],
        CubeFace.BACK: [
            Facelet(CubeFace.UP, CubePosition.THREE),
            Facelet(CubeFace.UP, CubePosition.TWO),
            Facelet(CubeFace.UP, CubePosition.ONE),
            #
            Facelet(CubeFace.LEFT, CubePosition.ONE),
            Facelet(CubeFace.LEFT, CubePosition.FOUR),
            Facelet(CubeFace.LEFT, CubePosition.SEVEN),
            #
            Facelet(CubeFace.RIGHT, CubePosition.THREE),
            Facelet(CubeFace.RIGHT, CubePosition.SIX),
            Facelet(CubeFace.RIGHT, CubePosition.NINE),
            #
            Facelet(CubeFace.DOWN, CubePosition.NINE),
            Facelet(CubeFace.DOWN, CubePosition.EIGHT),
            Facelet(CubeFace.DOWN, CubePosition.SEVEN),
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

        self.solution: MoveTimeline | None = None

    def isComplete(self) -> bool:
        try:
            if CubeLabel.UNLABELD not in self.state and self.solution is None:
                solution = kociemba.solve(str(self))
                if isinstance(solution, str):
                    print(solution)
                    self.solution = self.parseSolution(solution)
                    return True
        except ValueError:
            return False
        return False

    def parseSolution(self, solution: str) -> MoveTimeline:
        moves: list[CubeMove] = []
        for move in solution.split(" "):
            match move:
                case "U":
                    moves.append(CubeMove.U)
                case "U'":
                    moves.append(CubeMove.UPRIME)
                case "U2":
                    moves.append(CubeMove.U)
                    moves.append(CubeMove.U)

                case "R":
                    moves.append(CubeMove.R)
                case "R'":
                    moves.append(CubeMove.RPRIME)
                case "R2":
                    moves.append(CubeMove.R)
                    moves.append(CubeMove.R)

                case "F":
                    moves.append(CubeMove.F)
                case "F'":
                    moves.append(CubeMove.FPRIME)
                case "F2":
                    moves.append(CubeMove.F)
                    moves.append(CubeMove.F)

                case "D":
                    moves.append(CubeMove.D)
                case "D'":
                    moves.append(CubeMove.DPRIME)
                case "D2":
                    moves.append(CubeMove.D)
                    moves.append(CubeMove.D)

                case "L":
                    moves.append(CubeMove.L)
                case "L'":
                    moves.append(CubeMove.LPRIME)
                case "L2":
                    moves.append(CubeMove.L)
                    moves.append(CubeMove.L)

                case "B":
                    moves.append(CubeMove.B)
                case "B'":
                    moves.append(CubeMove.BPRIME)
                case "B2":
                    moves.append(CubeMove.B)
                    moves.append(CubeMove.B)
                case _:
                    raise ValueError(f'Move "{move}" not recognized!')

        return MoveTimeline(moves)

    def reset(self) -> None:
        self.state = [CubeLabel.UNLABELD for _ in range(self.numFacelets)]
        for cube_face in CubeFace:
            center_idx = (cube_face.value * 9) + CubePosition.FIVE.value
            self.state[center_idx] = CubeLabel(cube_face.value)

        self.solution = None

    def applyMove(self, move: CubeMove) -> None:
        match move:
            case CubeMove.U:
                self.rotateUpCW()
            case CubeMove.UPRIME:
                self.rotateUpCCW()
            case CubeMove.R:
                self.rotateRightCW()
            case CubeMove.RPRIME:
                self.rotateRightCCW()
            case CubeMove.F:
                self.rotateFrontCW()
            case CubeMove.FPRIME:
                self.rotateFrontCCW()
            case CubeMove.D:
                self.rotateDownCW()
            case CubeMove.DPRIME:
                self.rotateDownCCW()
            case CubeMove.L:
                self.rotateLeftCW()
            case CubeMove.LPRIME:
                self.rotateLeftCCW()
            case CubeMove.B:
                self.rotateBackCW()
            case CubeMove.BPRIME:
                self.rotateBackCCW()

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
