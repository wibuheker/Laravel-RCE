from termcolor import colored

class Color:

    @staticmethod
    def blue(string):
        return colored(string, 'blue')
    
    @staticmethod
    def red(string):
        return colored(string, 'red')
    
    @staticmethod
    def green(string):
        return colored(string, 'green')
    
    @staticmethod
    def yellow(string):
        return colored(string, 'yellow')