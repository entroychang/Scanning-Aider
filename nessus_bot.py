import requests
import json
import time
import argparse
from telegram_bot import TelegramBot

requests.packages.urllib3.disable_warnings()

class Nessus:
    def __init__(self, ip, port):
        self.telegram_bot = TelegramBot()
        self.username = "YOUR_USERNAME"
        self.password = "YOUR_PASSWORD"
        self.session = requests.Session()
        self.session.verify = False
        self.url = 'https://' + str(ip) + ':' + str(port)
        self.datas = []

    def login(self):
        login_api = "/session"

        response = self.session.post(self.url + login_api, json={
            "username": self.username,
            "password": self.password
        })

        response_json = json.loads(response.text)
        self.session.headers.update({'X-Cookie': "token=" + response_json["token"]})

    def scanStatus(self):
        scans_api = "/scans"
        response = self.session.get(self.url + scans_api)
        response_json = json.loads(response.text)

        scans = response_json["scans"]
        if not self.datas:
            for scan in scans:
                data = {}
                data["uuid"] = scan["uuid"]
                data["status"] = scan["status"]
                data["name"] = scan["name"]
                self.datas.append(data)
        else:
            for i in range(len(scans)):
                if self.datas[i]["status"] != scans[i]["status"]:
                    self.telegram_bot.sendMessage("Name: " + scans[i]["name"] + "\n" + "Status: " + scans[i]["status"] + "\n" + "uuid: " + scans[i]["uuid"])
                    self.datas[i]["status"] = scans[i]["status"]

def getParameter():
    parser = argparse.ArgumentParser()

    parser.add_argument("-n_ip", "--nessus_ip", type=str, help="Nessus ip", default="127.0.0.1")
    parser.add_argument("-n_port", "--nessus_port", type=str, help="Nessus port", default="8834")

    args = parser.parse_args()
    return vars(args)

def main():
    args = getParameter()
    
    nessus = Nessus(args["nessus_ip"], args["nessus_port"])
    nessus.login()
    while True:
        time.sleep(10)
        nessus.scanStatus()

if __name__ == '__main__':
    main()