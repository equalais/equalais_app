from pathlib import Path
from unittest import TestCase

from src.steganography.__main__ import decode, encode, read_image


class TestSteganography(TestCase):
    """Test for src/steganography/__main__.py"""

    @classmethod
    def setUpClass(cls):

        test_image_location = Path("src/tests/data")
        cls.image_jpg = read_image(test_image_location / "320px-Desert_Dunes.jpg")
        cls.image_png = read_image(test_image_location / "320px-Desert_Dunes.png")

    def test_steganography_main(self):
        """Test that encoding and decoding work for jpg and png."""
        true_message = "he who controls the spice controls the universe"

        test_input = self.image_jpg
        encoded_image = encode(test_input, true_message)
        decoded_message = decode(encoded_image)
        print(f"JPG encoded message: {decoded_message}")
        self.assertEqual(true_message, decoded_message)

        test_input = self.image_png
        encoded_image = encode(test_input, true_message)
        decoded_message = decode(encoded_image)
        print(f"PNG encoded message: {decoded_message}")
        self.assertEqual(true_message, decoded_message)
