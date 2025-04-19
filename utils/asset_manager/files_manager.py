"""

try:
   import importlib;from importlib import reload
except:
    import imp;from imp import reload

import SakitechX_Asset_Manager
from SakitechX_Asset_Manager.utils.asset_manager import file_manager

reload(file_manager)

#Get all the files
cFileManager.current_asset = cFileManager.asset[-1]
cFileManager.get_asset_files()

"""
import os
import glob
import json

class FileManager(object):

    def __init__(self, path=False):

        self.config_path = None

        if path:
            self.path = path
        else:
            self.path = self.get_scenes_from_config()
        self.asset = self.get_asset()

        if self.asset:
            self.current_asset = self.asset[0]
        else:
            self.current_asset = None

    def get_scenes_from_config(self):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        grand_parent_dir = os.path.dirname(parent_dir)
        path_to_json = os.path.join(grand_parent_dir, 'path.json')
        self.config_path = path_to_json


        with open(path_to_json, 'r') as f:
            json_data = json.load(f)

        path = json_data['scenes_path']
        return path

    def get_file_in_path(self, path):
        return glob.glob(os.path.join(path, '*'))

    def get_asset(self):
        asset = self.get_file_in_path(self.path)
        real_asset = []
        for a in asset:
            if os.path.exists(os.path.join(a, 'SakitechX.manager')):
                real_asset.append(a)
        return real_asset

    def get_asset_files(self):
        if not self.current_asset:
            return []

        asset_files = {}

        current_asset_folder = self.get_file_in_path(self.current_asset)
        for stage_folder in current_asset_folder:
            if self.get_basename(stage_folder) == 'SakitechX.manager':  # <- corrected
                continue
            asset_files[self.get_basename(stage_folder)] = self.get_file_in_path(stage_folder)

        return asset_files

    def get_basename(self, path):
        return os.path.basename(path)
