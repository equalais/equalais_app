import base64
import io
import json
import logging
from datetime import datetime

import numpy as np
from flask import Flask, request, send_file
from PIL import Image as pil_image
from PIL import Image
from werkzeug.utils import secure_filename

from flask_cors import CORS

from src.adversarial_attack.__main__ import perturb
from src.steganography.__main__ import encode
from src.watermark.__main__ import insert_watermark


ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]


app = Flask(__name__)
CORS(app)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def read_image(request_image) -> Image:

    image_bytes = request_image.read()
    image = pil_image.open(io.BytesIO(image_bytes)).convert("RGB")
    return image


def process_image(image: Image) -> Image:

    image = image.copy()

    # Adversarial attack
    # ------------------

    # NOTE: TF session created on import above
    orig_size = image.size
    image = image.resize((300, 300))
    image = np.asarray(image) / 255.0
    image = perturb([image])[0]
    image = pil_image.fromarray(np.uint8(image * 255)).resize(orig_size)

    # Steganography
    # -------------
    # TODO: Add interface for user to provide details)

    image = np.array(image)
    message = "I do not consent to use of face detection on this image or derivatives of this image."
    token = "elephant_garlic_pizza"
    image = encode(image, message, token, None)

    # Watermark
    # ---------

    # Applies watermark onto alpha channel. May want to apply it onto RGB
    watermark = Image.open("equalAIs_watermark.png")
    image = pil_image.fromarray(image)
    image = insert_watermark(image, watermark, position="top-right")

    # Return processed image
    # ----------------------
    return image


@app.route("/", methods=["GET", "POST", "PUT"])
def face():
    if request.method != "POST":
        return json.dumps({"error": "This endpoint only supports POST requests."})

    if len(request.files) == 0:
        return json.dumps({"error": "The 'files' payload was empty."})

    if request.files.get("image") is None:
        return json.dumps(
            {
                "error": "The 'files' payload did not contain an 'image' key (but did find keys: {}).".format(
                    ", ".join(request.files.keys())
                )
            }
        )

    request_image = request.files.get("image")
    filename = secure_filename(request_image.filename)
    if not allowed_file(filename):
        return json.dumps(
            {
                "error": "The /diagnose endpoint only supports image types: {}".format(
                    ", ".join(ALLOWED_EXTENSIONS)
                )
            }
        )

    image = read_image(request_image)

    image = process_image(image)

    buffer = io.BytesIO()
    image.save(buffer, "PNG")
    return send_file(
        io.BytesIO(base64.b64encode(buffer.getvalue())),
        attachment_filename="equalAIs_" + filename,
        mimetype="image/png;base64",
    )


@app.errorhandler(500)
def server_error(e):
    logging.exception("An error occurred during a request.")
    return (
        """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(
            e
        ),
        500,
    )


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
