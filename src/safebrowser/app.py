"""
SafeBrowser Application
Asosiy dastur class
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from safebrowser.ui.main_window import MainWindow


class SafeBrowserApp:
    """
    SafeBrowser dasturi
    """

    def __init__(self, argv: list = None):
        self.argv = argv or sys.argv
        self.app = None
        self.main_window = None

    def run(self) -> int:
        """Dasturni ishga tushirish"""
        # High DPI scaling
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        self.app = QApplication(self.argv)
        self.app.setApplicationName("SafeBrowser")
        self.app.setApplicationVersion("2.0.0")
        self.app.setOrganizationName("SafeBrowser Team")

        # Main window
        self.main_window = MainWindow()
        self.main_window.show()

        return self.app.exec()

    @staticmethod
    def create_app(argv: list = None) -> 'SafeBrowserApp':
        """Factory method"""
        return SafeBrowserApp(argv)


def main():
    """Entry point"""
    app = SafeBrowserApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
