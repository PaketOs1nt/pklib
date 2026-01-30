import os

os.system("")  # хз как но оно анлокает цвета в консоли на винде


def fg(r: int, g: int, b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m"


def bg(r: int, g: int, b: int) -> str:
    return f"\x1b[48;2;{r};{g};{b}m"


class fgcols:
    red = fg(255, 0, 0)
    green = fg(0, 255, 0)
    blue = fg(0, 0, 255)


class bgcols:
    red = bg(255, 0, 0)
    green = bg(0, 255, 0)
    blue = bg(0, 0, 255)


class rs:
    all = "\x1b[0m"
    fg = "\x1b[39m"
    bg = "\x1b[49m"
