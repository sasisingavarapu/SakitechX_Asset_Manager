"""

try:
   import importlib;from importlib import reload
except:
    import imp;from imp import reload

import SakitechX_Asset_Manager
from SakitechX_Asset_Manager.ui.asset_manager import load_asset_manager
reload(load_asset_manager)

cSakitechXAssetManager = load_asset_manager.SakitechXAssetManager()
cSakitechXAssetManager.show()

"""
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtUiTools import QUiLoader  # ✅ This is needed
from shiboken6 import wrapInstance
import os

import maya.OpenMayaUI as omui
from maya import cmds, mel

TITLE = 'SakitechX Asset Manager'
UI_FILE = 'asset_manager.ui'
FULL_PATH = os.path.dirname(__file__)
QT_PATH =os.path.join(FULL_PATH, UI_FILE)


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class SakitechXAssetManager(QtWidgets.QMainWindow):
    def __init__(self, parent=maya_main_window()):
        super(SakitechXAssetManager, self).__init__(parent)

        self.setWindowTitle(TITLE)

        self.init_ui()
        self.create_layout()
        self.create_connections()

    def init_ui(self):
        # Load UI file
        loader = QUiLoader()
        file = QtCore.QFile(QT_PATH)
        file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)
        file.close()

    def create_layout(self):
        self.resize(800,400)

    def create_connections(self):
        ''

if __name__ == "__main__":
    try:
        cSakitechXAssetManager.close()
        cSakitechXAssetManager.deleteLater()
    except Exception as e:
        print("An error occurred: {}".format(e))

    cSakitechXAssetManager = SakitechXAssetManager()
    cSakitechXAssetManager.show()



