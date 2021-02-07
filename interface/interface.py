import os
import subprocess
import re
from sys import argv
from intents.intents import Intent, Utterance, Slot, CustomSlotType, SlotValue

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
        # Initializing member variables.
        self.errorMsg = ""
        self.helpMsg = ""
        self.command = ""
        self.prevCommand = ""
        self.currSlot = None
        self.activeSlotTypes = self.createAmazonSlotTypes()
        self.customSlotTypes = []
        self.currTypeIndex = -1


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
            #subprocess.run("clear")
            print()
            print()
            print()
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
                    self.promptMode = "defaultSlotType"
                    self.setCurrSlot()
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

            elif self.promptMode == "defaultSlotType":
                if self.command == "custom":
                    self.promptMode = "nameCustomType"
                elif self.command == "defaults":
                    self.listSlotTypes()
                else:
                    self.addDefaultType()

            elif self.promptMode == "nameCustomType":
                self.addTypeName()

            elif self.promptMode == "enterVals":
                if self.command == "syn":
                    self.promptMode = "enterSyn"
                elif self.command == "q":
                    self.promptMode = "defaultSlotType"
                else:
                    self.enterSlotVal()

            elif self.promptMode == "enterSyn":
                if self.command == "q":
                    self.promptMode = "enterVals"
                else:
                    valIndex = len(self.customSlotTypes[self.currTypeIndex].values)-1
                    self.enterSlotValSyn(valIndex)

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

        elif self.promptMode == "defaultSlotType":
            if self.errorMsg == "":
                self.output = "(This will keep running until every slot has a type)\n"
                self.output += "The current slot is [{}]".format(self.currSlot)
            else:
                self.output = self.errorMsg + "\n"
                self.output += "(This will keep running until every slot has a type)\n"
                self.output += "The current slot is [{}]".format(self.currSlot)

        elif self.promptMode == "nameCustomType":
            self.output = "Creating a custom slot type..."

        elif self.promptMode == "enterVals":
            self.output = \
                "Please enter the potential values for this slot type\n"
            if len(self.customSlotTypes[self.currTypeIndex].values) == 0:
                self.output += \
                "(e.g. An ACTIVITIES slot type could have values like camping,\n"\
                + "biking and skiing.)"
            else:
                valString = ""
                for val in self.customSlotTypes[self.currTypeIndex].values:
                    valString += val.value + ", "
                valString = valString.strip(", ")

                self.output += "Current values for type '{}' are: [{}]"\
                    .format(self.customSlotTypes[self.currTypeIndex].typeName,\
                    valString)

        elif self.promptMode == "enterSyn":
            currCustVal = self.customSlotTypes[self.currTypeIndex].values[-1]
            self.output = "Entering synonym for '{}'"\
            .format(currCustVal.value)
            if len(currCustVal.synonyms) > 0:
                self.output += "\nCurrent synonyms are: "\
                            + str(currCustVal.synonyms)

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

        elif self.promptMode == "defaultSlotType":
            self.prompt = \
            "Please enter a built-in type for this slot or enter " +\
            "'custom' to create a custom type.\n" +\
            "(Enter 'defaults' to see a list of built-in slot types): "

        elif self.promptMode == "nameCustomType":
            self.prompt = "Please enter a name for your custom type: "

        elif self.promptMode == "enterVals":
            self.prompt = \
            "Enter a new value (enter 'syn' to add a synonym to the previous\n"\
            + "value or 'q' to quit): "

        elif self.promptMode == "enterSyn":
            self.prompt = "(Enter 'q' to cancel this): "

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


    def setCurrSlot(self):
        self.currSlot = None
        intentSlots = self.intent.grabIntentSlots()
        for slot in intentSlots:
            if slot.type == "":
                self.currSlot = slot
                break
        # If currSlot is still none, it's time to exit the program
        if self.currSlot == None:
            self.promptMode = "quit"


    def addDefaultType(self):
        if self.command in self.activeSlotTypes:
            self.currSlot.declareType(self.command)
            self.setCurrSlot()
        else:
            self.errorMsg = "'{}' is not a valid default slot type."\
                                .format(self.command)


    def addTypeName(self):
        # I don't like doing error handling in the interface, but I'd rather do
        # it here than in the constructor for now
        if not re.match(r'^[A-Za-z_]+$', self.command):
            self.errorMsg = \
                "Slot type names must only contain letters and underscores"
            return

        # Adding the new type to activeSlotTypes in string form
        self.activeSlotTypes.append(self.command)
        # Then creating the new type
        newType = CustomSlotType(self.command)
        self.customSlotTypes.append(newType)
        self.currTypeIndex = len(self.customSlotTypes) - 1
        self.errorMsg = ""
        self.promptMode = "enterVals"
        # Then setting the slot type
        self.currSlot.declareType(self.command)
        self.setCurrSlot()


    def listSlotTypes(self):
        self.helpMsg = "Coming soon"


    def enterSlotVal(self):
        currType = self.customSlotTypes[self.currTypeIndex]
        errorMsg = currType.checkVal(self.command)
        if errorMsg != "":
            return

        newVal = SlotValue(self.command)
        currType.addValue(newVal)
        self.customSlotTypes[self.currTypeIndex] = currType


    def enterSlotValSyn(self, index):
        currVal = self.customSlotTypes[self.currTypeIndex].values[index]
        errorMsg = currVal.addSynonym(self.command)


    def createAmazonSlotTypes(self):
        #TODO: add the actual types

        # Writing it this way to make it easier to add Amazon slot types as I
        # find out about them
        defaultSlotTypes = []
        return defaultSlotTypes


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
