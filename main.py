import os
import time
import requests

from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

DOMAIN_NAME = os.getenv("DOMAIN_NAME")
TOKEN = os.getenv("TOKEN")
INTERVAL = int(os.getenv("INTERVAL", 60))  # Default to 60 seconds if not set

def update_public_ip(domain_name: str, token: str):
    url = "https://update.dedyn.io/"
    
    print(f"Updating IP for {domain_name} with token {token}...")
     
    try:
        response = requests.get(url, auth=HTTPBasicAuth(domain_name, token), timeout=10)
        if response.status_code == 200:
            print("IP update successful:", response.text)
        else:
            print(f"Failed to update IP: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print("Error updating IP:", e)


def get_public_ip():
    try:
        response = requests.get("https://ifconfig.me", timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching IP: {e}")
        return None

if __name__ == "__main__":
    last_public_ip = None 
    
    print(f"Fetching public IP every {INTERVAL} seconds...")

    while True:
        ip = get_public_ip()
        if ip and ip != last_public_ip:
            print(f"Public IP changed: {ip}")
            last_public_ip = ip
            update_public_ip(DOMAIN_NAME, TOKEN)
        else:
            print(f"Public IP unchanged: {ip}")
        # Wait for the specified interval before checking again
        time.sleep(INTERVAL)
         