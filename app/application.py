"""Application bootstrap helpers for the Sound Converter GUI."""

from __future__ import annotations

import sys
from typing import Tuple

from PySide6.QtWidgets import QApplication

from .converter import SoundConverter
from .ui_main import MainWindow


def create_application() -> Tuple[QApplication, MainWindow]:
    """Instantiate the Qt application and main window."""

    app = QApplication(sys.argv)
    window = MainWindow(SoundConverter())
    return app, window


def run() -> int:
    """Create the application and start the Qt event loop."""

    app, window = create_application()
    window.show()
    return app.exec()


__all__ = ["create_application", "run"]
