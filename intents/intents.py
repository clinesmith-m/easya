class Intent():
    def __init__(self, name):
        self.intentName = name
        self.utterances = []
        self.intentSlots = []
        self.currUtterance = None

    def changeIntentName(self, name):
        self.intentName = name

    def legalUtterance(self, string):
        for char in string:
            if not char.isalnum() and \
                    char != " " and \
                    char != "{" and \
                    char != "}" and \
                    char != "." and \
                    char != "-" and \
                    char != "'":
                return char
            else:
                return ""

    # Either returns a string denoting an error or an empty string
    def checkUtterance(self, phrase):
        if self.legalUtterance(phrase) != "":
            return "Utterance contains illegal character '{}'.".format(
                                    self.legalUtterance(phrase))

        # Flagging digits seperately to give a more specific error message
        if any(char.isdigit() for char in phrase):
            return "Digit found. Please spell out numbers, instead " + \
                        "(i.e. 'five' rather than '5')."

        # Creating a variable to help with tracking curly brackets
        openCurlyBrace = -1
        for i in range(0, len(phrase), 1):
            # Periods should only be used to denote the single letters of initials
            # Amazons example is n. b. a. Any other periods aren't allowed
            if phrase[i] == ".":
                if not phrase[i-2] == " ":
                    return "Illegal period found. Periods should only be " + \
                            "used to seperate initials (e.g. 'n. b. a.')."

            # Single ticks should only be used for possives or conjunctions
            elif phrase[i] == "'":
                if not phrase[i-1].isalpha() and not phrase[i+1].isalpha():
                    return "The \"'\" character can only be used for " + \
                            "contractions and possessives " + \
                            "(e.g. shouldn't or Timmy's)."

            # Hyphens should only be used to join two words 
            elif phrase[i] == "-":
                if not phrase[i-1].isalpha() and not phrase[i+1].isalpha():
                    return "'-' should only be used to join hyphenated words " + \
                            "(e.g. editor-in-chief)"

            # Curly brackets must open and close before another set of curly
            # brackets starts
            elif phrase[i] == "}":
                if openCurlyBrace == -1:
                    return "Closing bracket with no opening bracket"
                # Resetting openCurlyBrace if this does close an opening
                # curly brace
                else:
                    openCurlyBrace = -1
            elif phrase[i] == "{":
                if openCurlyBrace != -1:
                    return "Multiple opening brackets with no closing brackets"
                else:
                    openCurlyBrace = i
            elif i == len(phrase)-1:
                if openCurlyBrace != -1:
                    return "Opening bracket with no closing bracket" 

        return ""

    def addUtterance(self, phrase):
        # One utterance can't have the same slot twice. This is a bit messy, but
        # it's the easiest place to check for that
        try:
            newUtterance = Utterance(phrase, self)
            self.intentSlots += newUtterance.grabSlots()
            self.utterances.append(newUtterance)
        except ValueError:
            return "Utterance contains the same slot multiple times"

    # Modifies member varibales and returns an error string/empty string
    def setCurrUtterance(self, inputIndex):
        try:
            index = int(inputIndex)
            if index < 0 or index >= len(self.utterances):
                return "'" + inputIndex + "' is not a valid index number."
            else:
                self.currUtterance = self.utterances[index]
                return ""
        except:
            return "'" + inputIndex + "' is not a valid index number."

    def addIntentSlot(self, slotObj):
        self.intentSlots.append(slotObj)

    def grabIntentSlots(self):
        slotnames = []
        uniqueSlots = []
        for slot in self.intentSlots:
            if slot.name not in slotnames:
                uniqueSlots.append(slot)
                slotnames.append(slot.name)

        return uniqueSlots

    def __getSlotsWithName(self, targetName):
        slotsWithName = []
        for slot in self.intentSlots:
            if slot.name == targetName:
                slotsWithName.append(slot)

        return slotsWithName

    def declareType(self, slotObj, slotType):
        sameNameSlots = self.__getSlotsWithName(slotObj.name)
        for slot in sameNameSlots:
            slot.declareType(slotType)


class Utterance(Intent):
    def __init__(self, phrase, parentIntent):
        self.phrase = phrase
        self.parent = parentIntent
        self.__initSlots()

    def __initSlots(self):
        self.slots = []
        for i in range(0, len(self.phrase), 1):
            if self.phrase[i] == "{":
                beginSlot = i+1
                while self.phrase[i] != "}":
                    i += 1
                endSlot = i
                newSlotName = self.phrase[beginSlot:endSlot]
                newSlot = Slot(newSlotName)
                # Erroring if the utterance already has a slot of the same name
                for slot in self.slots:
                    if slot.name == newSlotName:
                        # This is a bit of a dirty way to handle this, but I
                        # can't return an error string like I normally do in
                        # easyA because this is only used in the constructor.
                        raise ValueError
                self.slots.append(newSlot)
        return ""

    def grabSlots(self):
        return self.slots

    def findWord(self, inWord):
        wordList = self.phrase.split(" ")
        for word in wordList:
            if inWord == word:
                return ""

        return "'{}' not found.".format(inWord)

    # This functions has limited error handling because potential errors *should*
    # already be checked before this is called. Fingers crossed.
    def replaceWord(self, word, slotName):
        substitute = "{" + slotName + "}"
        self.phrase = self.phrase.replace(word, substitute)
        newSlot = Slot(slotName)
        #FIXME: Change this back to the old error handling
        for slot in self.slots:
            if slot.name == newSlotName:
                raise ValueError
        self.slots.append(newSlot)
        self.parent.addIntentSlot(newSlot)
        return ""

    def __repr__(self):
        return self.phrase

class Slot(Utterance):
    def __init__(self, slotName):
        self.name = slotName
        self.type = ""

    def declareType(self, slotType):
        self.type = slotType

    def __repr__(self):
        return "{" + self.name + "}"

class CustomSlotType():
    def __init__(self, name):
        self.typeName = name
        self.values = []

    def addValue(self, newVal):
        for value in self.values:
            if newVal.value == value.value:
                return "'{}' is already a value for SlotType '{}'"\
                        .format(newVal.value).format(self.typeName)

        self.values.append(newVal)
        return ""

    # Have to do this error checking here so that I don't have to 
    def checkVal(self, val):
        #TODO: Implement this
        return ""
        
    def addSynonym(self, origVal, syn):
        for value in self.values:
            if origVal == value.value:
                value.addSynonym(syn)

    def __repr__(self):
        return "Name='" + self.typeName + "', values=" + str(self.values)


class SlotValue():
    def __init__(self, val):
        self.value = val
        self.synonyms = []

    def addSynonym(self, syn):
        if syn not in self.synonyms:
            self.synonyms.append(syn)
            return ""
        else:
            return "'{}' is already a synonym of '{}'.".format(syn)\
                                                        .format(self.value)

    def __repr__(self):
        if len(self.synonyms) == 0:
            return self.value
        else:
            return "value='" + self.value + "', synonyms=" + str(self.synonyms)
