FROM python:3.11-slim

WORKDIR /home

# install package 
RUN pip install faunanet-record 

WORKDIR /home/faunanet-record

# locally set up faunanet-record
RUN faunanet-record 