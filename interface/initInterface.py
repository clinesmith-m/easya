class initerface():
    def __init__(self):
        pass


    def run(self):
        self.name = self.__getName()
        self.makedirs()


    def __getName(self):
        name = input("Please enter the name of your new project: ")
        print("Your project name is '{}'.".format(name)) 
        confirmation = input("This cannot be changed. Are you sure you want to keep this name (y/n)? ")
        if not confirmation.lower() == "y" or not confirmation.lower() == "yes":
            name = self.__getName()
        return name


    def makedirs(self):
        pass
