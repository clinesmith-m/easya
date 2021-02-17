import os
import subprocess
import re
from sys import argv
from intents.intents import Intent, Utterance, Slot, CustomSlotType, SlotValue
from interface.intentInterface import Intenterface
from writers.pywriter import Pywriter

class Interface():
    def __init__(self):
        self.commands = [
            "compile", "init", "add-intent", "update-intent", "help"
            ]


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
        if argv[1] == "compile":
            subprocess.run("cmake")
        elif argv[1] == "init":
            self.runInit()
        elif argv[1] == "add-intent":
            self.runAddIntent()
        elif argv[1] == "update-intent":
            self.runUpdateIntent()
        elif argv[1] == "help":
            self.help()


    def runInit(self):
        pass


    def runAddIntent(self):
        addIntentInterface = Intenterface()
        addIntentInterface.run()
        pywriter = Pywriter(addIntentInterface.intent)
        pywriter.write()

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
