import subprocess
import argparse
from telegram_bot import TelegramBot

class Nmap:
    def __init__(self):
        self.telegram_bot = TelegramBot()

    def command(self, cmd, result):
        subp = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
        outs, _ = subp.communicate()
        print(outs)

        self.telegram_bot.sendMessage("Command Complete" + "\n" + "Command: " + cmd)
        if result:
            self.telegram_bot.sendMessage(outs)

def getParameter():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--command", type=str, help="Command", required=True)
    parser.add_argument("-r", "--result", action=argparse.BooleanOptionalAction, help="Send result to your telegram bot")

    args = parser.parse_args()
    return vars(args)

def main():
    args = getParameter()

    nmap = Nmap()
    nmap.command(args["command"], args["result"])

if __name__ == '__main__':
    main()