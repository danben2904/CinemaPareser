'''core.py'''

import requests

class CinemaParser:
    '''Parser of Cinema site'''
    def __init__(self, city='msk'):
        '''Defining city'''
        self.city = city
        self.url = 'https://{}.subscity.ru'.format(self.city)
        self.content = None
    def extract_raw_content(self):
        '''Extract content'''
        self.content = requests.get(self.url).text
    def print_raw_content(self):
        '''Print content'''
        print(self.content)
