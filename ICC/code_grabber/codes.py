""" Script to grab idle champion codes """
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup as BS

class ICCodes:
    """ Using a default url to incendar we will scrape the codes """

    __url__ = 'https://incendar.com/idlechampions_codes.php'
    __data_file__ = Path(__file__).parent.parent / 'assets' / 'ICC_data.json'

    def __init__(self) -> None:
        self.jdata = self.json_data()
        self.current_codes = set(k for v in self.jdata.values() for k in v)
        self.update_data()
        self.j_data = self.filter_new_codes()
        self.nc_count = self.count_new_codes()

    def json_data(self) -> dict:
        """ Load our json data """
        try:
            with self.__data_file__.open('r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, PermissionError):
            data = {}
        return data

    def update_json_data(self):
        """ Updates our json file """
        with self.__data_file__.open('w') as f:
            json.dump(self.jdata, f, indent=4)

    def fetch_data(self):
        """ Fetch idle champion codes from our url """
        r = requests.get(self.__url__)
        if r.status_code == 200:
            soup_data = BS(r.content,'html.parser')
            codes = [c.text for code in soup_data.find_all('textarea') for c in code]
            return codes
        else:
            raise requests.ConnectionError

    def update_data(self):
        """ Main function that updates our data file """
        codes = self.fetch_data()
        i = len(self.current_codes)
        for code in codes:
            for c in code.split('\r\n'):
                if c not in self.current_codes and c != '':
                    self.jdata[str(i).zfill(3)] = {c:False}
                    i += 1
        self.update_json_data()

    def check_new_codes(self) -> bool:
        """ Checks the new code count """
        if self.nc_count >= 1:
            return True
        return False

    def count_new_codes(self) -> int:
        """ So we know how many new codes we have to enter """
        return len(self.j_data)

    def filter_new_codes(self):
        """ Filter down our list to the ones we have to do"""
        return {k:v for k, v in self.jdata.items() for _,b in v.items() if b == False}
