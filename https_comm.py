import requests
import logging
import ssl
import argparse
import os
import urllib3
import base64
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.ssl_ import create_urllib3_context

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.WARNING)

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")


def load_config():
    config = {}
    with open(CONFIG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and ":" in line:
                key, value = line.split(":", 1)
                config[key.strip()] = value.strip()
    config['auth_user'] = base64.b64decode(config['auth_user']).decode()
    config['auth_pass'] = base64.b64decode(config['auth_pass']).decode()

    return config


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.set_ciphers('DEFAULT:@SECLEVEL=0')
        ctx.maximum_version = ssl.TLSVersion.TLSv1_2
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)


def create_guest_user(session, base_url, username, userpwd, description="", guest_wlan_id="28"):
    url = f"{base_url}/screens/aaa/guestuser_create.html"
    payload = {
        "access_control": "1",
        "username": username,
        "userpwd": userpwd,
        "pwdconfirm": userpwd,
        "lifetime_days": "30",
        "lifetime_hours": "0",
        "lifetime_mins": "0",
        "lifetime_secs": "0",
        "GuestWlanID": guest_wlan_id,
        "description": description,
        "err_flag": "",
        "err_msg": "",
        "buttonClicked": "4",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": url,
        "Origin": base_url,
    }
    r = session.post(url, data=payload, headers=headers, timeout=10)
    return r.status_code


def main():
    parser = argparse.ArgumentParser(prog="lobbyAdmin", description="Cisco Lobby Admin - Guest User Creator")
    parser.add_argument("-u", required=True, help="Guest username")
    parser.add_argument("-p", required=True, help="Guest password")
    parser.add_argument("-d", default="", help="Guest description (optional)")
    args = parser.parse_args()

    config = load_config()
    base_url = f"https://{config['host']}"

    session = requests.Session()
    session.mount('https://', SSLAdapter())
    session.verify = False
    session.auth = HTTPBasicAuth(config['auth_user'], config['auth_pass'])

    session.get(f"{base_url}/", timeout=10)
    session.get(f"{base_url}/screens/preframeset.html", timeout=10)
    session.get(f"{base_url}/screens/lobbyadmin_frameset.html", timeout=10)

    status = create_guest_user(session, base_url, args.u, args.p, args.d, config.get('guest_wlan_id', '28'))

    if status == 200:
        print("operation succeed")
    else:
        print("operation FAILED")


if __name__ == "__main__":
    main()
