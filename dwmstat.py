# coding: utf-8
from subprocess import Popen, PIPE
from time import sleep
from random import choice

from utils import *

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

next_function = lambda: (0, "")
animate = lambda delay, text: (-delay, text)
wait = lambda delay, text: (delay, text)


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
    total_ram = float(interesting[0].split()[0])
    used_ram = total_ram / int(interesting[1].split()[2])
    total_swap = float(interesting[2].split()[1])
    used_swap = total_swap / int(interesting[2].split()[2])

    yield animate(5, pretty_progressbar(used_ram, 80))
    
    yield animate(5, "Used Swap Space")
    yield animate(5, pretty_progressbar(used_swap, 80))

    yield next_function()


# install a few transition functions

# These work in the same way as the status functions

@transition_func
def shoot(prev, new):
    d = 0.1
    icon = "*"
    length = max(len(prev), len(new))

    def lcut(s, l):
        if l > len(s):
            return ""
        else:
            return s[:l]

    yield wait(d, prev[:-1] + icon)
    for pos in range(length):
        yield wait(d, lcut(prev, pos) + icon + new[:-pos])
        d *= 0.9
    
    yield next_function()

def animate_trans(fr, to):
    animator = choice(_transitions)(fr, to)
    for (delay, text) in animator:
        dwm_set_status(text)
        sleep(delay)

def startup_animation():
    yield animate(1, "DWM Status Bar animator")
    yield animate(1, "a silly script by timonator")
    yield next_function()

def run_statuses(startfunc):
    func = startfunc()
    (cmd, text) = func.next()

    while True:
        pcmd, ptext = cmd, text
        try:
            (cmd, text) = func.next()
        except StopIteration:
            (cmd, text) = next_function()

        if cmd == 0:
            func = choice(_statuses)()
            (cmd, text) = func.next()

        elif cmd > 0:
            sleep(cmd)
        elif cmd < 0:
            sleep(-cmd)
            animate_trans(ptext, text)

        dwm_set_status(text)


if __name__ == "__main__":
    run_statuses(startup_animation)
