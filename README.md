[![tests](https://github.com/ssciwr/faunanet-record/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/ssciwr/faunanet-record/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/ssciwr/faunanet-record/graph/badge.svg?token=FwyE0PNiOk)](https://codecov.io/gh/ssciwr/faunanet-record)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ssciwr_iSparrowRecord&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ssciwr_iSparrowRecord)
[![Supported OS: Linux](https://img.shields.io/badge/OS-Linux%20%7C%20macOS%20%7C%20Windows-green.svg)](https://www.linux.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
# faunanet-record - Audio Recording facilities for the faunanet package
The `faunanet-record` project is a simple collection of audio recording facilities for the [faunanet](https://github.com/ssciwr/iSparrow) project. While it can be used standalone, it is designed to cooperate with `faunanet`. 

## Installation
faunanet-record officially only supports Linux-based operating systems and tests on Ubuntu. That being said, it has been successfully deployed on macOS, too. However, it has never been tried on Windows. Follow the following instruction to run it on Ubuntu: 

- Install portaudio and python development libraries first. `faunanet-record` depends on pyaudio, which in turn depends on portaudio. Hence, these steps are essential. 
```bash 
sudo apt install python3.x-dev portaudio19-dev
```
Replace the `x` with the python version you want `faunanet-record` to run on, or leave it out and use `python3` only if you want your OS' default python version. `faunanet-record` has been tested on `python3.9` and `python3.12`.

- Then, to get the newest release, install `faunanet-record` via pip: 
```bash 
python3.x -m pip install faunanet-record
```
After this, you should be able to get the `faunanet-record` cli in a terminal window by typing `faunanet-record`. 

For a development installation, install `faunanet-record` in editable mode: 

- Clone this repository
```bash
 git clone https://github.com/ssciwr/iSparrowRecord.git 
```
or, when you're using ssh: 
```bash
git@github.com:ssciwr/iSparrowRecord.git
```

- then, from the root directory of the repository: 
```bash 
python3 -m pip install -e . && python3 -m pip install -r requirements-dev.txt
```

## Usage
`faunanet-record` comes with two configuration files - 