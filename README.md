# equalAIs app

The equalAIs app provides three levels of protection and control to an image:

| | |
|-|-|
| <img src="equalAIs_watermark.png" width="75"> | 1. Adversial attack against face recognition </br> 2. Stegnographic message encoding </br> 3. Visible watermark |
|||

Current REST API: `https://equalais.ue.r.appspot.com`

## Spinning up REST service

### On Google Cloud App Engine

1. Install/configurature [google cloud SDK](https://cloud.google.com/sdk/)

1. In your Google Cloud dashboard create a project, `{gcloud-project-name}`

1. In a terminal, run:

   ```bash
   gcloud app deploy gcp_rest_app.yaml --project {gcloud-project-name} --verbosity=info
   ```

1. Update the URL in `equalais.github.io/js/tool.js` to be URL defined in the console output from the above command.

### Locally

1. Build the Docker image:

   ```bash
   docker build . -t {equalais-image-name}
   ```

1. Spin up the container:

   ```bash
   docker run -p 127.0.0.1:8080:8080 {equalais-image-name}
   ```

1. Then update the URL in `equalais.github.io/js/tool.js` to be `http://0.0.0.0:8080`.

## Running equalAIs components manually

In order to run components of equalAIs manually (i.e., not using the hosted tool), you will need to clone this repository. We do not currently provide a script for running the adversarial attack manually.

For details on implementation and argument options, please see the Python scripts in src.

### Steganography

The equalAIs webtool uses the following by default:

- `--message`: `I do not consent to use of face detection on this image or derivatives of this image.`
- `--token`: `elephant_garlic_pizza`

We are planning on updating our API to allow users to define their own message and decode token, however this is not currently available. In the meantime you can customize your steganographic message and token by running the steganography script manually.

#### Manually encoding steganographic message

If you would like to use a custom message and decoding token, you can run the steganography script using the following command in the root of this project:

```bash
python -m src.steganography encode path/to/photo.png --message "your-custom-message" --token "your-special-token"
```

#### Decoding steganographic message

You can decode your image that has been run through the equalAIs tool by running the following command in the root of this project:

```bash
python -m src.steganography decode "path/to/equalais/photo.png" --token "elephant_garlic_pizza"
```

If your image has been run through the webtool, by default this should return the message:

> I do not consent to use of face detection on this image or derivatives of this image.

#### Method

We use the Least Significant Bit (LSB) technique. The implementation we use is heavily based off of [Abdou Rockikz's well-explained demonstration](https://www.thepythoncode.com/article/hide-secret-data-in-images-using-steganography-python). Please note that a limitation of the LSB technique is that it only works on lossless compression images. As a result, we only write our images as `.png` files.

Our tool is a proof-of-concept, and we welcome suggestions and pull-request contributions for more robust techniques!

### Watermark

You can also manually add a watermark to an image using the following command:

```bash
python -m src.watermark "path/to/photo.png"
```

