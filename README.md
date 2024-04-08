# iSparrowRecord - Audio Recording facilities for the iSparrow package

## Summary 
tbd

## Features 
tbd 

## Run in docker 

### build the docker container 
*ONLY WORKS ON LINUX*

From the docker folder in the repo: 
`docker build -t container_name . `. Add `--no-cache` option in case when debugging to avoid pulling in defective layers that have been cached from previous builds

### run it 
`docker run -v /path/to/host_data_folder:/iSparrow/iSparrow_data -v /path/to/host/config/folder:/iSparrow/iSparrow_config --device=/dev/snd:/dev/snd 'container_name' command-line-args-of-isparrowrecord`

## Installation 
tbd 

