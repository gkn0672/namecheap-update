import os
import time
import requests

from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

DOMAIN_NAME = os.getenv("DOMAIN_NAME")
TOKEN = os.getenv("TOKEN")
INTERVAL = int(os.getenv("INTERVAL", 60))  # Default to 60 seconds if not set

import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # Logs to stdout (for Docker logs)
    ]
)

logger = logging.getLogger("desec-update")

def update_public_ip(domain_name: str, token: str):
    url = "https://update.dedyn.io/"
    
    logger.info(f"Updating IP for {domain_name} with token {token}...")
     
    try:
        response = requests.get(url, auth=HTTPBasicAuth(domain_name, token), timeout=10)
        if response.status_code == 200:
            logger.info(f"IP update successful: {response.text}")
        else:
            logger.info(f"Failed to update IP: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logger.info("Error updating IP:", e)


def get_public_ip():
    try:
        response = requests.get("https://ifconfig.me", timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        logger.info(f"Error fetching IP: {e}")
        return None

if __name__ == "__main__":
    last_public_ip = None 
    
    logger.info(f"Fetching public IP every {INTERVAL} seconds...")

    while True:
        ip = get_public_ip()
        if ip and ip != last_public_ip:
            logger.info(f"Public IP changed: {ip}")
            last_public_ip = ip
            update_public_ip(DOMAIN_NAME, TOKEN)
        else:
            logger.info(f"Public IP unchanged: {ip}")
        # Wait for the specified interval before checking again
        time.sleep(INTERVAL)
         