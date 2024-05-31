FROM python:3.11-slim

WORKDIR /home


# install tensorflow lite
RUN pip install faunanetrecord
WORKDIR /home/faunanet

# add folders for incoming data and for output and make sure they are mounted
RUN mkdir /home/faunanet/faunanet_data
RUN mkdir /home/faunanet/faunanet_config 

# add entrypoint
CMD ["faunanet_record"]