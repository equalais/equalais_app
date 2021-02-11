# equalAIs app

![watermark](equalAIs_watermark.png){:height="100px" width="100px"}

The equalAIs app provides three levels of protection and control to an image:

1. Adversial attack against face recognition
1. Stegnographic message encoding
1. Visible watermark

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
