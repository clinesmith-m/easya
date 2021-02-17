from pathlib import *

class Pywriter():
    def __init__(self, intent):
        self.intent = intent
        self.slots = self.intent.grabIntentSlots()

    def write(self):
        #TODO: Maybe add more error handling so it's a guarentee that the user
        # is in their easyA working directory. Should probably right when the
        # interface starts
        mainfile = Path("main.py")
        if not mainfile.exists():
            with open("main.py", "w") as f:
                initStr = self.openInitString()
                f.write(initStr)
            # This double open is ugly and inefficient, but it greatly
            # simplifies the addNewIntent code, so it'll probably stay
            with open("main.py", "w") as f:
                if self.intent != None:
                    f.write(self.addNewIntent(initStr))
                f.write(self.closeInitString())
        else:
            with open("main.py", "r+") as f:
                filedata = f.read()
                f.seek(0)
                f.truncate()
                f.write(self.addNewIntent(filedata))


    def addNewIntent(self, pyFileData):
        markerStr = "# PLEASE DO NOT REMOVE OR MODIFY THIS COMMENT."
        markerIndex = pyFileData.find(markerStr)
        startOfFile = pyFileData[:markerIndex]
        endOfFile = pyFileData[markerIndex:]

        intentClassName = self.intent.intentName + "Handler"
        pyIntent = "class " + intentClassName
        pyIntent += "(AbstractRquestHandler):\n"

        # Adding the always-repeated can_handle function
        pyIntent += "\tdef can_handle(self, handler_input):\n"
        pyIntent += "\t\treturn ask_utils.is_intent_name(\""
        pyIntent += self.intent.intentName + "\")(handler_input)\n"
        pyIntent += "\n"

        # And the actually interesting handle function
        pyIntent += "\tdef handle(self, handler_input):\n"
        intentSlots = self.intent.grabIntentSlots()
        if len(intentSlots) > 0:
            pyIntent += "\t\tslots = handler_input.request_envelope.request.intent.slots\n"
            for slot in intentSlots:
                pyIntent += "\t\t" + slot.name
                pyIntent += " = slots[\"" + slot.name + "\"].value\n"

        pyIntent += "\t\tspeak_output = \"Change this string to modify what Alexa says\"\n"
        pyIntent += "\n"
        pyIntent += "\t\treturn (\n"
        pyIntent += "\t\t\thandler_input.response_builder\n"
        pyIntent += "\t\t\t\t.speak(speak_output)\n"
        pyIntent += "\t\t\t\t# .ask(\"Add a reprompt if you want to keep the session open for the user\")\n"
        pyIntent += "\t\t\t\t.response\n"
        pyIntent += "\t\t\t)\n"
        pyIntent += "\n"

        fullFileData = startOfFile + pyIntent + endOfFile
        return(fullFileData)


    def openInitString(self):
        openInit = ""
        openInit += "import logging\n"
        openInit += "import ask_sdk_core.utils as ask_utils\n"
        openInit += "\n"
        openInit += "from ask_sdk_core.skill_builder import SkillBuilder\n"
        openInit += "from ask_sdk_core.dispatch_components import AbstractRequestHandler\n"
        openInit += "from ask_sdk_core.dispatch_components import AbstractExceptionHandler\n"
        openInit += "ask_sdk_core.handler_input import HandlerInput\n"
        openInit += "\n"
        openInit += "from ask_sdk_model import Response\n"
        openInit += "logger = logging.getLogger(__name__)\n"
        openInit += "logger.setLevel(logging.INFO\n"
        openInit += "\n"
        openInit += "\n"
        openInit += "class LaunchRequestHandler(AbstractRequestHandler):\n"
        openInit += "\t# Handler to launch the skill\n"
        openInit += "\tdef can_handle(self, handler_input):\n"
        openInit += "\t\treturn ask_utils.is_request_type(\"LaunchRequest\")(handler_input)\n"
        openInit += "\n"
        openInit += "\tdef handle(self, handler_input):\n"
        openInit += "\t\tspeak_output = \"Welcome to {}. Modify this string to change what Alexa says\"\n".format(self.intent.intentName)
        openInit += "\t\t#reprompt_text = \"Prompt the user for more dialogue here.\"\n"
        openInit += "\t\treturn (\n"
        openInit += "\t\t\thandler_input.response_builder\n"
        openInit += "\t\t\t\t.speak(speak_output\n"
        openInit += "\t\t\t\t#.ask(reprompt_text)\n"
        openInit += "\t\t\t\t.response\n"
        openInit += "\t\t)\n"
        openInit += "\n"
        openInit += "\n"
        openInit += "# PLEASE DO NOT REMOVE OR MODIFY THIS COMMENT.\n"
        openInit += "# easyA uses it as a marker when adding intents to this file\n"
        openInit += "\n"
        return openInit


    def closeInitString(self):
        closeInit = ""
        closeInit += "\n"
        closeInit += "class HelpIntentHandler(AbstractRequestHandler):\n"
        closeInit += "\t# Handles the default Amazon Help intent\n"
        closeInit += "\tdef can_handle(self, handler_input):\n"
        closeInit += "\t\treturn ask_utils.is_intent_name(\"AMAZON.HelpIntent\")(handler_input)\n"
        closeInit += "\n"
        closeInit += "\tdef handle(self, handler_input):\n"
        closeInit += "\t\tspeak_output = \"You can say hello to me! How can I help?\"\n"
        closeInit += "\t\treturn (\n"
        closeInit += "\t\t\thandler_input.response_builder\n"
        closeInit += "\t\t\t\t.speak(speak_output)\n"
        closeInit += "\t\t\t\t.ask(speak_output)\n"
        closeInit += "\t\t\t\t.response\n"
        closeInit += "\t\t)\n"
        closeInit += "\n"
        closeInit += "\n"
        closeInit += "class CancelOrStopIntentHandler(AbstractRequestHandler):\n"
        closeInit += "\t# Handles both the Cancel and Stop default intents\n"
        closeInit += "\tdef can_handle(self, handler_input):\n"
        closeInit += "\t\treturn (ask_utils.is_intent_name(\"AMAZON.CancelIntent\")(handler_input) or\n"
        closeInit += "\t\t\task_utils.is_intent_name(\"AMAZON.StopIntent\")(handler_input))\n"
        closeInit += "\n"
        closeInit += "\tdef handle(self, handler_input):\n"
        closeInit += "\t\tspeak_output = \"Goodbye\"\n"
        closeInit += "\n"
        closeInit += "\t\treturn (\n"
        closeInit += "\t\t\thandler_input.response_builder\n"
        closeInit += "\t\t\t\t.speak(speak_output)\n"
        closeInit += "\t\t\t\t.response\n"
        closeInit += "\t\t)\n"
        closeInit += "\n"
        closeInit += "\n"
        closeInit += "class SessionEndedRequestHandler(AbstractRequestHandler):\n"
        closeInit += "\t# Handles the session end\n"
        closeInit += "\tdef can_handle(self, handler_input):\n"
        closeInit += "\t\treturn ask_utils.is_request_type(\"SessionEndedRequest\")(handler_input)\n"
        closeInit += "\n"
        closeInit += "\tdef handle(self, handler_input):\n"
        closeInit += "\n"
        closeInit += "\t\t# Any clean-up logic goes here\n"
        closeInit += "\n"
        closeInit += "\t\t\treturn handler_input.response_builder.response\n"
        closeInit += "\n"
        closeInit += "\n"
        closeInit += "class IntentReflectorHandler(AbstractRequestHandler):\n"
        closeInit += "\t# The intent reflector is used for testing and debugging the interaction model\n"
        closeInit += "\t# It will simply repeat the intent the user said.\n"
        closeInit += "\t# You can create custom handlersfor your intents by defining them above,\n"
        closeInit += "\t# then also adding them to the request handler chain below.\n"
        closeInit += "\t# The creator of easyA will point out said request handler\n"
        closeInit += "\t# chain through its own comment once he figures out what/where it is\n"
        closeInit += "\tdef can_handle(self, handler_input):\n"
        closeInit += "\t\treturn ask_utils.is_request_type(\"IntentRequest\")(handler_input)\n"
        closeInit += "\n"
        closeInit += "\tdef handle(self, handler_input):\n"
        closeInit += "\t\tintent_name = ask_utils.get_intent_name(handler_input)\n"
        closeInit += "\t\tspeak_output = \"You just triggered\" + intent_name + \".\"\n"
        closeInit += "\n"
        closeInit += "\t\treturn (\n"
        closeInit += "\t\t\thandler_input.response_builder\n"
        closeInit += "\t\t\t\t.speak(speak_output)\n"
        closeInit += "\t\t\t\t#.ask(\"Add a reprompt if you want to keep the session open for the user\")\n"
        closeInit += "\t\t\t\t.response\n"
        closeInit += "\t\t)\n"
        closeInit += "\n"
        closeInit += "\n"
        closeInit += "class CatchAllExceptionHandler(AbstractExceptionHandler):\n"
        closeInit += "\t# Generic error handling to capture any syntax or routing errors. If you receive an error\n"
        closeInit += "\t# stating the request handler chain is not found, you have not implemented a handler\n"
        closeInit += "\t# for the intent being invoked or included it in the skill builder below, per Amazon's github\n"
        closeInit += "\t# It also means that easyA messed up, so please let the me know by opening an issue\n"
        closeInit += "\t# describing your bug at github.com/clinemith-m/easya\n"
        closeInit += "\tdef can_handle(self, handler_input, exception):\n"
        closeInit += "\t\treturn True\n"
        closeInit += "\n"
        closeInit += "\tdef handle(self, handler_input, exception):\n"
        closeInit += "\t\tlogger.error(exception, exc_info=True)\n"
        closeInit += "\n"
        closeInit += "\t\tspeak_output = \"Sorry, I had trouble doing what you asked. Please try again.\"\n"
        closeInit += "\t\treturn (\n"
        closeInit += "\t\t\thandler_input.response_builder\n"
        closeInit += "\t\t\t\t.speak(speak_output)\n"
        closeInit += "\t\t\t\t.ask(speak_output)\n"
        closeInit += "\t\t\t\t.response\n"
        closeInit += "\t\t)\n"
        closeInit += "\n"
        closeInit += "\n"
        closeInit += "# YOU SHOULD NEVER HAVE TO MESS WITH THE BELOW CODE. IF THERE IS A PROBLEM PLEASE\n"
        closeInit += "# PLEASE NOTIFY ME BY OPENING AN ISSUE AT github.com/clinesmith-m/easya\n"
        closeInit += "# For the curious, though, per Amazon:\n"
        closeInit += "# The SkillBuilder object acts as the entry point for your skill, routing all request and response\n"
        closeInit += "# payloads to the handlers above. Make sure any new handlers or interceptors you've\n"
        closeInit += "# defined are included below. The order matters - they're processed top to bottom.\n"
        closeInit += "\n"
        closeInit += "\n"
        closeInit += "sb = SkillBuilder()\n"
        closeInit += "\n"
        closeInit += "sb.add_request_handler(LaunchRequestHandler())\n"
        closeInit += "# User intents are added here\n"
        if self.intent != None:
            closeInit += "sb.add_request_handler({}Handler())\n"\
                            .format(self.intent.intentName)
        closeInit += "sb.add_request_handler(HelpIntentHandler())\n"
        closeInit += "sb.add_request_handler(CancelOrStopIntentHandler())\n"
        closeInit += "sb.add_request_handler(SessionEndedRequestHandler())\n"
        closeInit += "sb.add_request_handler(IntentReflectorHandler())# make sure this goes last\n"
        closeInit += "\n"
        closeInit += "sb.add_exception_handler(CatchAllExceptionHandler())\n"
        closeInit += "\n"
        closeInit += "lambda_handler = sb.lambda_handler()\n"
        closeInit += "\n"
        return closeInit

if __name__== "__main__":
    pass
