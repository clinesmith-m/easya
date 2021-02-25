import os
import subprocess
from pathlib import *

class Initializer():
    def __init__(self, name):
        self.proj_name = name


    def __cloneSDK(self, projPath, sdkPath):
        for child in sdkPath.iterdir():
            currPath = projPath / child.name
            currPath.symlink_to(child)


    def run(self):
        os.mkdir(self.proj_name)
        currPath = Path(self.proj_name)
        sdkPath = Path("/home/michael/alexasrc")
        self.__cloneSDK(currPath, sdkPath)


if __name__ == "__main__":
    initer = Initializer("new_proj")
    initer.run()
