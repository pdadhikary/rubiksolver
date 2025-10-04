import numpy as np
import pyrr

from rubiksolver.cube import CubeFace, CubeLabel
from rubiksolver.vision import PlanarCubeVisualizer

from .transformation import ModelMatrixStack


class RubiksCubeMesh:
    ColorMap = {
        CubeLabel.UP: np.array(
            PlanarCubeVisualizer.ColorMap[CubeLabel.UP], dtype=np.float32
        )[::-1]
        / 255.0,
        CubeLabel.RIGHT: np.array(
            PlanarCubeVisualizer.ColorMap[CubeLabel.RIGHT], dtype=np.float32
        )[::-1]
        / 255.0,
        CubeLabel.FRONT: np.array(
            PlanarCubeVisualizer.ColorMap[CubeLabel.FRONT], dtype=np.float32
        )[::-1]
        / 255.0,
        CubeLabel.DOWN: np.array(
            PlanarCubeVisualizer.ColorMap[CubeLabel.DOWN], dtype=np.float32
        )[::-1]
        / 255.0,
        CubeLabel.LEFT: np.array(
            PlanarCubeVisualizer.ColorMap[CubeLabel.LEFT], dtype=np.float32
        )[::-1]
        / 255.0,
        CubeLabel.BACK: np.array(
            PlanarCubeVisualizer.ColorMap[CubeLabel.BACK], dtype=np.float32
        )[::-1]
        / 255.0,
        CubeLabel.UNLABELD: np.array(
            PlanarCubeVisualizer.ColorMap[CubeLabel.UNLABELD], dtype=np.float32
        )[::-1]
        / 255.0,
    }

    CubiesIndicesByFace = {
        CubeFace.UP: [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            18,
            19,
            20,
            36,
            37,
            38,
            45,
            46,
            47,
        ],
        CubeFace.RIGHT: [
            2,
            5,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            20,
            23,
            26,
            29,
            32,
            35,
            45,
            48,
            51,
        ],
        CubeFace.FRONT: [
            6,
            7,
            8,
            9,
            12,
            15,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            38,
            41,
            44,
        ],
        CubeFace.DOWN: [
            15,
            16,
            17,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            42,
            43,
            44,
            51,
            52,
            53,
        ],
        CubeFace.LEFT: [
            0,
            3,
            6,
            18,
            21,
            24,
            27,
            30,
            33,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            47,
            50,
            53,
        ],
        CubeFace.BACK: [
            0,
            1,
            2,
            11,
            14,
            17,
            33,
            34,
            35,
            36,
            39,
            42,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
        ],
    }

    def __init__(self) -> None:
        normals = np.array(
            [
                [0, 0, 1],
                [0, 0, 1],
                [0, 0, 1],
                [0, 0, 1],
                [0, 0, 1],
                [0, 0, 1],
            ],
            dtype=np.float32,
        )
        verts, indices = pyrr.geometry.create_quad(st=True)
        self.vertices = np.hstack((verts[indices], normals))
        self.nvertices = 6
        self.ninstances = 54

        self.modelMatices = self.getModelMatrices()

    def getColorData(self, labels: list[CubeLabel]) -> np.ndarray:
        return np.array([self.ColorMap[label] for label in labels], dtype=np.float32)

    def getRotationMatrices(self, face: CubeFace, angle: float) -> np.ndarray:
        indices_to_rotate = self.CubiesIndicesByFace[face]

        ids = np.eye(4, dtype=np.float32).reshape((1, 4, 4))
        rotMats = np.repeat(ids, self.ninstances, axis=0)

        rot = pyrr.matrix44.create_identity(dtype=np.float32)
        if face == CubeFace.UP or face == CubeFace.DOWN:
            rot = pyrr.matrix44.create_from_y_rotation(
                np.radians(angle), dtype=np.float32
            )
        if face == CubeFace.RIGHT or face == CubeFace.LEFT:
            rot = pyrr.matrix44.create_from_x_rotation(
                np.radians(angle), dtype=np.float32
            )
        if face == CubeFace.FRONT or face == CubeFace.BACK:
            rot = pyrr.matrix44.create_from_z_rotation(
                np.radians(angle), dtype=np.float32
            )

        rotMats[indices_to_rotate] = rot
        return rotMats

    def getModelMatrices(self) -> np.ndarray:
        stack = ModelMatrixStack()
        modelMatrices = np.zeros((self.ninstances, 4, 4), dtype=np.float32)

        # UP FACE
        stack.gPush()
        stack.gRotateX(90)
        stack.gTranslate(-1, 1, 1.5)
        modelMatrices[0] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(90)
        stack.gTranslate(0, 1, 1.5)
        modelMatrices[1] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(90)
        stack.gTranslate(1, 1, 1.5)
        modelMatrices[2] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(90)
        stack.gTranslate(-1, 0, 1.5)
        modelMatrices[3] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(90)
        stack.gTranslate(0, 0, 1.5)
        modelMatrices[4] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(90)
        stack.gTranslate(1, 0, 1.5)
        modelMatrices[5] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(90)
        stack.gTranslate(-1, -1, 1.5)
        modelMatrices[6] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(90)
        stack.gTranslate(0, -1, 1.5)
        modelMatrices[7] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(90)
        stack.gTranslate(1, -1, 1.5)
        modelMatrices[8] = stack.modelMatrix
        stack.gPop()

        # RIGHT FACE
        stack.gPush()
        stack.gRotateY(-90)
        stack.gTranslate(-1, 1, 1.5)
        modelMatrices[9] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(-90)
        stack.gTranslate(0, 1, 1.5)
        modelMatrices[10] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(-90)
        stack.gTranslate(1, 1, 1.5)
        modelMatrices[11] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(-90)
        stack.gTranslate(-1, 0, 1.5)
        modelMatrices[12] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(-90)
        stack.gTranslate(0, 0, 1.5)
        modelMatrices[13] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(-90)
        stack.gTranslate(1, 0, 1.5)
        modelMatrices[14] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(-90)
        stack.gTranslate(-1, -1, 1.5)
        modelMatrices[15] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(-90)
        stack.gTranslate(0, -1, 1.5)
        modelMatrices[16] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(-90)
        stack.gTranslate(1, -1, 1.5)
        modelMatrices[17] = stack.modelMatrix
        stack.gPop()

        # FRONT FACE
        stack.gPush()
        stack.gTranslate(-1, 1, 1.5)
        modelMatrices[18] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gTranslate(0, 1, 1.5)
        modelMatrices[19] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gTranslate(1, 1, 1.5)
        modelMatrices[20] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gTranslate(-1, 0, 1.5)
        modelMatrices[21] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gTranslate(0, 0, 1.5)
        modelMatrices[22] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gTranslate(1, 0, 1.5)
        modelMatrices[23] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gTranslate(-1, -1, 1.5)
        modelMatrices[24] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gTranslate(0, -1, 1.5)
        modelMatrices[25] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gTranslate(1, -1, 1.5)
        modelMatrices[26] = stack.modelMatrix
        stack.gPop()

        # DOWN FACE
        stack.gPush()
        stack.gRotateX(-90)
        stack.gTranslate(-1, 1, 1.5)
        modelMatrices[27] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(-90)
        stack.gTranslate(0, 1, 1.5)
        modelMatrices[28] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(-90)
        stack.gTranslate(1, 1, 1.5)
        modelMatrices[29] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(-90)
        stack.gTranslate(-1, 0, 1.5)
        modelMatrices[30] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(-90)
        stack.gTranslate(0, 0, 1.5)
        modelMatrices[31] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(-90)
        stack.gTranslate(1, 0, 1.5)
        modelMatrices[32] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(-90)
        stack.gTranslate(-1, -1, 1.5)
        modelMatrices[33] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(-90)
        stack.gTranslate(0, -1, 1.5)
        modelMatrices[34] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateX(-90)
        stack.gTranslate(1, -1, 1.5)
        modelMatrices[35] = stack.modelMatrix
        stack.gPop()

        # LEFT FACE
        stack.gPush()
        stack.gRotateY(90)
        stack.gTranslate(-1, 1, 1.5)
        modelMatrices[36] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(90)
        stack.gTranslate(0, 1, 1.5)
        modelMatrices[37] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(90)
        stack.gTranslate(1, 1, 1.5)
        modelMatrices[38] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(90)
        stack.gTranslate(-1, 0, 1.5)
        modelMatrices[39] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(90)
        stack.gTranslate(0, 0, 1.5)
        modelMatrices[40] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(90)
        stack.gTranslate(1, 0, 1.5)
        modelMatrices[41] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(90)
        stack.gTranslate(-1, -1, 1.5)
        modelMatrices[42] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(90)
        stack.gTranslate(0, -1, 1.5)
        modelMatrices[43] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(90)
        stack.gTranslate(1, -1, 1.5)
        modelMatrices[44] = stack.modelMatrix
        stack.gPop()

        # BACK FACE
        stack.gPush()
        stack.gRotateY(180)
        stack.gTranslate(-1, 1, 1.5)
        modelMatrices[45] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(180)
        stack.gTranslate(0, 1, 1.5)
        modelMatrices[46] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(180)
        stack.gTranslate(1, 1, 1.5)
        modelMatrices[47] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(180)
        stack.gTranslate(-1, 0, 1.5)
        modelMatrices[48] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(180)
        stack.gTranslate(0, 0, 1.5)
        modelMatrices[49] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(180)
        stack.gTranslate(1, 0, 1.5)
        modelMatrices[50] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(180)
        stack.gTranslate(-1, -1, 1.5)
        modelMatrices[51] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(180)
        stack.gTranslate(0, -1, 1.5)
        modelMatrices[52] = stack.modelMatrix
        stack.gPop()

        stack.gPush()
        stack.gRotateY(180)
        stack.gTranslate(1, -1, 1.5)
        modelMatrices[53] = stack.modelMatrix
        stack.gPop()

        return modelMatrices
