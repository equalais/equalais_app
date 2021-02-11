from argparse import ArgumentParser
from pathlib import Path

from numpy import array
from PIL import Image

from src.io import write_image
from src.logger import get_main_logger

VALID_POSITIONS = [None, "top-left", "top-right", "bottom-left", "bottom-right"]


def insert_watermark(image: Image, watermark: Image, position: str = None) -> Image:
    """Create an image with a watermark.

    Position of watermark is scaled by size of `image` and includes padding.

    Args:
        image (Image): Target image to have watermarked.
        watermark (Image): Image to use as the watermark.
        position (str, optional): Corner position of watermark. Defaults to None.

    Raises:
        ValueError: If passed position is invalid.

    Returns:
        array: Watermarked image.
    """

    if position not in VALID_POSITIONS:
        raise ValueError(
            f"{position}, is an invalid position. You may pass: {VALID_POSITIONS}"
        )

    width, height = image.size

    # Scale the watermark
    scale = 1 / 6
    largest_dimension = max(width, height)
    watermark_dimension = int(largest_dimension * scale)
    watermark = watermark.resize((watermark_dimension, watermark_dimension))

    padding = int(largest_dimension * (scale / 4))
    offset = watermark_dimension + padding

    if position is None:
        position = (0 + padding, 0 + padding)
    elif position == "top-left":
        position = (0 + padding, 0 + padding)
    elif position == "bottom-left":
        position = (0 + padding, height - offset)
    elif position == "top-right":
        position = (width - offset, 0 + padding)
    elif position == "bottom-right":
        position = (width - offset, height - offset)

    watermarked_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    watermarked_image.paste(image, (0, 0))
    watermarked_image.paste(watermark, position, mask=watermark)

    return watermarked_image


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "image", type=str, help="Filepath to the image to put the watermark on."
    )
    parser.add_argument(
        "-w",
        "--watermark",
        type=str,
        default="equalAIs_watermark.png",
        help="Filepath to the watermark to be placedon the image.",
    )
    parser.add_argument(
        "-p",
        "--position",
        type=str,
        choices=VALID_POSITIONS,
        default="top-right",
        help="Position to place watermark.",
    )

    args = parser.parse_args()

    logger = get_main_logger("equalAIs", "watermark")

    input_filepath = Path(args.image)
    input_image_format = input_filepath.suffix.split(".")[1]
    output_filename = f"{input_filepath.stem}_watermarked.png"
    output_filepath = input_filepath.parent / output_filename

    image = Image.open(input_filepath)
    watermark = Image.open(args.watermark)

    watermarked_image = insert_watermark(image, watermark, position=args.position)
    watermarked_image = array(watermarked_image)

    write_image(watermarked_image, output_filepath, logger)
