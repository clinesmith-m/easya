class AddIntent():
    def __init__(self, name):
        self.intentName = name
        self.utterances = []

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

        for i in range(0, len(phrase), 1):
            # Periods should only be used to denote the single letters of initials
            # Amazons example is n. b. a. Any other periods aren't allowed
            if phrase[i] == ".":
                if not phrase[i-2] == " ":
                    return "Illegal period found. Periods should only be " + \
                            "used to seperate initials (e.g. 'n. b. a.')."

            # Single ticks should only be used for possives or conjunctions
            if phrase[i] == "'":
                if not phrase[i-1].isalpha() and not phrase[i+1].isalpha():
                    return "The \"'\" character can only be used for " + \
                            "contractions and possessives " + \
                            "(e.g. shouldn't or Timmy's)."

            # Hyphens should only be used to join two words 
            if phrase[i] == "-":
                if not phrase[i-1].isalpha() and not phrase[i+1].isalpha():
                    return "'-' should only be used to join hyphenated words " + \
                            "(e.g. editor-in-chief)"

        return ""

    def addUtterance(self, utterance):
        self.utterances.append(utterance)
