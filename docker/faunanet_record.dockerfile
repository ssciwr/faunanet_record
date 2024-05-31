FROM python:3.11-slim

WORKDIR /home

# install portaudio 
RUN apt-get update
RUN apt-get install -y libportaudio2 libportaudiocpp0 portaudio19-dev libasound-dev libsndfile1-dev build-essential alsa-utils

# install package 
RUN pip install faunanet-record 

WORKDIR /home/faunanet-record

RUN faunanet_record install

# locally set up faunanet-record
RUN CMD ["/bin/bash", "-c", "echo Welcome to faunanet-record!"]