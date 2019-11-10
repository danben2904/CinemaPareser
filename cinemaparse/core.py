'''core.py'''

from time import gmtime, strftime
import requests
from bs4 import BeautifulSoup as bs

class CinemaParser:
    '''Parser of Cinema site'''
    def __init__(self, city='msk'):
        '''Defining city'''
        self.city = city
        self.url = 'https://{}.subscity.ru'.format(self.city)
        self.content = None
    def extract_raw_content(self):
        '''Extract content'''
        self.content = requests.get(self.url)
    def print_raw_content(self):
        '''Print content'''
        print(self.content.text)
    def get_films_list(self):
        '''Get films'''
        new_url = self.url + "/movies"
        page = requests.get(new_url)
        soup = bs(page.text, 'html.parser')
        ans = []
        all_films = soup.find_all("div", class_="movie-plate")
        for film in all_films:
            ans.append(film['attr-title'])
        return ans
    def get_film_nearest_session(self, name):
        '''Get film nearest session'''
        new_url = self.url + "/movies"
        page = requests.get(new_url)
        soup = bs(page.text, 'html.parser')
        all_films = soup.find_all("div", class_="movie-plate")
        kino = None
        time = 'zzzz'
        now_time = list(strftime("%H:%M", gmtime()))
        now_h = str((int(now_time[0] + now_time[1]) + 3) % 24)
        now_h = [str(i) for i in now_h]
        if len(now_h) == 1:
            now_time[1:2] = now_h[:1]
        else:
            now_time[:2] = now_h[:2]
        ans = ""
        for i in now_time:
            ans += str(i)
        now_time = ans
        for film in all_films:
            if film['attr-title'].lower() == name.lower():
                new_url = self.url + film.find_all("a")[0]['href']
                page = requests.get(new_url)
                soup = bs(page.text, 'html.parser')
                day_table = soup.find_all("table", class_="table")[1]
                dredi = day_table.find_all("tr", class_="row-entity")
                for i in dredi:
                    now_kino = i.find_all("a", class_="underdashed")[0].get_text()
                    dredi2 = i.find_all("tr")
                    for j in dredi2:
                        for k in j.find_all("a", class_="btn"):
                            if (k.get_text() < time and k.get_text() > now_time):
                                time = k.get_text()
                                kino = now_kino
                return (kino, time)
        return (None, None)
    def get_soonest_session(self):
        '''Get soonest session'''
        time = 'zzzz'
        kino = None
        film = None
        new_url = self.url + "/movies"
        page = requests.get(new_url)
        soup = bs(page.text, 'html.parser')
        all_films = soup.find_all("div", class_="movie-plate")
        print(new_url)
        for flm in all_films:
            now = self.get_film_nearest_session(flm['attr-title'])
            if now[1] < time:
                time = now[1]
                kino = now[0]
                film = flm['attr-title']
        return (kino, film, time)
