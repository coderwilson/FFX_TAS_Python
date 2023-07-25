# Python code to convert an image to ASCII image.
import logging
import time

from PIL import Image

import config

logger = logging.getLogger(__name__)

logging.getLogger("PIL").setLevel(logging.INFO)


config_data = config.open_config()
# gamestate
config_logging = config_data.get("logging", {})
color_log = config_logging.get("color_log", False)
show_images = config_logging.get("show_images", False)
terminal_width = config_logging.get("terminal_width", 80)


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        ret = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        logger.debug(f"Elapsed time: {elapsed:0.4f} seconds")
        return ret

    return wrapper


class ImageToText(object):
    # gray scale level values from:
    # http://paulbourke.net/dataformats/asciiart/
    # 70 levels of gray
    gscale1 = (
        r"""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
    )
    # 10 levels of gray
    gscale2 = "@%#*+=-:. "

    reset = "\x1b[0m"

    def __init__(self, filename, cols, scale=0.5, more_levels=True, color=False):
        self._convert_image(filename, cols, scale, more_levels, color)

    def _rgb(self, col):
        """
        Get the console code for a given RGB color [R, G, B].
        Colors are in the range 0-255
        """
        red = int(col[0])
        green = int(col[1])
        blue = int(col[2])
        return f"\x1b[38;2;{red};{green};{blue}m"

    @timer_decorator
    def _convert_image(self, filename, cols, scale, more_levels, color):
        """
        Given Image and dims (rows, cols) returns an m*n list of Images
        """
        # Open image and convert to grayscale
        image_color = Image.open(filename)
        # Store dimensions
        W, H = image_color.size[0], image_color.size[1]
        logger.debug(f"input image {filename} dims: {W} x {H}")
        ratio = W / H
        # Compute number of rows
        rows = int(ratio * cols * scale)

        image_color = image_color.resize(size=[cols, rows])
        image_bw = image_color.convert("L")

        logger.debug(f"cols: {cols}, rows: {rows}")

        # Ascii image is a list of character strings, one for each row
        self.ascii = []
        # Generate list of dimensions
        for y in range(rows):
            # Append an empty string (new row)
            self.ascii.append("")

            for x in range(cols):
                coord = x, y
                # Get average luminance
                bw_pixel = int(image_bw.getpixel(coord))

                # Apply color to the tile
                if color:
                    # Apply color using hex code
                    self.ascii[y] += self._rgb(image_color.getpixel(coord))

                # Look up ascii char from LUT
                if more_levels:
                    gsval = self.gscale1[int((bw_pixel * 69) / 255)]
                else:
                    gsval = self.gscale2[int((bw_pixel * 9) / 255)]

                # Append ascii char to string
                self.ascii[y] += gsval
        # Restore console coloring
        if color:
            self.ascii[rows - 1] += self.reset

    # Print the image to console
    def print_image(self):
        for row in self.ascii:
            print(f"{row}")


def maybe_show_image(filename):
    if show_images:
        ImageToText(
            filename=filename, cols=terminal_width, color=color_log
        ).print_image()
