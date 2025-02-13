""" Main script for the whole program """

from os import getenv
from delivery import GameLoader, MessageReader, time, pycopy, ICCodes
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KController
from dotenv import load_dotenv
from __init__ import __environment__

env_data = load_dotenv(__environment__)
game = getenv('URL')

if game == '':
    raise ValueError('You need to enter a URL in the .env file.')
gpu_status = False if getenv('GPU_ON') == 'False' else True

PAUSE = int(getenv('DELAY'))

our_data = ICCodes()
codes = our_data.j_data

if not our_data.check_new_codes():
    print('No new Codes to Enter!')
    exit(0)

if our_data.nc_count == 1:
    print(f'Looks like there is {our_data.nc_count} new code to enter!')
else:
    print(f'Looks like there are {our_data.nc_count} new codes to enter!')

mreader = MessageReader(gpu=gpu_status) # to make it run faster you can pass True to gpu parameter

loader = GameLoader(game) # there are two different wait times.. one for inital load and one for the games intro
loader.load_game()
loader.move_game(intro_screen=(PAUSE*4)) # this is the second wait time thats multipled by original wait time, depending how long it takes to get through the intro may want to adjust accordingly

time.sleep(10)
our_mouse = Controller()
our_keyboard = KController()

def unlock_chest_menu():
    ' To open the unlock chest menu '
    time.sleep(5)
    print('Now entering unlock a locked Chest Menu')
    our_mouse.position = (83, 613)
    our_mouse.click(Button.left,1)
    time.sleep(5)

def click_paste():
    ' To paste from our copy in clipboard '
    our_mouse.position = (205, 695)
    our_mouse.click(Button.left,1)

def enter_codes():
    ' Our main function for entering our codes into the unlock Chest Menu '
    remaining_new = our_data.nc_count

    for k, c in codes.items():
        for code, _ in c.items():
            time.sleep(PAUSE)
            print(code)
            pycopy(code)
            time.sleep(PAUSE)
            click_paste()
            time.sleep(PAUSE)
            our_keyboard.press(Key.enter)
            our_keyboard.release(Key.enter)
            time.sleep(PAUSE)

            # If code has been redeemed
            if mreader.check_for_message():
                time.sleep(PAUSE)
                our_keyboard.press(Key.enter)
                our_keyboard.release(Key.enter)
                time.sleep(PAUSE)

            else:
                time.sleep((PAUSE*2))
                x , y  = mreader.flip_message()
                our_mouse.position = (x,y)
                our_mouse.click(Button.left,1)
                time.sleep(PAUSE)
                our_mouse.click(Button.left,1)
                time.sleep(PAUSE)
                unlock_chest_menu()

            our_data.j_data[k][code] = True
            our_data.update_json_data()
            remaining_new -= 1

            if remaining_new == 0:
                break

        if remaining_new == 0:
            break

opening_message = mreader.check_opening()

if opening_message[1] == 'Okay':
    center_x, center_y = mreader.center_click(opening_message[0])
    our_mouse.position = (center_x, center_y)
    our_mouse.click(Button.left,1)

elif opening_message[1] is None:
    raise ValueError('Seemed like the game has not loaded properly, or try to adjust intro delay')

time.sleep(5)
print('Now entering Chests Menu')
our_mouse.position = (141, 118)
our_mouse.click(Button.left, 1)

unlock_chest_menu()
enter_codes()

time.sleep(PAUSE)
print('Completed entering Codes! Congrats on automating unlock codes!!🥳🥳🥳')
