import numpy as np
from PIL import Image
import time

def split_channels(image_path):
    image = Image.open(image_path)
    red_channel, green_channel, blue_channel = image.split()
    red_array = np.array(red_channel)
    green_array = np.array(green_channel)
    blue_array = np.array(blue_channel)
    return red_array, green_array, blue_array


def merge_channels(red_channel, green_channel, blue_channel):
    red_channel = array2image(red_channel)
    blue_channel = array2image(blue_channel)
    green_channel = array2image(green_channel)
    merged_image = Image.merge("RGB", (red_channel, green_channel, blue_channel))
    return merged_image


def image2array(image_path: str, mode="L") -> np.ndarray:
    image = Image.open(image_path)
    image = image.convert(mode)
    image_array = np.array(image)
    return image_array


def array2image(image_array: np.ndarray, save_path: str = "NULL",mode="L" ,is_save: bool = False):
    image = Image.fromarray(image_array.astype(np.uint8), mode=mode)
    if is_save:
        image.save(save_path)
    return image