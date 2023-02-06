## General info
This script was created to get an information about NordVPN servers from the NordVPN public API.
## Requirements
* Python 3.7+
* pip

## Usage
1. Before running this script run folowing command to install missing dependencies.

```bash
$ python3 -m pip install -r requirements.txt
```
2. After that we need to create `config.ini` file adding API URL, Subnet and required network prefix information to it.
Example:
```ini
[config]
api_url=https://api.nordvpn.com/v1/servers
subnet=89.187.175.0/24
new_prefix=25
```
3. Now we can run the script using following command.

```bash
$ parser.py [-h] -c CONFIG -l {INFO,DEBUG} [-f LOG]
```
Example:
```bash
$ ./parser.py -c config.ini -l DEBUG -f parser.log
```
