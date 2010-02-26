# coding: utf-8
# The dwmstatusline utility module.
# Written by Timo Paulssen
from subprocess import Popen, call, PIPE

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

statuses = []
transitions = []

# A decorator to add a function to our statuses list.
def status_func(func):
    global statuses
    statuses.append(func)
    return func

def register_if_installed(command):
    if call(["which", command], stdout=PIPE) == 0:
        return status_func
    else:
        return lambda x: x

# A decorator to add a function to our transitions list.
def transition_func(func):
    global transitions
    transitions.append(func)
    return func

# This function allows us to set the text of the status line.
def dwm_set_status(text):
    Popen(["xsetroot", "-name", text])
