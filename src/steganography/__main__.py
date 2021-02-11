"""This module is used for encoding and decoding messages in images.

Implementation came from Abdou Rockikz:
https://www.thepythoncode.com/article/hide-secret-data-in-images-using-steganography-python

For a different implementation, see Dave Briccetti:
https://github.com/dcbriccetti/StegaPy/blob/master/stegapy.py

Least Significant Bit (LSB) is a technique in which last bit of each pixel is modified and replaced with the data bit. This method only works on Lossless-compression images, which means that the files are stored in a compressed format, but that this compression does not result in the data being lost or modified, PNG, TIFF, and BMP as an example, are lossless-compression image file formats.
"""
from argparse import ArgumentParser
from logging import Logger
from pathlib import Path
from typing import Iterable

import numpy as np

from src.io import read_image, write_image
from src.logger import get_main_logger


def to_bin(data: Iterable) -> str:
    """Convert data to binary format as string.

    Args:
        data (Iterable): Target data to convert to string.

    Raises:
        TypeError: If data provided does not meet instance conditions.

    Returns:
        str: String in binary format.
    """
    if isinstance(data, str):
        return "".join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")


def encode(
    image: np.array, message: str, token: str, logger: Logger = None
) -> np.array:
    """Encode an image with a secret message using Least Significant Bit method.

    Args:
        image (np.array): Target image to embed a message in.
        message (str): Secret message to embed in an image.
        token (str): Secret token that marks end of line for decoding message in image.
        logger (Logger): Logging object for writing output to conole. (default: None)

    Raises:
        ValueError: If message has insufficient bytes available in target image.

    Returns:
        np.array: Image encoded with secret message.
    """
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    if logger is not None:
        logger.info(f"Maximum bytes to encode: {n_bytes}")
    if len(message) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    # add stopping criteria
    message += token
    data_index = 0
    # convert data to binary
    binary_message = to_bin(message)
    # size of data to hide
    data_len = len(binary_message)
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_message[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_message[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_message[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image


def decode(image: np.array, token: str) -> str:
    """Decodes secret message in an image array.

    Args:
        image (np.array): Input image with secret message.
        token (str): Secret token that marks end of line for decoding message in image.

    Returns:
        str: Decoded secret message.
    """
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    # split by 8-bits
    all_bytes = [binary_data[i : i + 8] for i in range(0, len(binary_data), 8)]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-len(token) :] == token:
            break
    return decoded_data[: -len(token)]


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "action",
        type=str,
        choices=["encode", "decode"],
        help="Whether to encode or decode a message in a given image."
        "If encode is passed a message must also be passed.",
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Filepath to image that is target of message encoding or decoding.",
    )
    parser.add_argument(
        "-m",
        "--message",
        type=str,
        default=None,
        help="The message to encode in a target image.",
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        default="equalAIs_token",
        help="Secret token to use for decoding message in image.",
    )

    args = parser.parse_args()

    logger = get_main_logger("equalAIs", "steganography", args.action)

    if args.action == "encode":
        if args.message is None:
            raise ValueError(
                "A message must be passed with -m or --message when the action is encode."
            )
    elif args.action == "decode":
        if args.message is not None:
            raise ValueError(
                "You selected to decode. Passing a message when decoding is invalid."
            )

    input_filepath = Path(args.filepath)

    input_image_format = input_filepath.suffix.split(".")[1]
    if input_image_format != "png":
        logger.warning(
            f"Image provided was {input_image_format} format. Converting image to png."
        )
    output_filename = f"{input_filepath.stem}_equalAIs.png"
    output_filepath = input_filepath.parent / output_filename

    image = read_image(input_filepath, logger)

    if args.action == "encode":
        encoded_image = encode(image, args.message, args.token, logger)
        write_image(encoded_image, output_filepath, logger)

    elif args.action == "decode":
        decoded_message = decode(image, args.token)
        logger.info(decoded_message)
    else:
        raise ValueError(
            f"{args.action} is not a valid action. You may pass 'encode' or 'decode'."
        )
