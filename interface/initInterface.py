from writers.JSONWriter import JSONWriter 
import subprocess
class Initerface():
    def __init__(self):
        pass


    def run(self):
        self.name = self.__getName()
        subprocess.run(["easyA-init", self.name])
        jwriter = JSONWriter(name=self.name)
        jwriter.initWrite()


    # This can be modified to do error checking. I think AVS has a couple
    # additional rules for skill names
    def __getName(self):
        name = input("Please enter the name of your new project: ")
        print("Your project name is '{}'.".format(name)) 
        confirmation = input("This cannot be changed. Are you sure you want to keep this name (y/n)? ")
        while not confirmation.lower() == "y" and not confirmation.lower() == "yes":
            name = input("New name: ")
            confirmation = input("Do you want to keep this name (y/n)? ")
        return name
