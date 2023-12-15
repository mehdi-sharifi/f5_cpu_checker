import os
import requests, logging
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from time import sleep

# Disable SSL warnings
disable_warnings(InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authenticate_f5(user, passwd, f5_host):
    base_url = f"https://{f5_host}/mgmt/shared/authn/login"
    auth_data = {
        "username": user,
        "password": passwd,
        "loginProviderName": "tmos"
    }
    try:
        response = requests.post(url=base_url, json=auth_data, verify=False)
        if response.status_code == 200:
            token = response.json()["token"]["token"]
            json_token = {
                "X-F5-Auth-Token": token,
                "Content-Type": "application/json"
            }
            logger.info("Authentication successful")
            return json_token
        else:
            logger.error('Wrong Username or Password!')
            return {"error": 'Wrong Username or Password!'}
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as e:
        logger.error(f"Connection error: {e}")
        return {"error": "Destination is unreachable!"}


def GetVsCpuUsage(f5_host, token):
    try:
        req_url = f'https://{f5_host}/mgmt/tm/ltm/virtual/stats'

        response = requests.get(req_url, headers=token, verify=False)
        response.raise_for_status()  # Raise an HTTPError for bad status codes

        parsed_data = response.json()['entries']
        cpu_stat = {}

        for vs in parsed_data:
            vs_name = parsed_data[vs]['nestedStats']['entries']['tmName']['description'].split('/')[2]
            cpu_val = parsed_data[vs]['nestedStats']['entries']['oneMinAvgUsageRatio']['value']
            cpu_stat[vs_name] = cpu_val

            if cpu_val >= 30:
                message = ""
                if 30 <= cpu_val < 50:
                    message = f'The virtual server named *{vs_name}* is using *{cpu_val}%* CPU :large_yellow_circle:'
                elif cpu_val >= 50:
                    message = f'The virtual server named *{vs_name}* is using *{cpu_val}%* CPU :red_circle:'

                # Send notification to Slack
                webhook_url = os.getenv('WEBHOOK_URL')
                logger.info("Webhooks send")
                payload = {'text': message}
                requests.post(webhook_url, json=payload)

        return cpu_stat

    except requests.RequestException as e:
        logging.error(f"Request Exception: {e}")
        return None

    except KeyError as e:
        logging.error(f"KeyError: {e}")
        return None

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


f5_host_1 = os.getenv('F5_HOST')
f5_user = os.getenv('F5_USER')
f5_pass = os.getenv('F5_PASS')

while True:
    token_1 = authenticate_f5(f5_user, f5_pass, f5_host_1)
    cpu_1 = GetVsCpuUsage(f5_host_1, token_1)
    sleep(60)
