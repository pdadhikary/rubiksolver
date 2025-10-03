import ctypes

import numpy as np
import OpenGL.GL as gl
import pyrr
from OpenGL.GL.shaders import ShaderProgram, compileProgram, compileShader
from PySide6.QtCore import QElapsedTimer, Qt, QTimer, Slot
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QGridLayout, QSlider, QWidget

from rubiksolver.cube import CubeLabel
from rubiksolver.gui.mesh import RubiksCubeMesh


class Cube3DViewerWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.cubeWidget = CubeGLWidget()

        self.cameraPitchSlider = QSlider(Qt.Orientation.Vertical)
        self.cameraPitchSlider.setRange(
            self.cubeWidget.cameraPitch - 180, self.cubeWidget.cameraPitch + 180
        )
        self.cameraPitchSlider.setValue(self.cubeWidget.cameraPitch)

        self.cameraRollSlider = QSlider(Qt.Orientation.Horizontal)
        self.cameraRollSlider.setRange(
            self.cubeWidget.cameraRoll - 180, self.cubeWidget.cameraRoll + 180
        )
        self.cameraRollSlider.setValue(self.cubeWidget.cameraRoll)

        self.cameraYawSlider = QSlider(Qt.Orientation.Horizontal)
        self.cameraYawSlider.setRange(
            self.cubeWidget.cameraYaw - 180, self.cubeWidget.cameraYaw + 180
        )
        self.cameraYawSlider.setValue(self.cubeWidget.cameraYaw)

        self.cameraPitchSlider.valueChanged.connect(self.cubeWidget.setCameraPitch)
        self.cameraRollSlider.valueChanged.connect(self.cubeWidget.setCameraRoll)
        self.cameraYawSlider.valueChanged.connect(self.cubeWidget.setCameraYaw)

        layout = QGridLayout(self)
        layout.addWidget(self.cameraPitchSlider, 1, 0)
        layout.addWidget(self.cameraRollSlider, 0, 1)
        layout.addWidget(self.cameraYawSlider, 2, 1)
        layout.addWidget(self.cubeWidget, 1, 1)

    def cleanup(self):
        self.cubeWidget.cleanup()


class CubeGLWidget(QOpenGLWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.cameraPitch = -45
        self.cameraRoll = 0  # -45
        self.cameraYaw = 45  # 45

        self.cubeLabels: list[CubeLabel] = [CubeLabel.UNLABELD for _ in range(54)]

        self.baseViewMatrix = pyrr.matrix44.create_look_at(
            eye=np.array([0.0, 0.0, 10.0], dtype=np.float32),
            target=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            up=np.array([0.0, 1.0, 0.0], dtype=np.float32),
            dtype=np.float32,
        )

        # temp proerty
        self.angle = 0.0

        self.deltaTime = 0.0
        self.elapsed = QElapsedTimer()
        self.elapsed.start()

        self.renderTimer = QTimer(self, interval=16)
        self.renderTimer.setTimerType(Qt.TimerType.PreciseTimer)
        self.renderTimer.timeout.connect(self.renderUpdate)
        self.renderTimer.start()

    def initializeGL(self) -> None:
        print(f"OpenGL version: {gl.glGetString(gl.GL_VERSION)}")
        self.cubeMesh = RubiksCubeMesh()

        self.aspect = self.size().width() / self.size().height()

        self.program = CubeGLWidget.loadProgram(
            "src/shaders/shader.vert", "src/shaders/shader.frag"
        )
        gl.glUseProgram(self.program)

        self.projectionUniformLocation = gl.glGetUniformLocation(
            self.program, "projection"
        )
        self.viewUniformLocation = gl.glGetUniformLocation(self.program, "view")

        self.cubeVAO = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.cubeVAO)

        self.meshVBO = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.meshVBO)
        vertices = self.cubeMesh.vertices
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW
        )

        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 32, ctypes.c_void_p(0))

        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(
            1, 2, gl.GL_FLOAT, gl.GL_FALSE, 32, ctypes.c_void_p(12)
        )

        gl.glEnableVertexAttribArray(2)
        gl.glVertexAttribPointer(
            2, 3, gl.GL_FLOAT, gl.GL_FALSE, 32, ctypes.c_void_p(20)
        )

        self.modelVBO = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.modelVBO)
        modelMatrices = self.cubeMesh.modelMatices
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, modelMatrices.nbytes, modelMatrices, gl.GL_STATIC_DRAW
        )

        gl.glEnableVertexAttribArray(3)
        gl.glVertexAttribPointer(3, 4, gl.GL_FLOAT, gl.GL_FALSE, 64, ctypes.c_void_p(0))
        gl.glVertexAttribDivisor(3, 1)

        gl.glEnableVertexAttribArray(4)
        gl.glVertexAttribPointer(
            4, 4, gl.GL_FLOAT, gl.GL_FALSE, 64, ctypes.c_void_p(16)
        )
        gl.glVertexAttribDivisor(4, 1)

        gl.glEnableVertexAttribArray(5)
        gl.glVertexAttribPointer(
            5, 4, gl.GL_FLOAT, gl.GL_FALSE, 64, ctypes.c_void_p(32)
        )
        gl.glVertexAttribDivisor(5, 1)

        gl.glEnableVertexAttribArray(6)
        gl.glVertexAttribPointer(
            6, 4, gl.GL_FLOAT, gl.GL_FALSE, 64, ctypes.c_void_p(48)
        )
        gl.glVertexAttribDivisor(6, 1)

        self.colorVBO = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.colorVBO)
        colorData = self.cubeMesh.getColorData(self.cubeLabels)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, colorData.nbytes, colorData, gl.GL_STATIC_DRAW
        )

        gl.glEnableVertexAttribArray(7)
        gl.glVertexAttribPointer(7, 3, gl.GL_FLOAT, gl.GL_FALSE, 12, ctypes.c_void_p(0))
        gl.glVertexAttribDivisor(7, 1)

        gl.glBindVertexArray(0)

        gl.glEnable(gl.GL_DEPTH_TEST)

    def paintGL(self) -> None:
        gl.glClearColor(0.2, 0.2, 0.2, 1.0)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))
        gl.glUseProgram(self.program)

        projectionMatrix = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=self.aspect, near=0.1, far=20, dtype=np.float32
        )
        gl.glUniformMatrix4fv(
            self.projectionUniformLocation, 1, gl.GL_FALSE, projectionMatrix
        )

        view_matrix = pyrr.matrix44.multiply(
            m1=pyrr.matrix44.create_from_eulers(
                np.array(
                    [
                        np.radians(self.cameraPitch),
                        np.radians(self.cameraRoll),
                        np.radians(self.cameraYaw),
                    ],
                    dtype=np.float32,
                ),
                dtype=np.float32,
            ),
            m2=self.baseViewMatrix,
        )
        gl.glUniformMatrix4fv(self.viewUniformLocation, 1, gl.GL_FALSE, view_matrix)

        gl.glBindVertexArray(self.cubeVAO)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.colorVBO)
        colorData = self.cubeMesh.getColorData(self.cubeLabels)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, colorData.nbytes, colorData)

        gl.glDrawArraysInstanced(
            gl.GL_TRIANGLES, 0, self.cubeMesh.nvertices, self.cubeMesh.ninstances
        )

        gl.glBindVertexArray(0)

    def resizeGL(self, w: int, h: int) -> None:
        if h == 0:
            h = 1
        gl.glViewport(0, 0, w, h)
        self.aspect = w / h

    def cleanup(self):
        print("OpenGL Cleanup...")
        self.makeCurrent()
        try:
            self.renderTimer.stop()
            gl.glDeleteVertexArrays(1, self.cubeVAO)
            gl.glDeleteBuffers(1, self.meshVBO)
            gl.glDeleteBuffers(1, self.modelVBO)
            gl.glDeleteBuffers(1, self.colorVBO)
            gl.glDeleteProgram(self.program)
        finally:
            self.doneCurrent()

    def setCubeLabels(self, labels: list[CubeLabel]):
        self.cubeLabels = labels

    @Slot(int)
    def setCameraPitch(self, value: int):
        self.cameraPitch = value

    @Slot(int)
    def setCameraRoll(self, value: int):
        self.cameraRoll = value

    @Slot(int)
    def setCameraYaw(self, value: int):
        self.cameraYaw = value

    @Slot()
    def renderUpdate(self):
        self.deltaTime = self.elapsed.restart() / 1000.0
        self.update()

    @staticmethod
    def loadProgram(
        vertex_shader_path: str, fragment_shader_path: str
    ) -> ShaderProgram:
        vertex_shader_content = CubeGLWidget.loadShaderFile(vertex_shader_path)
        fragment_shader_content = CubeGLWidget.loadShaderFile(fragment_shader_path)

        return compileProgram(
            compileShader(vertex_shader_content, gl.GL_VERTEX_SHADER),
            compileShader(fragment_shader_content, gl.GL_FRAGMENT_SHADER),
        )

    @staticmethod
    def loadShaderFile(shader_path: str) -> str:
        with open(shader_path, "r") as file:
            shader_content = file.readlines()

        return "".join(shader_content)
