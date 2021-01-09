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
        print("Type 'help' at any time for more information")
        intentName = input("What is the name of your new intent?\n")
        # I intend to clear the screen after every command to avoid overloading
        # the user with information. I'm saving the output of each command in
        # this variable to be printed after the screen is cleared.
        self.output = "The name of your intent is '{}'. ".format(intentName) + \
                "Change it at any time by typing 'change intent name'."
        #TODO: Refactor this so that it actually kinda makes sense. THen test
        self.intent = Intent(intentName)
        self.prompt = "Please start by adding at least one sample utterance " + \
            "(type 'rules' to learn more about how to write an utterance):\n"
        self.promptMode = "addUtterance"

        while self.promptMode != "quit":
            subprocess.run("clear")
            print(self.output)
            command = input(self.prompt)

            if self.promptMode == "addUtterance":
                self.addUtterances(command)
            elif self.promptMode == "chooseUtterance":
                if command == "q":
                    pass #FIXME: Skip past slots
                else:
                    self.chooseUtterance(command)
            elif self.promptMode == "slot":
                self.prepCurrUterance()
                self.addSlots(command)

    

    def setIntentsPrompts(self, mode):
        if mode == "addUtterance":
            self.prompt = \
            "Enter another utterance or enter 'q' to start creating slots:\n"
        elif mode == "chooseUtterance":
            self.prompt = "Please enter an utterance number: "
            

    def addUtterances(self, command):
        # Allowing the user to perform actions other than entering
        # utterances
        if len(intent.utterances) >= 1:
            if command == "q":
                self.promptMode = "chooseUtterance"
            elif command == "undo":
                del(intent.utterances[-1])

        # Reading and processing the input
        elif intent.checkUtterance(command) != "":
            errorString = intent.checkUtterance(command)
            self.output = errorString
        else:
            intent.addUtterance(command)
            self.output = "'{}'\n".format(command) + "Looks good."

    # Allows the user to choose which utternacne they wish to modify
    def chooseUtterance(self, command):
        # Choosing the correct utterance to modify if the user has, in fact,
        # picked an utterance to modify
        if command != "q":
            try:
                self.currUtteranceIndex = int(command)
                if self.currUtteranceIndex > len(self.intent.utterances):
                    self.output = "'" + command + "' is not a valid index number."
                else:
                    self.promptMode = "slot"
            except:
                self.output = "'" + command + "' is not a valid index number."
        else:
            self.output = "Select one of the following utterances to add slots to it. If you don't wish to add slots to any, enter 'q'.\n"
            for i in range(0, len(self.intent.utterances), 1):
                self.output += i + ". " + self.intent.utterances[i] + "\n"

    # Creates an intuitive prompt/interface for the user to add slots to
    # specific utternaces
    def prepCurrUtterance(self):
        slots = self.intent.utterances[self.currUtteranceIndex].grabSlots()
        self.output = "Selected utterance: {}"\
            .format(self.utterances[self.currUtteranceIndex])
        self.prompt = "Your current slots are " + slots + \
                "If you wish to add more, enter the word you want to replace. (Enter 'q' if don't want to add a slot.): "

    def addSlots(self, command):
        if command == "q":
            #TODO: Change to next mode (I think it's just slot type and done)
            print("Work left to do")
        elif command == "change utterance":
            self.promptMode = "chooseUtterance"
        else:
        phrase = self.intent.utterances[self.currUtteranceIndex]
        if 

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
