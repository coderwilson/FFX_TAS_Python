import colorsys
from typing import Any, overload


def s32(integer: int) -> int:
    return ((integer & 0xffffffff) ^ 0x80000000) - 0x80000000


def treeview(obj, indentation: int = 0) -> str:
    string = ''
    match obj:
        case dict():
            for key, value in obj.items():
                string += ' ' * 4 * indentation
                string += f'{key}: '
                if isinstance(value, dict):
                    string += '\n'
                string += treeview(value, indentation + 1)
        case list() | tuple():
            string += f'{", ".join([str(a) for a in obj])}\n'
        case _:
            string += f'{obj}\n'
    return string


def add_bytes(*values: int) -> int:
    value = 0
    for position, byte in enumerate(values):
        value += byte * (256 ** position)
    return value


@overload
def get_contrasting_color(color: str) -> str:
    ...


@overload
def get_contrasting_color(color: tuple[int, int, int]) -> tuple[int, int, int]:
    ...


def get_contrasting_color(color: str | tuple[int, int, int] | int,
                          ) -> str | tuple[int, int, int]:
    """Returns a color that contrasts with the one provided as input.
    Accepts either a string in the format #rrggbb or rrggbb
    or a tuple of 3 integers in range 0-255."""
    match color:
        case str():
            hexcode = color.strip('#')
            red = int(hexcode[:2], 16)
            green = int(hexcode[2:4], 16)
            blue = int(hexcode[4:6], 16)
            return_string = True
        case (int(), int(), int()):
            red, green, blue = color
            return_string = False
        case (red, green, blue):
            return_string = False
        case _:
            raise TypeError()

    h, s, v = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
    if s < 0.1:
        if v < 0.1:
            s = 0
        if v < 0.5:
            v = 1
        else:
            v = 0
    h = (h + 0.5) % 1
    red, green, blue = [int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v)]

    if return_string:
        return f'#{red:02x}{green:02x}{blue:02x}'
    return red, green, blue


def stringify(object: Any) -> str:
    return str(object).lower().replace(' ', '_')
