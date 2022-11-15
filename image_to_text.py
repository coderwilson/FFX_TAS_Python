# Python code to convert an image to ASCII image.
import logging
import time

import numpy as np
from PIL import Image

import config

logger = logging.getLogger(__name__)

logging.getLogger("PIL").setLevel(logging.INFO)


config_data = config.open_config()
# gamestate
color_log = config_data.get("color_log", False)
show_images = config_data.get("show_images", False)


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
    gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    # 10 levels of gray
    gscale2 = "@%#*+=-:. "

    reset = "\x1b[0m"

    def __init__(self, filename, cols, scale=0.5, more_levels=False, color=False):
        self._convert_image(filename, cols, scale, more_levels, color)

    def _get_average_L(self, image):
        """
        Given PIL Image, return average value of grayscale value
        """
        # Get image as numpy array
        im = np.array(image)
        # Get shape
        w, h = im.shape
        # Get average
        return np.average(im.reshape(w * h))

    def _get_average_RGB(self, image):
        """
        Given PIL Image, return average value of color
        """
        im = np.array(image)
        avg_color_per_row = np.average(im, axis=0)
        return np.average(avg_color_per_row, axis=0)

    def _rgb(self, col):
        """
        Get the console code for a given RGB color [R, G, B]. Colors are in the range 0-255
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
        image_bw = image_color.convert("L")
        # Store dimensions
        W, H = image_color.size[0], image_color.size[1]
        logger.info(f"input image {filename} dims: {W} x {H}")
        # Compute width of tile
        w = W / cols
        # Compute tile height based on aspect ratio and scale
        h = w / scale
        # Compute number of rows
        rows = int(H / h)

        logger.info(f"cols: {cols}, rows: {rows}")
        logger.info(f"tile dims: {w} x {h}")

        # Check if image size is too small
        if cols > W or rows > H:
            raise ValueError("Image {filename} is too small for specified cols!")

        # Ascii image is a list of character strings, one for each row
        self.ascii = []
        # Generate list of dimensions
        for j in range(rows):
            y1 = int(j * h)
            y2 = int((j + 1) * h)
            # Correct last tile
            if j == rows - 1:
                y2 = H
            # Append an empty string (new row)
            self.ascii.append("")

            for i in range(cols):
                # Crop image to tile
                x1 = int(i * w)
                x2 = int((i + 1) * w)
                # Correct last tile
                if i == cols - 1:
                    x2 = W
                # Crop image to extract tile
                bw_tile = image_bw.crop((x1, y1, x2, y2))
                # Get average luminance
                avg = int(self._get_average_L(bw_tile))

                # Apply color to the tile
                if color:
                    # Crop color image to extract tile
                    col_tile = image_color.crop((x1, y1, x2, y2))
                    # Get average [r,g,b] value of tile
                    col_avg = self._get_average_RGB(col_tile)
                    # Apply color using hex code
                    self.ascii[j] += self._rgb(col_avg)

                # Look up ascii char from LUT
                if more_levels:
                    gsval = self.gscale1[int((avg * 69) / 255)]
                else:
                    gsval = self.gscale2[int((avg * 9) / 255)]

                # Append ascii char to string
                self.ascii[j] += gsval
        # Restore console coloring
        if color:
            self.ascii[rows - 1] += self.reset

    # Print the image to console
    def print_image(self):
        for row in self.ascii:
            print(f"{row}")


def maybe_show_image(filename, cols=80):
    if show_images:
        ImageToText(filename=filename, cols=cols, color=color_log).print_image()
