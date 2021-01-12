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
        self.intent = Intent(intentName)
        self.promptMode = "addUtterance"

        while self.promptMode != "quit":
            subprocess.run("clear")
            print(self.output)
            self.setIntentPrompt()
            command = input(self.prompt)

            if self.promptMode == "addUtterance":
                if command == "q":
                    if len(self.intent.utterances) >= 1:
                        self.promptMode = "chooseUtterance"
                elif command == "undo":
                    if len(self.intent.utterances) >= 1:
                        del(intent.utterances[-1])
                else:
                    self.addUtterances(command)

                self.getIntentOutput()
                self.setIntentPrompt()
            elif self.promptMode == "chooseUtterance":
                if command == "q":
                    self.promptMode = "slot"
                else:
                    self.chooseUtterance(command)

                self.getIntentOutput()
                self.setIntentPrompt()
            elif self.promptMode == "slot":
                if command == "q":
                    self.promptMode = "slotType"
                else:
                    self.addSlots(command)

                self.getIntentOutput()
                self.setIntentPrompt()
            elif self.promptMode == "slotType":
                self.promptMode = "quit"#FIXME: Implement slot typing.
                                        # Every slot needs a type.

    def getIntentOutput(self):
        if self.promptMode == "addUtterance":
            if self.errorMsg == "":
                self.output = "'{}'\n".format(self.intent.utterances[-1]) \
                                + "Looks good."
            else:
                self.output = self.errorMsg
        elif self.promptMode == "chooseUtterance":
            if self.errorMsg == "":
                self.output = "Please pick one of the following utterances " + \
                            "to add slots to it.\n(Enter 'q' to skip this)\n"
                for i in range(0, len(self.intent.utterances), 1):
                    self.output += "{}. '{}'\n".format(i, self.intent.utterances[i])
            else:
                self.output = self.errorMsg
        elif self.promptMode == "slot":
            if self.errorMsg == "":
                self.output = "Selected utterance: {}".format(self.intent.currUtterance)
            else:
                self.output = self.errorMsg

    def setIntentPrompt(self):
        if self.promptMode == "addUtterance":
            if len(self.intent.utterances) == 0:
                self.prompt = "Please start by adding at least one sample " + \
                "utterance\n(type 'rules' to learn more about how to write an utterance):\n"
            else:
                self.prompt = \
                "Enter another utterance or enter 'q' to start creating slots:\n"
        elif self.promptMode == "chooseUtterance":
            self.prompt = "Please enter an utterance number: "
        elif self.promptMode == "slot":
            slots = self.intent.currUtterance.grabSlots()
            self.prompt = "Your current slots are " + str(slots) + "\n"\
            "If you wish to add more, enter the word you want to replace.\n" +\
            "(Enter 'q' if you are done adding slots.): "
            

    def addUtterances(self, command):
        # Reading and processing the input
        if self.intent.checkUtterance(command) != "":
            self.errorMsg = self.intent.checkUtterance(command)
        else:
            self.errorMsg = ""
            self.intent.addUtterance(command)
            print(self.intent.utterances)

    # Allows the user to choose which utternacne they wish to modify
    def chooseUtterance(self, command):
        self.errorMsg = self.intent.setCurrUtterance(command)
        if self.errorMsg == "":
            self.promptMode = "slot"

    def addSlots(self, command):
        #FIXME: This needs input twice. Will be complicated to make.
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
