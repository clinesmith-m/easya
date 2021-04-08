from pathlib import *

class JSONWriter():
    def __init__(self, name="", customTypes=[], intent=None):
        self.skillname = name
        self.intent = intent
        self.customTypes = customTypes


    # This should only ever run when a new project is first created. It
    # hardcodes a lot of things that will be problems at any other time
    def writeInit(self):
        dirName = self.skillname.replace(" ", "-")
        with open(dirName + "/en-US.json", "w") as f:
            f.write(self.initString())


    def writeIntent(self):
        with open("en-US.json", "r+") as f:
            filedata = f.read()
            f.seek(0)
            f.truncate()
            f.write(self.intentString(filedata))


    def initString(self):
        initStr = '{\n'
        initStr += '\t"interactionModel": {\n'
        initStr += '\t\t"languageModel": {\n'
        initStr += '\t\t\t"invocationName": "' + self.skillname + '",\n'
        initStr += '\t\t\t"intents": [\n'
        initStr += '\t\t\t\t{\n'
        initStr += '\t\t\t\t\t"name": "AMAZON.CancelIntent",\n'
        initStr += '\t\t\t\t\t"samples": []\n'
        initStr += '\t\t\t\t},\n'
        initStr += '\t\t\t\t{\n'
        initStr += '\t\t\t\t\t"name": "AMAZON.HelpIntent",\n'
        initStr += '\t\t\t\t\t"samples": []\n'
        initStr += '\t\t\t\t},\n'
        initStr += '\t\t\t\t{\n'
        initStr += '\t\t\t\t\t"name": "AMAZON.StopIntent",\n'
        initStr += '\t\t\t\t\t"samples": []\n'
        initStr += '\t\t\t\t},\n'
        initStr += '\t\t\t\t{\n'
        initStr += '\t\t\t\t\t"name": "AMAZON.NavigateHomeIntent",\n'
        initStr += '\t\t\t\t\t"samples": []\n'
        initStr += '\t\t\t\t}\n'
        initStr += '\t\t\t],\n'
        initStr += '\t\t\t"types": [\n'
        initStr += '\t\t\t]\n'
        initStr += '\t\t},\n'
        initStr += '\t\t"dialog": {\n'
        initStr += '\t\t\t"prompts": [\n'
        initStr += '\t\t\t]\n'
        initStr += '\t\t}\n'
        initStr += '\t}\n'
        initStr += '}\n'
        return initStr


    def __findIntentStart(self, jsonData):
        # Finding the right spot in the file, which is just after
        # the newline that comes before the square bracket that closes the
        # 'intents' entry.
        start = jsonData.find("\"intents\": [")
        index = jsonData.find("{", start)

        #Iterating past the previous intents
        lastIntent = False
        layersDeep = 0
        while not lastIntent:
            if jsonData[index] == "{":
                layersDeep += 1
            elif jsonData[index] == "}":
                layersDeep -= 1
                if layersDeep == 0 and jsonData[index+1] != ",":
                    lastIntent = True

            index += 1

        return index


    def __findTypeStart(self, jsonData):
        markerStr = '"types": [\n'
        index = jsonData.find(markerStr)
        index += len('"types": [\n')

        # Checking to see if other types exist
        itr = index # Keeping index where it is in case there aren't other types
        foundType = False
        while jsonData[itr] != "]":
            if jsonData[itr] == "{":
                foundType = True
                break

            itr += 1

        if foundType:
            index = itr # Now changing index since that what'll be returned
            layersDeep = 0
            lastType = False
            while not lastType:
                if jsonData[index] == "{":
                    layersDeep += 1
                elif jsonData[index] == "}":
                    layersDeep -= 1
                    if layersDeep == 0 and jsonData[index+1] != ",":
                        lastType = True

                index += 1

        return index


    def intentString(self, jsonData):
        # Adding the intent
        newIntentStart = self.__findIntentStart(jsonData)

        startOfFile = jsonData[:newIntentStart]
        endOfFile = jsonData[newIntentStart:]

        # Creating the JSON for the intent
        intentStr = ',\n'
        intentStr += '\t\t\t\t{\n'
        intentStr += '\t\t\t\t\t"name": "'+ self.intent.intentName +'",\n'
        # Writing any and all slots
        slots = self.intent.grabIntentSlots()
        if len(slots) > 0:
            intentStr += '\t\t\t\t\t"slots": [\n'
            for slot in slots:
                slotStr = '\t\t\t\t\t\t{\n'
                slotStr += '\t\t\t\t\t\t\t"name": "' + slot.name + '",\n'
                slotStr += '\t\t\t\t\t\t\t"type": "' + slot.type + '"\n'
                slotStr += '\t\t\t\t\t\t},\n'
                intentStr += slotStr
            # Removing the last trailing comma and restoring the newline
            intentStr = intentStr[:-2] + "\n"
            intentStr += '\t\t\t\t\t],\n'
        # Writing the utterances
        intentStr += '\t\t\t\t\t"samples": [\n'
        for utterance in self.intent.utterances:
            intentStr += '\t\t\t\t\t\t"' + utterance.phrase + '",\n'
        # Removing the trailing comma
        intentStr = intentStr[:-2] + "\n"
        intentStr += '\t\t\t\t\t]\n'
        # Closing the intent
        intentStr += '\t\t\t\t}' # There's already a newline in endOfFile
        # And putting the jsonData string back together so it can be searched
        # again in the next step
        jsonData = startOfFile + intentStr + endOfFile

        # Adding custom slot types
        if len(self.customTypes) > 0:
            typeStart = self.__findTypeStart(jsonData)
            startOfFile = jsonData[:typeStart]
            endOfFile = jsonData[typeStart:]

            # If the last character in startOfFile is a '}', then there are
            # already some custom types, and the last custom type will need a
            # comma added to it
            if startOfFile[-1] == "}":
                startOfFile += ","

            typeStr = '\t\t\t\t{\n'
            for custType in self.customTypes:
                typeStr += '\t\t\t\t\t"name": "'+ custType.typeName +'",\n'
                typeStr += '\t\t\t\t\t"values": [\n'
                for val in custType.values:
                    typeStr += '\t\t\t\t\t\t{\n'
                    typeStr += '\t\t\t\t\t\t\t"name": {\n'
                    typeStr += '\t\t\t\t\t\t\t\t"value": "'+val.value+'"\n'
                    if len(val.synonyms) > 0:
                        # Adding a comma to the previous line
                        typeStr = typeStr[:-1] + "," + typeStr[-1]
                        typeStr += '\t\t\t\t\t\t\t\t"synonyms": [\n'
                        for syn in val.synonyms:
                            typeStr += '\t\t\t\t\t\t\t\t\t"' + syn + '",\n'
                        typeStr = typeStr[:-2] + "\n"
                        typeStr += '\t\t\t\t\t\t\t\t]\n'
                    typeStr += '\t\t\t\t\t\t\t}\n'
                    typeStr += '\t\t\t\t\t\t},\n'
                # Stripping a comma from the last value
                typeStr = typeStr[:-2] + "\n"

                typeStr += '\t\t\t\t\t]\n'
                typeStr += '\t\t\t\t}\n'
            jsonData = startOfFile + typeStr + endOfFile

        #TODO: Once reprompts (etc.) are supported, they'll go here.
        

        return jsonData
