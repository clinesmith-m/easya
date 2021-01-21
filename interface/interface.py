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
        self.helpMsg = ""
        self.command = ""
        self.prevCommand = ""
        self.currSlot = None


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
            if self.helpMsg != "":
                print(self.helpMsg)
            else:
                print(self.output)
            self.setIntentPrompt()
            self.prevCommand = self.command
            self.command = input(self.prompt)
            self.helpMsg = ""

            if self.promptMode == "addUtterance":
                if self.command == "q":
                    if len(self.intent.utterances) >= 1:
                        self.promptMode = "chooseUtterance"
                elif self.command == "undo":
                    if len(self.intent.utterances) >= 1:
                        del(intent.utterances[-1])
                else:
                    self.addUtterances()

            elif self.promptMode == "chooseUtterance":
                if self.command == "q":
                    self.promptMode = "slotType"
                else:
                    self.chooseUtterance()

            elif self.promptMode == "chooseSlotWord":
                if self.command == "q":
                    self.promptMode = "chooseUtterance"
                else:
                    self.chooseSlotWord()
                    if self.errorMsg == "":
                        self.promptMode = "chooseSlotName"

            elif self.promptMode == "chooseSlotName":
                self.replaceSlotWord()

            elif self.promptMode == "slotType":
                if self.currSlot != None and self.command == "custom":
                    self.promptMode = "CustomSlotType"
                elif self.command == "defaults":
                    self.listSlotTypes()
                else:
                    self.addSlotTypes()
            elif self.promptMode == "CustomSlotType":
                #TODO: Implement this
                break

            else:
                print("Mistakes were made")
                break

            self.getIntentOutput()
 

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
        elif self.promptMode == "chooseSlotWord":
            if self.errorMsg == "":
                self.output = "Selected utterance: {}".format(self.intent.currUtterance)
            else:
                self.output = self.errorMsg
        elif self.promptMode == "chooseSlotName":
            if self.errorMsg == "":
                self.output = str(self.intent.currUtterance)
                self.output = \
                    self.output.replace(self.command, "[Selected Word]", 1)
            else:
                self.output = self.errorMsg
        elif self.promptMode == "slotType":
            self.output = "(This will keep running until every slot has a type)\n"
            self.output += "The current slot is [{}]".format(self.currSlot)
        else:
            self.output = "Under Construction"

    def setIntentPrompt(self):
        if self.promptMode == "addUtterance":
            if len(self.intent.utterances) == 0:
                self.prompt = "Please start by adding at least one sample " + \
                "utterance\n" +\
                "(enter 'rules' to learn more about how to write an utterance):\n"
            else:
                self.prompt = \
                "Enter another utterance or enter 'q' to start creating slots:\n"
        elif self.promptMode == "chooseUtterance":
            self.prompt = "Please enter an utterance number: "
        elif self.promptMode == "chooseSlotWord":
            slots = self.intent.currUtterance.grabSlots()
            self.prompt = "The current slots in the utterance are "\
                + str(slots) + "\n"\
                "If you wish to add more, enter the word you want to replace.\n" +\
                "(Enter 'q' if you are done adding slots.): "
        elif self.promptMode == "chooseSlotName":
            intentSlots = self.intent.grabIntentSlots()
            self.prompt = "Current slots you have in your intent are {}\n"\
                .format(str(intentSlots)) + "Enter the name of this slot: "
        elif self.promptMode == "slotType":
            self.prompt = \
            "Please enter a built-in type for this slot or enter " +\
            "'custom' to create a custom type.\n" +\
            "(Enter 'defaults' to see a list of built-in slot types): "
        else:
            self.prompt = "Under Construction"
            

    def addUtterances(self):
        # Reading and processing the input
        if self.intent.checkUtterance(self.command) != "":
            self.errorMsg = self.intent.checkUtterance()
        else:
            self.errorMsg = ""
            self.intent.addUtterance(self.command)

    # Allows the user to choose which utternacne they wish to modify
    def chooseUtterance(self):
        self.errorMsg = self.intent.setCurrUtterance(self.command)
        if self.errorMsg == "":
            self.promptMode = "chooseSlotWord"

    def chooseSlotWord(self):
        self.errorMsg = self.intent.currUtterance.findWord(self.command)
        if self.errorMsg == "":
            self.promptMode = "chooseSlotName"

    def replaceSlotWord(self):
        self.errorMsg = \
            self.intent.currUtterance.replaceWord(self.prevCommand, self.command)
        if self.errorMsg == "":
            self.promptMode = "chooseSlotWord"

    # This is pretty bad computationally, but that shouldn't really matter and
    # this does make the code cleaner... I think.
    def addSlotTypes(self):
        if self.currSlot == None:
            intentSlots = self.intent.grabIntentSlots()
            for slot in intentSlots:
                if slot.type == None:
                    self.currSlot = slot
                    break
            # If currSlot is still none, it's time to exit the program
            if self.currSlot == None:
                self.promptMode = "quit"
        else:
            self.currSlot.declareType(self.command)
            self.currSlot = None

    def listSlotTypes(self):
        self.helpMsg = "Coming soon"

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
