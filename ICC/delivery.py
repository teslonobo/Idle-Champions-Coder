""" Script to hide some imports and for our game loader class and OCR message reader"""

import time
from webbrowser import open as wbopen

from code_grabber.codes import ICCodes, Path
from PIL import ImageGrab

from pygetwindow import getActiveWindow
from pyperclip import copy as pycopy
from easyocr import Reader


class GameLoader:
    """ To handle opening and moving our game in a position we need please read docs if your having issues """
    def __init__(self, path_to_game:str|None, wait:float|int=3) -> None:
        if path_to_game is None or path_to_game == '':
            raise ValueError('Please enter url found in games shortcut property')
        else:
            self.game = path_to_game
        self.wait_period = wait

    def load_game(self):
        """ Load our game """
        wbopen(self.game)
        print('Game is currently loading',end='\r',flush=True)
        time.sleep(self.wait_period)
        print('Game is loaded and ready!')

    def move_game(self,intro_screen:int=5):
        """ Moves our game in the top left hand corner if it isnt already """
        window = getActiveWindow()

        if window.topleft == (0,0):
            print('Game didnt have to be moved to the top left hand corner')
        else:
            window.moveTo(0,0)
            print('Game was moved to the top left hand corner')

        time.sleep(self.wait_period*intro_screen)

class MessageReader:
    """ A handler for our OCR """
    __temp_file__ = Path(__file__).parent / r'assets\temp.png'

    def __init__(self, lang:list[str]=['en'],gpu:bool=False):
        self.reader = Reader(lang, gpu=gpu)

    def create_temp(self):
        """ Create a temp image """
        ss = ImageGrab.grab(bbox=(0,0,1280,720))
        ss.save(self.__temp_file__)

    def check_opening(self):
        """ We need to check the opening OKAY to even begin"""
        self.create_temp()
        text = self.reader.readtext(str(self.__temp_file__))
        for found in text:
            if found[1] == 'Okay':
                return found

    def check_for_message(self) -> bool:
        """ We need to check for certain messages to be able to continue trying in place or we need to go back and since it opened successfully"""
        self.create_temp()
        text = self.reader.readtext(str(self.__temp_file__))

        search_for = ['This is not a valid combination.', 'Youhave already redeemed this', 'This offer has expired','You have already redeemed this']
        for found in text:
            if found[1] in search_for:
                return True
        return False

    def center_click(self,bounding) -> tuple:
        """ Centers our clicks"""
        center_x = (bounding[0][0] + bounding[2][0]) / 2
        center_y = (bounding[0][1] + bounding[2][1]) / 2
        return center_x, center_y

    def flip_message(self):
        """ Checks for a flip all cards message to flip the cards over  """
        self.create_temp()
        text = self.reader.readtext(str(self.__temp_file__))

        for found in text:
            if found[1] == 'Flip All Cards':
                return self.center_click(found[0])




