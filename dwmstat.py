# coding: utf-8
from subprocess import Popen, PIPE
from time import sleep
from random import choice

from utils import *

PREVIOUS = object()

_statuses = []
_transitions = []

# A decorator to add a function to our statuses list.
def status_func(func):
    global _statuses
    _statuses.append(func)
    return func

# A decorator to add a function to our transitions list.
def transition_func(func):
    global _transitions
    _transitions.append(func)
    return func

# This function allows us to set the text of the status line.
def dwm_set_status(text):
    Popen(["xsetroot", "-name", text])

def animate(delay, text):
    previous = yield PREVIOUS
    animator = choice(_transitions)
    yield animator(previous, text)
    sleep(delay)

def wait(delay, text):
    yield text
    sleep(delay)


# install a few status functions

# Status functions call one of these helper functions and yield the result:
#
# next_function   Resume with the next (random) status function.
# animate         Use a transition function to show the next string.
# wait            Wait some time before displaying the next string.


# uptime/load
# mpd status
# free hard drive storage

# Free memory function
@status_func
def memory_free():
    yield animate(5, "Used RAM")
    
    # Parse the output of the "free" command. :(
    free_output = Popen(["free"], stdout=PIPE).communicate()[0]
    # get the interesting lines
    interesting = free_output.split("\n")[1:]
    total_ram = float(interesting[0].split()[1])
    used_ram = int(interesting[1].split()[2]) / total_ram
    total_swap = float(interesting[2].split()[1])
    used_swap = int(interesting[2].split()[2]) / total_swap

    yield animate(5, pretty_progressbar(used_ram, 80))
    
    yield animate(5, "Used Swap Space")
    yield animate(5, pretty_progressbar(used_swap, 80))

@status_func
def mpd_np():
    try:
        status_output = Popen(["mpc", "status"], stdout=PIPE).communicate()[0]
    except OSError:
        yield wait(5, "mpc not installed :(")
        return

    result = ""

    lines = status_output.split("\n")
    if len(lines) < 3: # stopped
        yield wait(5, "MPD stopped")
    else:
        result += "MPD " + lines[1].split()[0] + " " + lines[0].strip()
        yield animate(5, result)
        yield animate(5, lines[1].split()[2])

@status_func
def battery():
    try:
        status_output = Popen(["acpi"], stdout=PIPE).communicate()[0]
    except OSError:
        yield wait(5, "battery status could not be determined.")
        return
    
    yield animate(10, status_output.split("\n")[0])

# install a few transition functions

# These work in the same way as the status functions

@transition_func
def shoot(prev, new):
    d = 0.05
    icon = "*"
    length = max(len(prev), len(new))

    for pos in range(0, length, 2):
        padding = max(length - pos - 1 - len(prev), 0)
        old = prev[-(length - pos - padding):]
        yield wait(d, new[:pos] + ' ' * padding + old)

    yield wait(1, new.lstrip())

def startup_animation():
    yield wait(1, "DWM Status Bar Animator")
    yield animate(1, "a silly script by timonator")

def run_animation(iter_, previous):
    yield previous
    yield iter_.send(previous)
    for value in iter_:
        yield value

def run_statuses(startfunc):
    iters = [startfunc()]
    previous = ''

    while True:
        while iters:
            iter_ = iters.pop()
            for value in iter_:
                if isinstance(value, basestring):
                    dwm_set_status(value)
                    previous = value
                elif value is PREVIOUS:
                    iters.append(run_animation(iter_, previous))
                    break
                else:
                    iters.append(iter_)
                    iters.append(value)
                    break
        iters.append(choice(_statuses)())


if __name__ == "__main__":
    run_statuses(startup_animation)
