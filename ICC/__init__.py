""" Script creates data file and asset directory if not already created """

from code_grabber.codes import Path

__assets__ = Path(__file__).parent / 'assets'
__data__ = __assets__ / 'ICC_data.json'
__environment__ = __assets__ / '.env'

def inital_setup():
    """ Initial setup """
    __assets__.mkdir(parents=True)
    __data__.touch()

    with __environment__.open('w') as f:
        f.write("""URL=''\nGPU_ON=False\nDELAY='2'""")

if not __assets__.exists():
    inital_setup()
