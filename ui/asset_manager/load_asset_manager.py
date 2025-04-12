"""
import SakitechX_Asset_Manager
from SakitechX_Asset_Manager.ui.asset_manager import load_asset_manager



"""

from PySide2 import QtUiTools, QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance
import os

import maya.OpenMayaUI as omui
from maya import cmds, mel


TITLE = 'SakitechX Asset Manager'
UI_FILE = 'asset_manager.ui'
FULL_PATH = __file__

print(FULL_PATH)