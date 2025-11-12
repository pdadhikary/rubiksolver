import argparse
import cProfile
import pstats
import sys

from PySide6.QtWidgets import QApplication

from .gui import CubeDetectionAppWindow


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug", action="store_true", help="Run the program in debug mode."
    )
    args = parser.parse_args()

    if args.debug:
        print("Running in debug mode")
        with cProfile.Profile() as profile:
            run(True)
        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.TIME)
        results.dump_stats("rubiksolver.prof")
    else:
        run(False)


def run(debug: bool):
    app = QApplication(sys.argv)
    window = CubeDetectionAppWindow(debug)
    window.setMinimumSize(1600, 900)
    window.show()
    window.move(0, 0)
    sys.exit(app.exec())
