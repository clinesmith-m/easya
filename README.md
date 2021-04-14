# easyA
## Overview
A suite of workflow management and development tools designed to enable easier Amazon Alexa development. This is designed to be run in a programmers development environment with testing taking place through AWS Lambda.

## Prerequisites
You must already have `make`, `python3` and python `virtualenv` installed. For full functionality, you will also need to be able to run this code from within a `bash` shell. You will also need your own AWS account.

## Setup
Clone this repository into the directory of your choice. Then enter that directory and run `make`. This will install all of the necessary executables. You also have the option to specify what directory these install in by running `make INSTALL_DIR=<YOUR_DIR>`. By default, they will install in `${HOME}/bin`.

## Using easyA
### Making a new skill
Enter the directory of your choice and run `easyA init`. This will prompt you to enter the invocation name for your skill, which is what users will say to an Alexa to get it to run your code. easyA will then create a new directory based on the invocation name of your skill and create a python virtual environemnt within it.

### Adding an intent
Intents are added by running `easyA add-intent` and following the prompts on the command line. This will generate python code in `main.py` that handles your intent and also updates the `en-US.json` file to include all the new information you entered. You are then free to write the actual code for your intents.

### Creating a zip file of your skill
Run `easyA zip`. This will create a file named `skill.zip` in the parent directory of your easyA working directory. This is formatted to compatable with AWS Lambda.

## Creating your skill within AWS
To test a sizable Alexa skill, you'll need to create an AWS Lambda function and a skill on the AVS developer console. When creating the lambda function you'll need to select the `author from scratch` option in the console and use python 3.6 or better as your runtime environment. Once the function is created, you'll need to change the `handler` option from its default to `main.lambda_handler`. I also recommend changing your configuration so that your function doesn't time out for at least 15 seconds or so because errors often take a while to return, meaning that if there's a problem with your code, you'll be shown a timeout error rather than the actual issue.

When creating the skill in the AVS developer console, make sure you select the `custom` option for the skill model and `Provision your own` for the backend, and, on the next page, `Start from scratch` as the template. From there, all the default options should be compatible with easyA.

Once both the skill and the function are created, you can follow the `Connect the Lambda function to your skill` and `Add an Alexa Skills Kit Trigger` sections of the broader tutorial found [here](https://developer.amazon.com/en-US/docs/alexa/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html) to tie the two together.

## Testing your skill
In the simple case where you've updated your code, but haven't added any additional intents, you can simply take the zip file output by `easyA zip` and upload it to your AWS Lambda function via the `Upload from zip` functionality in the code tab.

If you've added new intents, or this is simply the first time you've invoked your skill, you'll need to both do the above step and go to the AVS Developer console, upload the `en-US.json` file in your primary working directory to the JSON editor that's located in the `build` tab, and rebuild your model.

Once the relevant action has been taken, you can invoke your skill by using the `test` tab of the AVS Development Console. If it works, Alexa will respond. If not, you can copy/paste the JSON request the console generated and paste that into the `Test event` field of the `test` tab of your AWS Lambda function to generate a comprehensive error message. I believe you can also configure Lambda to log that information, but I never took the time to do that while testing this project, because it's not an immediately intuitive process.

## When not to use easyA
easyA is for sizable hobby projects. If you want to make an alexa skill that isn't overly complex, it would be much easier for you to host it entirely on the AVS developer console, which automates far more of the skill development process than easyA ever could. That said, you can't import any external libraries whatsoever on the developer console, so for larger projects, it's not a viable option, hence why this exists.

This also isn't the option if you're making a particularly ambitious Alexa project, as it has several limitations, which I detail in the next section.

## Current limitations
The two main features that I don't currently support, but would like to, is multi-turn dialogue, which is a pretty core feature of the Alexa that will take serious augmentation of the `add-intent` interface and the JSON code I generate, and the ability to write your code in multiple python files which you import into main.py, which will require and upgrade of the `easyZip` script, along with additional testing to make sure AWS Lambda can still process the resulting zip file. I currently have no timetable for implementing these changes, but if you're using easyA and those augmentations would be beneficial to you, reach out to me and I can give you a better idea of when they might be done.

## Reporting issues
If you encounter any problems with easyA, or know of functionality that would be helpful to implement, open an issue in this github repository and I will take a look at it.
