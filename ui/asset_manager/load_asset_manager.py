"""
try:
   import importlib;from importlib import reload
except:
    import imp;from imp import reload

import SakitechX_Asset_Manager
from SakitechX_Asset_Manager.ui.asset_manager import load_asset_manager
reload(load_asset_manager)

try:
    cSakitechXAssetManager.close()
except:
    pass

cSakitechXAssetManager = load_asset_manager.SakitechXAssetManager()
cSakitechXAssetManager.show()


"""
import os
import json
from os.path import basename

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtUiTools import QUiLoader
from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui
from maya import cmds, mel
from functools import partial
import glob

try:
    import importlib
    from importlib import reload
except:
    import imp
    from imp import reload

import SakitechX_Asset_Manager
from SakitechX_Asset_Manager.utils.asset_manager import files_manager
reload(files_manager)


TITLE = 'SakitechX Asset Manager'
UI_FILE = 'asset_manager.ui'
FULL_PATH = os.path.dirname(__file__)
QT_PATH = os.path.join(FULL_PATH, UI_FILE)


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class SakitechXAssetManager(QtWidgets.QMainWindow):
    def __init__(self, parent=maya_main_window()):
        super(SakitechXAssetManager, self).__init__(parent)

        self.setWindowTitle(TITLE)

        self.cFileManager = files_manager.FileManager()
        self.stage_tab = None

        self.init_ui()
        self.create_layout()
        self.create_connections()

    def init_ui(self):
        loader = QUiLoader()
        file = QtCore.QFile(QT_PATH)
        file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)
        file.close()

    def create_layout(self):
        self.resize(800, 400)
        self.check_path_exists()
        self.put_path_in_edit_line()
        self.populate_asset_layout()

    def create_connections(self):
        self.ui.select_path_btn.clicked.connect(self.edit_path_line)

    def check_path_exists(self):
        if not os.path.exists(self.cFileManager.path):
            self.ask_window_path()

    def ask_window_path(self):
        dialog = cmds.fileDialog2(dialogStyle=1, fileMode=3, caption="Open")
        if not dialog:
            return False

        path_folder = dialog[0]
        write_json = os.path.join(self.cFileManager.config_path)

        data = {
            "scenes_path": path_folder
        }
        with open(write_json, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.cFileManager.path = path_folder
        return path_folder

    def put_path_in_edit_line(self):
        self.ui.path_line.setText(self.cFileManager.path)

    def edit_path_line(self):
        self.ask_window_path()
        self.put_path_in_edit_line()

    def get_basename(self, path):
        return os.path.basename(path)

    def populate_asset_layout(self):
        main_layout = self.ui.asset_vlayout
        assets = self.cFileManager.asset
        print('Assets:', assets)

        for asset_path in assets:
            basename = self.get_basename(asset_path)
            folder_button = QtWidgets.QPushButton(basename)
            folder_button.setFixedSize(150, 40)

            main_layout.addWidget(folder_button)

            # Button Connet

            stage = self.get_stages(asset_path)
            folder_button.clicked.connect(partial(self.create_tab_stage, stage))


    def get_stages(self, path):
        self.cFileManager.current_asset = path
        asset_stages = self.cFileManager.get_asset_files()
        return asset_stages

    def clean_assets_layout(self):
        ''

    def create_tab_stage(self, stages_dic):
        if self.stage_tab:
            self.stage_tab.setParent(None)
            self.stage_tab = None

        self.stage_tab = QtWidgets.QTabWidget()
        self.ui.asset_details.addWidget(self.stage_tab)

        for stage in stages_dic:
            tab = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(tab)

            scroll = QtWidgets.QScrollArea(self)
            wrap = QtWidgets.QWidget(self)
            list_box = QtWidgets.QVBoxLayout(self)

            for data in stages_dic[stage]:
                if not self.filter_by_ext(path=data):
                    continue
                widget = self.create_file_widget(data)
                layout.addWidget(widget)
                #list_box.addStretch(1)

            wrap.setLayout(list_box)
            scroll.setWidget(wrap)
            layout.addWidget(scroll)

            self.stage_tab.addTab(tab, stage)

    def filter_by_ext(self, path):
        current_ext = self.ui.ext_combo.currentText()
        if current_ext:
            current_ext = current_ext.replace('.', '')
        path_extension = path.split('.')[-1]

        print(current_ext)
        print(path_extension)

        if path_extension == 'ma':
            path_extension = 'mb'

        if current_ext == 'Show_All':
            return True

        elif current_ext.lower() == path_extension.lower():
            return True

        else:
            return False

    def create_file_widget(self, file_path):
        # Create a QWidget to act as a container
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)

        basename = os.path.basename(file_path)

        label = QtWidgets.QLabel(basename)
        label.setToolTip(file_path)
        layout.addWidget(label)

        open_btn = QtWidgets.QPushButton('open')
        import_btn = QtWidgets.QPushButton('import')
        ref_btn = QtWidgets.QPushButton('reference')

        open_btn.clicked.connect(partial(self.file_button_function, 'open', file_path))
        import_btn.clicked.connect(partial(self.file_button_function, 'import', file_path))
        ref_btn.clicked.connect(partial(self.file_button_function, 'reference', file_path))

        for btn in [open_btn, import_btn, ref_btn]:
            btn.setFixedSize(80, 30)
            layout.addWidget(btn)

        return container  # Return the QWidget, not the layout

    def file_button_function(self, action, file_path):
        if action == 'open':
            self.open_file(file_path)
        elif action == 'import':
            self.import_file(file_path)
        elif action == 'reference':
            self.reference_file(file_path)

    def open_file(self, file_path):
        cmds.file(file_path, open=True, force=True)
        print("open file action")

    def import_file(self, file_path):
        cmds.file(file_path, i=True)
        print("import file action")

    def reference_file(self, file_path):
        cmds.file(file_path, reference=True)
        print("reference file action")


if __name__ == "__main__":
    try:
        cSakitechXAssetManager.close()
        cSakitechXAssetManager.deleteLater()
    except Exception as e:
        print("An error occurred: {}".format(e))

    cSakitechXAssetManager = SakitechXAssetManager()
    cSakitechXAssetManager.show()
