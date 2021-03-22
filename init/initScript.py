import os
import subprocess
from pathlib import *

class Initializer():
    def __init__(self, name="new_proj"):
        self.proj_name = name


    def run(self):
        os.mkdir(self.proj_name)
        currPath = Path(self.proj_name)


if __name__ == "__main__":
    initer = Initializer("new_proj")
    initer.run()
