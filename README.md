# Scanning Aider

## Purpose
* This bot is for someone who needs to remind them that the scanning mission is done. 
* This bot only support Acunetix, Nessus and commands. 

## Requirement
* This project is based on telegram bot, so [hire](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0) a bot XD. 
* `pip install -r requirements.txt` to install modules. 
* Make sure you have Acunetix and Nessus. 

## Usage
### Telegram Bot 
* In file `telegram_bot.py`, remember to change token and chat id. 
* If you don't know your chat id, ask [Telegram Bot Raw](https://t.me/RawDataBot). 

### Acunetix
* In file `acunetix_bot.py`, remember to change username and password. 
    * Remeber that the password is hashed. (SHA-256)
#### Usage
```
usage: acunetix_bot.py [-h] [-a_ip ACUNETIX_IP] [-a_port ACUNETIX_PORT] -t T -d DESCRIPTION [-u USERNAME] [-p PASSWORD] [-s | --scan_status | --no-scan_status]

optional arguments:
  -h, --help            show this help message and exit
  -a_ip ACUNETIX_IP, --acunetix_ip ACUNETIX_IP
                        Acunetix ip
  -a_port ACUNETIX_PORT, --acunetix_port ACUNETIX_PORT
                        Acunetix port
  -t T                  Target address
  -d DESCRIPTION, --description DESCRIPTION
                        Target description
  -u USERNAME, --username USERNAME
                        Target username
  -p PASSWORD, --password PASSWORD
                        Target password
  -s, --scan_status, --no-scan_status
                        Only check scanning board
```
* `acunetix ip` default is `127.0.0.1`
* `acunetix port` default is `13443`
* Only `target address` and `target description` is required. 
* Strongly recommand to create an account for bot, otherwise you will influence the bot. 
* Example: 
```
python3 acunetix_bot.py -t http://127.0.0.1/ -d "testing" -a_ip ACUNETIX_IP -a_port ACUNETIX_PORT
```
* You are able to only scan the board to check whether there are missions completed or not. 
```
python3 acunetix_bot.py -s
```
![](https://i.imgur.com/MdPbs2o.png)

### Nessus
* In file `nessus_bot.py`, remember to change username and password.
#### Usage
```
usage: nessus_bot.py [-h] [-n_ip NESSUS_IP] [-n_port NESSUS_PORT]

optional arguments:
  -h, --help            show this help message and exit
  -n_ip NESSUS_IP, --nessus_ip NESSUS_IP
                        Nessus ip
  -n_port NESSUS_PORT, --nessus_port NESSUS_PORT
                        Nessus port
```
* Example: 
```
python3 nessus_bot.py -n_ip NESSUS_IP -n_port NESSUS_PORT
```
![](https://i.imgur.com/Pv17vkL.png)

### Command
* The bot is able to remind you that the command is finished. I write the project, since `nmap` usually take a long time to wait ... 
#### Usage
```
usage: command_bot.py [-h] -c COMMAND [-r | --result | --no-result]

optional arguments:
  -h, --help            show this help message and exit
  -c COMMAND, --command COMMAND
                        Command
  -r, --result, --no-result
                        Send result to your telegram bot
```
* Example:
```
python3 command_bot.py -c "YOUR_COMMAND" -r
```
![](https://i.imgur.com/WMtOQ0f.png)

