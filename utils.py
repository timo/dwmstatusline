# coding: utf-8
# The dwmstatusline utility module.
# Written by Timo Paulssen
from subprocess import check_call, call, PIPE
import time
from random import choice

STATUSDELAY = 30

PREVIOUS = object()

def pretty_progressbar(fraction, charsize):
    """Generate a progressbar with accompanying percentage value.

    fraction should be a value between 0 and 1.
    charsize is the amount of space free for the status bar.
    For optimum results, do not try to generate bars shorter than 15
    characters."""
    # Remove one char on each side for the brackets and one in the middle.
    charsize -= 3
    # Remove five characters for a percentage, too.
    charsize -= 5

    # Make sure it's round so that we don't accidentally have wiggly status
    # bars.
    bar1size = int(fraction * charsize)
    bar2size = charsize - bar1size

    return "[%s%s%s] %03d%%" % (
      "=" * bar1size,
      "O",
      " " * bar2size,
      fraction * 100)

def animate(delay, text):
    """Run an animator to the text."""
    previous = yield PREVIOUS
    animator = choice(transitions)
    yield animator(previous, text)
    time.sleep(delay)

def wait(delay, text):
    """Wait before displaying the text."""
    yield text
    time.sleep(delay)

statuses = []
transitions = []

def status_func(func):
    """A decorator to add a function to our statuses list."""
    global statuses
    statuses.append(func)
    return func

def register_if_installed(command):
    """Only install this status func if the command exists in PATH."""
    if call(["which", command], stdout=PIPE) == 0:
        return status_func
    else:
        return lambda x: x
def transition_func(func):
    """A decorator to add a function to our transitions list."""
    global transitions
    transitions.append(func)
    return func

def dwm_set_status(text):
    """This function allows us to set the text of the status line."""
    check_call(["xsetroot", "-name", text])

class DelayedUpdateDisplay(object):
    delay = 300
    def __init__(self):
        if not self.checkInstall():
            return
        global statuses
        self.last_update = 0
        statuses.append(self)

    def checkInstall(self):
        """Check wether to install this status func."""
        print "checkInstall(self) not implemented by %s." % (self.__class__.__name__,)
        return False

    def __call__(self):
        """Do the displaying."""
        if time.time() > self.last_update + self.delay:
            self.__update__()
            return
        
        for res in self.call():
            yield res

    def call(self):
        yield wait(1, "call(self) not implemented by %s." % (self.__class__.__name__),)
        print "call(self) not implemented by %s." % (self.__class__.__name__,)

    def __update__(self):
        self.update()
        self.last_update = time.time()

    def update(self):
        """Update the data."""
        print "update(self) not implemented by %s." % (self.__class__.__name__,)
