import cProfile
import pstats
import sys

from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWidgets import QApplication

from .gui import CubeDetectionAppWindow


def main():
    with cProfile.Profile() as profile:
        run()

    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.dump_stats("rubiksolver.prof")


def run():
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    QSurfaceFormat.setDefaultFormat(fmt)

    app = QApplication(sys.argv)
    window = CubeDetectionAppWindow()
    window.setMinimumSize(1600, 900)
    window.show()
    window.move(0, 0)
    sys.exit(app.exec())
