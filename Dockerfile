FROM arm64v8/python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/ducky4life/pou"

COPY requirements.txt /

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY pou.py keep_alive.py .env /

RUN mkdir databases

WORKDIR /

CMD [ "python", "music.py" ]