FROM python:3.11-slim


# install portaudio 
RUN apt-get update \ 
&& apt-get install --no-install-recommends -y portaudio19-dev build-essential alsa-utils libasound-dev libsndfile1-dev \
&& apt-get autoremove -y \ 
&& apt-get clean \ 
&& rm -rf /var/lib/apt/lists/*

WORKDIR /root/test

# install package 
RUN pip install pyaudio wave

COPY ./iotest.py ./

ENTRYPOINT ["python3", "./iotest.py"]