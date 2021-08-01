import pickle


class Command:
    def __init__(self, command):
        self.__raw = command
        self.__split = command.split(" ")

    @property
    def raw(self):
        return self.__raw

    @property
    def split(self):
        return self.__split

    @property
    def name(self):
        return self.__split[0]

    @property
    def args(self):
        return self.__split[1:]
        
