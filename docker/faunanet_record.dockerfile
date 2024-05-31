FROM python:3.11-slim

WORKDIR /home

# install package 
RUN pip install faunanet-record 

WORKDIR /home/faunanet-record

RUN faunanet-record install

# locally set up faunanet-record
RUN CMD ["/bin/bash", "-c", "echo Welcome to faunanet-record!"]