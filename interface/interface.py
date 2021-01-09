import os
import subprocess
from sys import argv
from intents.intents import Intent, Utterance, Slot

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
        # Initializing member variables. Python doesn't need this but I do
        self.errorMsg = ""


        print("Type 'help' at any time for more information")
        intentName = input("What is the name of your new intent?\n")
        # I intend to clear the screen after every command to avoid overloading
        # the user with information. I'm saving the output of each command in
        # this variable to be printed after the screen is cleared.
        self.output = "The name of your intent is '{}'. ".format(intentName) + \
                "Change it at any time by typing 'change intent name'."
        #TODO: Refactor this so that it actually kinda makes sense. THen test
        #TODO: It's testing time. Then make slots works
        self.intent = Intent(intentName)
        self.promptMode = "addUtterance"

        while self.promptMode != "quit":
            subprocess.run("clear")
            print(self.output)
            self.setIntentsPrompt()
            command = input(self.prompt)

            if self.promptMode == "addUtterance":
                self.addUtterances(command)
            elif self.promptMode == "chooseUtterance":
                self.chooseUtterance(command)
            elif self.promptMode == "slot":
                self.prepCurrUtterance()
                self.addSlots(command)

    def getIntentsOutput(self):
        if self.promptMode == "addUtterance":
            if self.errorMsg == "":
                self.output = "'{}'\n".format(command) + "Looks good."
            else:
                self.output = self.errorMsg
        elif self.promptMode == "chooseUtterance":
            if self.errorMsg == "":
                self.output = "Selected utterance: {}".format(self.intent.currUtterance)
            else:
                self.output = self.errorMsg

    def setIntentsPrompts(self):
        if self.promptMode == "addUtterance":
            if len(self.intents.utterances) == 0:
            self.prompt = "Please start by adding at least one sample " + \
                "utterance (type 'rules' to learn more about how to write an utterance):\n"
            else:
                self.prompt = \
                "Enter another utterance or enter 'q' to start creating slots:\n"
        elif self.promptMode == "chooseUtterance":
            self.prompt = "Please enter an utterance number: "
        elif self.promptMode == "slots":
            slots = self.intent.currUtterance.grabSlots()
            self.prompt = "Your current slots are " + slots + \
            "If you wish to add more, enter the word you want to replace. (Enter 'q' if don't want to add a slot.): "
            

    def addUtterances(self, command):
        # Allowing the user to perform actions other than entering
        # utterances
        if len(self.intent.utterances) >= 1:
            if command == "q":
                self.promptMode = "chooseUtterance"
            elif command == "undo":
                del(intent.utterances[-1])

        # Reading and processing the input
        elif self.intent.checkUtterance(command) != "":
            self.errorMsg = intent.checkUtterance(command)
        else:
            self.errorMsg = ""
            self.intent.addUtterance(command)

    # Allows the user to choose which utternacne they wish to modify
    def chooseUtterance(self, command):
        self.errorMsg = self.intent.setCurrUtterance(command)

    def addSlots(self, command):
        pass

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
