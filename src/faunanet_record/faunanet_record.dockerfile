FROM python:3.11-slim

ENV RUN_CONFIG=""

# install portaudio 
RUN apt-get update \ 
&& apt-get install --no-install-recommends -y --fix-missing portaudio19-dev build-essential alsa-utils libasound-dev libsndfile1-dev \
&& apt-get autoremove -y \ 
&& apt-get clean \ 
&& rm -rf /var/lib/apt/lists/*

WORKDIR /root

# install package 
RUN pip install faunanet-record && faunanet_record install

# locally set up faunanet-record
# TODO: should this be a python script? 
CMD ["/bin/bash", "-c", "if [[ -z \"$RUN_CONFIG\" ]] ; then faunanet_record run; else faunanet_record run --cfg=~/faunanet/config/${RUN_CONFIG}; fi"]