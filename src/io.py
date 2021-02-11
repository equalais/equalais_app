from logging import Logger
from pathlib import Path

from numpy import array as Array
from PIL import Image as pil_image


def read_image(filepath: Path, logger: Logger = None) -> Array:
    """Reads in an image as an array and logs read to console.

    Args:
        filepath (Path): Filepath to image.
        logger (Logger): Logging object for writing output to console. (default: None)

    Returns:
        np.array: Target image.
    """
    pil_pointer = pil_image.open(filepath).convert("RGB")
    image = Array(pil_pointer)
    pil_pointer.close()
    if logger is not None:
        logger.info(f"Read: {filepath}")
    return image


def write_image(image: Array, filepath: Path, logger: Logger = None) -> None:
    """Write an image to disk and logs write to console.

    Args:
        image (np.array): Image array to write to disk.
        filepath (Path): Destination for where to write image.
        logger (Logger): Logging object for writing output to console. (default: None)
    """
    pil_pointer = pil_image.fromarray(image)
    pil_pointer.save(filepath)
    if logger is not None:
        logger.info(f"Wrote: {filepath}")
