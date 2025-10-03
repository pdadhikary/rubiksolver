import numpy as np
import pyrr


class ModelMatrixStack:
    def __init__(self):
        self._modelStack: list[np.ndarray] = []
        self._modelMatrix: np.ndarray = pyrr.matrix44.create_identity(np.float32)

    @property
    def modelMatrix(self) -> np.ndarray:
        return self._modelMatrix.copy()

    def gPush(self):
        self._modelStack.append(self._modelMatrix)

    def gPop(self):
        if len(self._modelStack) <= 0:
            return
        self._modelMatrix = self._modelStack.pop()

    def gRotateX(self, deg=0.0):
        self._modelMatrix = pyrr.matrix44.multiply(
            m1=pyrr.matrix44.create_from_x_rotation(np.radians(deg), dtype=np.float32),
            m2=self._modelMatrix,
        )

    def gRotateY(self, deg=0.0):
        self._modelMatrix = pyrr.matrix44.multiply(
            m1=pyrr.matrix44.create_from_y_rotation(np.radians(deg), dtype=np.float32),
            m2=self._modelMatrix,
        )

    def gRotateZ(self, deg=0.0):
        self._modelMatrix = pyrr.matrix44.multiply(
            m1=pyrr.matrix44.create_from_z_rotation(np.radians(deg), dtype=np.float32),
            m2=self._modelMatrix,
        )

    def gReflectXY(self):
        self._modelMatrix = pyrr.matrix44.multiply(
            m1=np.diag([1.0, 1.0, -1.0, 1.0]).astype(np.float32),
            m2=self._modelMatrix,
        )

    def gReflectXZ(self):
        self._modelMatrix = pyrr.matrix44.multiply(
            m1=np.diag([1.0, -1.0, 1.0, 1.0]).astype(np.float32),
            m2=self._modelMatrix,
        )

    def gReflectYZ(self):
        self._modelMatrix = pyrr.matrix44.multiply(
            m1=np.diag([-1.0, 1.0, 1.0, 1.0]).astype(np.float32),
            m2=self._modelMatrix,
        )

    def gTranslate(self, x=0.0, y=0.0, z=0.0):
        self._modelMatrix = pyrr.matrix44.multiply(
            m1=pyrr.matrix44.create_from_translation(
                np.array([x, y, z]), dtype=np.float32
            ),
            m2=self._modelMatrix,
        )

    def gScale(self, sx=1.0, sy=1.0, sz=1.0):
        self._model_matrix = pyrr.matrix44.multiply(
            m1=pyrr.matrix44.create_from_scale(
                np.array([sx, sy, sz]), dtype=np.float32
            ),
            m2=self._model_matrix,
        )

    def gEuler(self, pitch=0.0, roll=0.0, yaw=0.0):
        self._model_matrix = pyrr.matrix44.multiply(
            m1=pyrr.matrix44.create_from_eulers(
                eulers=pyrr.euler.create(
                    pitch=np.radians(pitch),
                    roll=np.radians(roll),
                    yaw=np.radians(yaw),
                ),
                dtype=np.float32,
            ),
            m2=self._model_matrix,
        )
