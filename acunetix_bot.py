import requests
import json
import time
import argparse
from telegram_bot import TelegramBot

requests.packages.urllib3.disable_warnings()

class Acunetix:
    def __init__(self, ip, port):
        self.telegram_bot = TelegramBot()
        self.username = 'YOUR_USERNAME'
        self.password = 'YOUR_PASSWORD'
        self.session = requests.Session()
        self.session.verify = False
        self.url = 'https://' + str(ip) + ':' + str(port)
        self.target_id = ''
        self.target = ''
        self.description = ''
        self.target_ids = []
        
    def login(self):
        login_api = '/api/v1/me/login'

        self.session.post(self.url + login_api, json={
            'email': self.username,
            'password': self.password,
            'remember_me': 'false',
            'logout_previous': 'true'
        }, verify=False)

        ui_session = self.session.cookies.get_dict()['ui_session']
        self.session.headers.update({'X-Auth': ui_session})

    def addTarget(self, target, description):
        self.target = target
        self.description = description
        add_target_api = '/api/v1/targets/add'

        response = self.session.post(self.url + add_target_api, json={
            "targets": [{
                "address": str(target),
                "description": str(description)
            }],
            "groups": []
        })

        response_json = json.loads(response.text)
        self.target_id = response_json["targets"][0]["target_id"]

        self.telegram_bot.sendMessage('Add target: ' + target + '\n' + 'Add description: ' + description)

    def configurateTarget(self, username=None, password=None):
        patch_targets_api = '/api/v1/targets/{}'.format(self.target_id)
        self.session.patch(self.url + patch_targets_api, json={
            "description": self.description,
            "criticality":30
        })

        post_target_continuous_scan_api = '/api/v1/targets/{}/continuous_scan'.format(self.target_id)
        self.session.post(self.url + post_target_continuous_scan_api, json={
            "enable": "false"
        })

        patch_targets_configuration_api = '/api/v1/targets/{}/configuration'.format(self.target_id)
        if username != None and password != None:
            self.session.patch(self.url + patch_targets_configuration_api, json={
                "scan_speed": "fast",
                "login": {
                    "kind": "automatic",
                    "credentials": {
                        "enabled": "true",
                        "username": str(username),
                        "password": str(password)
                    }
                },
                "ssh_credentials": {
                    "kind": "none"
                },
                "sensor": "false",
                "user_agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.21",
                "case_sensitive": "auto",
                "limit_crawler_scope": "true",
                "excluded_paths": [],
                "authentication":{
                    "enabled": "false"
                },
                "proxy": {
                    "enabled": "false"
                },
                "technologies": [],
                "custom_headers": [],
                "custom_cookies": [],
                "debug": "false",
                "client_certificate_password": "",
                "client_certificate_url": None,
                "issue_tracker_id": "",
                "excluded_hours_id": ""
            })
        else:
            self.session.patch(self.url + patch_targets_configuration_api, json={
                "scan_speed": "fast",
                "login": {
                    "kind": "none"
                },
                "ssh_credentials": {
                    "kind": "none"
                },
                "sensor": "false",
                "user_agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.21",
                "case_sensitive": "auto",
                "limit_crawler_scope": "true",
                "excluded_paths": [],
                "authentication":{
                    "enabled": "false"
                },
                "proxy": {
                    "enabled": "false"
                },
                "technologies": [],
                "custom_headers": [],
                "custom_cookies": [],
                "debug": "false",
                "client_certificate_password": "",
                "client_certificate_url": None,
                "issue_tracker_id": "",
                "excluded_hours_id": ""
            })

    def scanTarget(self):
        scans_target_api = '/api/v1/scans'
        self.session.post(self.url + scans_target_api, json={
            "profile_id": "11111111-1111-1111-1111-111111111111",
            "ui_session_id": "2caa59779cfc3e1844298f017d355398",
            "incremental": "false",
            "schedule": {
                "disable": "false", 
                "start_date": None,
                "time_sensitive": "false"
            },
            "target_id": self.target_id
        })

        self.telegram_bot.sendMessage('Start scanning ... ')

    def allScanStatus(self):
        scans_api = '/api/v1/scans?l=100'
        response = self.session.get(self.url + scans_api)
        response_json = json.loads(response.text)
        
        if not self.target_ids:
            for scan in response_json["scans"]:
                data = {}
                data["target_id"] = scan["target_id"]
                data["target"] = scan["target"]["address"]
                data["description"] = scan["target"]["description"]
                data["status"] = scan["current_session"]["status"]
                data["severity_counts"] = scan["current_session"]["severity_counts"]
                self.target_ids.append(data)
        else:
            scans = response_json["scans"]
            for i in range(len(scans)):
                if self.target_ids[i]["status"] != scans[i]["current_session"]["status"]:
                    self.telegram_bot.sendMessage("Target: " + self.target_ids[i]["target"] + '\n' + 'Status: ' + scans[i]["current_session"]["status"])
                    self.target_ids[i]["status"] = scans[i]["current_session"]["status"]

                    if self.target_id == scans[i]["target_id"] and 'in progress' != self.target_ids[i]["status"]:
                        self.telegram_bot.sendMessage("End scanning ... ")
                        
                        return True
        
        return False

def getParameter():
    parser = argparse.ArgumentParser()

    parser.add_argument("-a_ip", "--acunetix_ip", type=str, help="Acunetix ip", default="127.0.0.1")
    parser.add_argument("-a_port", "--acunetix_port", type=str, help="Acunetix port", default="13443")
    parser.add_argument("-t", type=str, help="Target address", required=True)
    parser.add_argument("-d", "--description", type=str, help="Target description", required=True)
    parser.add_argument("-u", "--username", type=str, help="Target username", default=None)
    parser.add_argument("-p", "--password", type=str, help="Target password", default=None)
    parser.add_argument("-s", "--scan_status", action=argparse.BooleanOptionalAction, help="Only check scanning board")

    args = parser.parse_args()
    return vars(args)

def main():
    args = getParameter()

    if args["scan_status"] == False:
        acunetix = Acunetix(args["acunetix_ip"], args["acunetix_port"])
        acunetix.login()
        acunetix.addTarget(args["t"], args["description"])
        acunetix.configurateTarget(username=args["username"], password=args["password"])
        acunetix.scanTarget()

    while True:
        time.sleep(10)
        status = acunetix.allScanStatus()
        if status == True:
            break

if __name__ == '__main__':
    main()