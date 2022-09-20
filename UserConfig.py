import re


#  class container for saving users parsing parametrs
class Config:

    def __init__(self):

        #  reading user config file and initialization configuration atributes
        with open('config.txt') as file:
            self.mark = re.search(r'\'(.*)\'', file.readline().strip()).group(1).lower().replace(' ', '-')
            self.model = re.search(r'\'(.*)\'', file.readline().strip()).group(1).lower().replace(' ', '-')
            self.direction = re.search(r'\'(.*)\'', file.readline().strip()).group(1)


