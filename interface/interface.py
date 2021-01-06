import os
import subprocess
from sys import argv
from intents.addIntent import Intent, Utterance, Slot

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
        print("Type 'help' at any time for more information")
        intentName = input("What is the name of your new intent?\n")
        # I intend to clear the screen after every command to avoid overloading
        # the user with information. I'm saving the output of each command in
        # this variable to be printed after the screen is cleared.
        self.output = "The name of your intent is '{}'. ".format(intentName) + \
                "Change it at any time by typing 'change intent name'."

        self.intent = AddIntent(intentName)
        self.prompt = "Please start by adding at least one sample utterance " + \
            "(type 'rules' to learn more about how to write an utterance):\n"

        promptMode = "utterance"
        while promptMode != "quit":
            subprocess.run("clear")
            print(self.output)
            command = input(self.prompt)

            if promptMode == "utterance":
                self.addUtterances(command)
            if promptMode == "slot":
                self.addSlots(command)

    def addUtterances(self, command):
        # Allowing the user to perform actions other than entering
        # utterances
        if len(intent.utterances) >= 1:
            if command == "q":
                promptMode = "slot"
            elif command == "undo":
                del(intent.utterances[-1])

        # Reading and processing the input
        elif intent.checkUtterance(command) != "":
            errorString = intent.checkUtterance(command)
            self.output = errorString
        else:
            intent.addUtterance(command)
            self.output = "'{}'\n".format(command) + "Looks good."
            self.prompt = \
            "Enter another utterance or enter 'q' to start creating slots:\n"

    # Creates an intuitive prompt/interface for the user to add slots to
    # specific utternaces
    def processUtterance(self, command):
        self.intent.currUtterance.grabSlots()
        

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
