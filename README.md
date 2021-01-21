# AutoMeterpreter

## About

## Installation
This project requires `pip`. This can be installed with
`sudo apt install python-pip`

The dependencies can be installed using
`pip install -r requirements.txt`

The Metasploit Framework must be installed for this to work.

## Usage
The options for the metasploit listener can be modified in `config.py`, as well as the path to the meterpreter command list (script), which is a list of newline separated meterpreter commands.

The server payload directory can be added in `config.py` to point to the folder containing the payload files to serve on each port specified in the config.

The program can then be started with `python AutoMeterpreter.py` and when a new meterpreter session is established the commands will be sent to the remote machine.

**NOTE:** AutoMeterpreter must be run as root to function correctly!

## Config
The configuration for AutoMeterpreter.py can be found in `config.py`
