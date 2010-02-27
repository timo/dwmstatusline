# coding: utf-8
from subprocess import Popen, call, PIPE
from random import choice
import utils
from utils import animate, wait, PREVIOUS
import time


# install a few status functions

# Status functions call one of these helper functions and yield the result:
#
# next_function   Resume with the next (random) status function.
# animate         Use a transition function to show the next string.
# wait            Wait some time before displaying the next string.


# uptime/load
# mpd status
# free hard drive storage

@utils.status_func
def memory_free():
    """Display the used RAM and Swap space."""
    yield animate(2, "Used RAM")
    
    # Parse the output of the "free" command. :(
    free_output = Popen(["free"], stdout=PIPE).communicate()[0]
    # get the interesting lines
    interesting = free_output.split("\n")[1:]
    total_ram = float(interesting[0].split()[1])
    used_ram = int(interesting[1].split()[2]) / total_ram
    total_swap = float(interesting[2].split()[1])
    used_swap = int(interesting[2].split()[2]) / total_swap

    yield animate(10, utils.pretty_progressbar(used_ram, 80))
    
    yield animate(2, "Used Swap Space")
    yield animate(10, utils.pretty_progressbar(used_swap, 80))

@utils.register_if_installed("mpc")
def mpd_np():
    """Display the mpd status via mpc."""
    try:
        status_output = Popen(["mpc", "status"], stdout=PIPE).communicate()[0]
    except OSError:
        yield wait(5, "mpc not installed :(")
        return

    result = ""

    lines = status_output.split("\n")
    if len(lines) < 3: # stopped
        yield wait(10, "MPD stopped")
    else:
        result += "MPD " + lines[1].split()[0] + " " + lines[0].strip()
        yield animate(10, result)
        yield animate(10, lines[1].split()[2])

@utils.register_if_installed("acpi")
def battery():
    """Display the battery status via acpi."""
    try:
        status_output = Popen(["acpi"], stdout=PIPE).communicate()[0]
    except OSError:
        yield wait(5, "battery status could not be determined.")
        return
    
    yield animate(10, status_output.split("\n")[0])

class NewsbeuterUnread(utils.DelayedUpdateDisplay):
    delay = 600
    def call(self):
        unread_text = Popen(["newsbeuter", "-x", "print-unread"], stdout=PIPE).communicate()[0]
        unread_items = int(unread_text.split()[0])
        if unread_items > 0:
            yield animate(10, "Newsbeuter: %d unread news." % (unread_items,))
        else:
            yield animate(10, "Newsbeuter: No unread news.")

    def update(self):
        Popen(["newsbeuter", "-x", "reload"], stdout=PIPE)
        self.last_update = time.time()

    def checkInstall(self):
        return call(["which", "newsbeuter"], stdout=PIPE) == 0
NewsbeuterUnread()

# install a few transition functions

# These work in the same way as the status functions

@utils.transition_func
def shoot(prev, new):
    """Animate a transition with a flying star."""
    d = 0.05
    icon = "*"
    length = max(len(prev), len(new))

    for pos in range(0, length, 2):
        padding = max(length - pos - 1 - len(prev), 0)
        old = prev[-(length - pos - padding):]
        yield wait(d, new[:pos] + ' ' * padding + old)

    yield wait(1, new.lstrip())

def startup_animation():
    """Animate the startup of the script."""
    yield wait(1, "DWM Status Bar Animator")
    yield animate(1, "a silly script by timonator")

def run_animation(iter_, previous):
    """Run an animation."""
    yield previous
    yield iter_.send(previous)
    for value in iter_:
        yield value

def run_statuses(startfunc):
    """The 'main loop' of dwmstat."""
    iters = [startfunc()]
    previous = ''

    while True:
        while iters:
            iter_ = iters.pop()
            for value in iter_:
                if isinstance(value, basestring):
                    utils.dwm_set_status(value)
                    previous = value
                elif value is PREVIOUS:
                    iters.append(run_animation(iter_, previous))
                    break
                else:
                    iters.append(iter_)
                    iters.append(value)
                    break
        iters.append(choice(utils.statuses)())


if __name__ == "__main__":
    run_statuses(startup_animation)
