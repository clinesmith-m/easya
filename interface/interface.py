import os
import subprocess
import re
from pathlib import *
from sys import argv
from intents.intents import Intent, Utterance, Slot, CustomSlotType, SlotValue
from interface.intentInterface import Intenterface
from interface.initInterface import Initerface
from writers.pywriter import Pywriter
from writers.JSONWriter import JSONWriter

class Interface():
    def __init__(self):
        self.commands = [
            "init", "add-intent", "update-intent", "help", "zip"
        ]


    def __checkForProj(self):
        pathToCheck = Path(".easya")
        if not pathToCheck.is_file():
            print("This Directory is not a properly initialized easyA project")
            print("(No '.easya' file exists)")
            exit(1) 


    def run(self):
        # Erroring if no commands are passed
        if len(argv) == 1:
            self.printUsage()
            exit(1)

        # Rejecting invalid commands
        if argv[1] not in self.commands:
            print("Unknown command '{}'".format(argv[1]))
            print("\nAccepted commands are:\n")
            for cmd in self.commands:
                print("\t{}".format(cmd))
            print()

        # Passing valid commands to handler functions
        if argv[1] == "init":
            self.runInit()
        elif argv[1] == "add-intent":
            self.__checkForProj()
            self.runAddIntent()
        elif argv[1] == "update-intent":
            self.__checkForProj()
            self.runUpdateIntent()
        elif argv[1] == "zip":
            subprocess.run("easyZip")
        elif argv[1] == "help":
            self.help()


    def runInit(self):
        initInterface = Initerface()
        initInterface.run()


    def runAddIntent(self):
        addIntentInterface = Intenterface()
        addIntentInterface.run()
        pywriter = Pywriter(addIntentInterface.intent)
        pywriter.write()
        jsonwriter = JSONWriter(customTypes=addIntentInterface.customSlotTypes,
                            intent=addIntentInterface.intent)
        jsonwriter.writeIntent()

    def runUpdateIntent(self):
        pass


    def help(self):
        print("help doesn't need other objects, so it can just happen here")


    def printUsage(self):
        print("-"*35 + "  Usage:  " + "-"*35)
        print()
        print("easyA <command>")
        print("\nAccepted commands are:\n")
        for cmd in self.commands:
            print("\t{}".format(cmd))
        print()
