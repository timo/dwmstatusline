# coding: utf-8
# The dwmstatusline utility module.
# Written by Timo Paulssen

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
    bar1size = int(percent * charsize)
    bar2size = charsize - bar1size

    return "[%s%s%s] %03d%%" % (
      "=" * bar1size,
      "∗",
      " " * bar2size,
      percent)
