from pathlib import *

class JSONWriter():
    def __init__(self, name="", customTypes=[], intent=None):
        self.skillname = name
        self.intent = intent
        self.customTypes = customTypes


    # This should only ever run when a new project is first created. It
    # hardcodes a lot of things that will be problems at any other time
    def initWrite(self):
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
        initStr += '\t\t"languageModel: {\n'
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
        initStr += '\t\t\t\t},\n'
        initStr += '\t\t\t],\n'
        initStr += '\t\t\t"types": [\n'
        initStr += '\t\t\t]\n'
        initStr += '\t\t},\n'
        initStr += '\t\t"dialog": {\n'
        initStr += '\t\t},'
        initStr += '\t\t"prompts": [\n'
        initStr += '\t\t],'
        initStr += '\t}\n'
        initStr += '}\n'
        return initStr


    def intentString(self, jsonData):
        # Adding the intent
        # Starting by finding the right spot in the file
        markerStr1 = "AMAZON.NavigateHomeIntent"
        mark1 = jsonData.find(markerStr1)
        markerStr2 = "},"
        mark2 = jsonData.find(mark1, markerStr2)
        mark2 += 3 # Moves the index past the "},\n" on this line
        startOfFile = jsonData[:mark2]
        endOfFile = jsonData[mark2:]

        # Creating the JSON for the intent
        intentStr = '\t\t\t\t{\n'
        intentStr += '\t\t\t\t\t"name": "'+ self.intent.intentName +'"\n'
        # Writing any and all slots
        slots = self.intent.grabIntentSlots
        if len(slots) > 0:
            intentStr += '\t\t\t\t\t"slots": [\n'
            for slot in slots:
                slotStr = '\t\t\t\t\t\t{\n'
                slotStr += '\t\t\t\t\t\t\t"name": "' + slot.name + '",\n'
                slotStr += '\t\t\t\t\t\t\t"type": "' + slot.type + '",\n'
                slotStr += '\t\t\t\t\t\t},\n'
                intentStr += slotStr
            intentStr = intentStr[:-1] # Removing the last trailing comma
            intentStr += '\t\t\t\t\t],\n'
        # Writing the utterances
        intentStr += '\t\t\t\t\t"samples": [\n'
        for utterance in self.intent.utterances:
            intentStr += '\t\t\t\t\t\t"' + utterance + '",\n'
        intentStr += '\t\t\t\t\t]'
        # Closing the intent
        intentStr += '\t\t\t\t},\n'
        # And putting the jsonData string back together so it can be searched
        # again in the next step
        jsonData = startOfFile + intentStr + endOfFile

        # Adding custom slot types
        if len(self.customTypes) > 0:
            markerStr = "types: [\n"
            mark = jsonData.find(markerStr)
            mark += len("types: [\n")
            startOfFile = jsonData[:mark]
            endOfFile = jsonData[mark:]
            for custType in self.customTypes:
                typeStr = '\t\t\t\t"name": "'+ custType.typeName +'",\n'
                typeStr += '\t\t\t\t"values": [\n'
                for val in custType.values:
                    typeStr += '\t\t\t\t\t{\n'
                    typeStr += '\t\t\t\t\t\t"name": {\n'
                    typeStr += '\t\t\t\t\t\t\t"value": "'+val.value+'"\n'
                    if len(val.synonyms) > 0:
                        typeStr += '\t\t\t\t\t\t\t"synonyms": [\n'
                        for syn in val.synonyms:
                            typeStr += '\t\t\t\t\t\t\t\t"' + syn + '",\n'
                        typeStr += '\t\t\t\t\t\t\t]\n'
                    typeStr += '\t\t\t\t\t\t}\n'
                    typeStr += '\t\t\t\t\t},\n'
                typeStr += '\t\t\t\t],\n'
            jsonData = startOfFile + typeStr + endOfFile

        #TODO: Once reprompts (etc.) are supported, they'll go here.
        

        return jsonData
