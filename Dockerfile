FROM gcr.io/google-appengine/python

COPY requirements.txt requirements.txt
COPY model model/
COPY src src/
COPY main.py main.py
COPY equalAIs_watermark.png equalAIs_watermark.png

RUN virtualenv /env -p python3.6
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
RUN pip install -r requirements.txt

# Run a WSGI server to serve the application.
# gunicorn must be declared as a dependency in requirements.txt
CMD gunicorn -b :$PORT main:app