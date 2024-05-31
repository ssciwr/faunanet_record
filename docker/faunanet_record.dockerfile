FROM python:3.11-slim

WORKDIR /home

# install portaudio 
RUN apt-get update && apt-get install -y libportaudio2 libportaudiocpp0 portaudio19-dev libasound-dev libsndfile1-dev build-essential alsa-utils && apt-get clean
# install package 
RUN pip install faunanet-record

WORKDIR /home/faunanet-record

RUN faunanet_record install

RUN apt-get autoremove -y && apt-get clean

# locally set up faunanet-record
CMD ["/bin/bash", "-c", "echo Welcome to faunanet-record!"]