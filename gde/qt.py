#
# This hidden module contains shared GUI elements used by GDE.
#
# This file is part of GDE.
# See https://github.com/MichaelClerx/gde for sharing, and licensing details.
#
import signal
import sys

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt


# Fix PyQt naming issues
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot
QtCore.Property = QtCore.pyqtProperty


# Stand alone applications
class Application(QtWidgets.QMainWindow):
    """
    Base class for GDE applications.

    *Extends*: ``QtWidgets.QMainWindow``.
    """


def run(app, *args):
    """
    Runs a :class:`GDEApplication` as a stand-alone application.

    Arguments:

    ``app``
        The application to run, specified as a class object (not an instance).
    ``*args``
        Any arguments to pass to the app's constructor.

    Example usage:

        load(gde.GraphDataExtractor, 'file.gde')


    """
    # Test application class
    if not issubclass(app, Application):
        raise ValueError(
            'Application must be a subclass of GDEkitApplication.')

    # Create Qt app
    a = QtWidgets.QApplication([])

    # Apply custom styling if required
    #_style_application(a)
    # Close with last window
    a.lastWindowClosed.connect(a.quit)

    # Close on Ctrl-C
    def int_signal(signum, frame):
        a.closeAllWindows()
    signal.signal(signal.SIGINT, int_signal)

    # Create app and show
    app = app(*args)
    app.show()

    # For some reason, Qt needs focus to handle the SIGINT catching...
    timer = QtCore.QTimer()
    timer.start(500)  # Flags timeout every 500ms
    timer.timeout.connect(lambda: None)

    # Wait for app to exit
    sys.exit(a.exec_())

