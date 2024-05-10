[![tests](https://github.com/ssciwr/iSparrowRecord/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/ssciwr/iSparrowRecord/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/ssciwr/iSparrowRecord/graph/badge.svg?token=FwyE0PNiOk)](https://codecov.io/gh/ssciwr/iSparrowRecord)
# iSparrowRecord - Audio Recording facilities for the iSparrow package

## Summary 
tbd

## Features 
tbd 

## Installation
iSparrowRecord officially only supports Linux-based operating systems and tests on Ubuntu. That being said, it has been successfully deployed on macOS, too. However, it has never been tried on Windows. Follow the following instruction to run it on ubuntu: 

- Install portaudio and python development libraries first. `iSparrowRecord` depends on pyaudio, which in turn depends on portaudio. Hence, these steps are essential. 
```bash 
sudo apt install python3.x-dev portaudio19-dev
```
Replace the `x` with the python version you want `iSparrowRecord` to run on, or leave it out and use `python3` only if you want your OS' default python version. `iSparrowRecord` has been tested on python3.9 and python3.12. 

Then, to get the newest release, install `iSparrowRecord` via pip: 
```bash 
python3.x -m pip install isparrowrecord
```

After this, you should be able to get the `iSparrowRecord` cli in a terminal window by typing `iSparrowRecord`.

## Usage
tbd