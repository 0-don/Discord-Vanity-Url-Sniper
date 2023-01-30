import os
import random
import requests
import time

from itertools import cycle
from datetime import datetime
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from dotenv import dotenv_values
from user_agent import generate_user_agent

config = dotenv_values(".env") 

class Sniper:
    def __init__(self):
        self.vanity_url = config.get("VANITY_URL")
        self.guild_id = config.get("GUILD_ID")
        self.token = config.get("TOKEN")

        self.headers = {
            "authorization": self.token, 
            "user-agent": generate_user_agent()
        }
        self.session = requests.Session()
        self.session.mount("", HTTPAdapter(max_retries=3))

        self.payload = {"code": self.vanity_url}
        self.proxies = self.grab_proxies()
        self.num_proxies = len(self.proxies)
        self.current_proxy_index = 0

    def grab_proxies(self):
        # code to fetch proxy list

    def get_proxy(self):
        if self.num_proxies > 0:
            proxy = self.proxies[self.current_proxy_index]
            self.current_proxy_index = (self.current_proxy_index + 1) % self.num_proxies
            return proxy
        return None

    def check_vanity_url(self):
        while True:
            try:
                proxy = self.get_proxy()
                if proxy:
                    self.session.proxies = {"http": proxy, "https": proxy}
                response = self.session.post(
                    f"https://discord.com/api/v6/guilds/{self.guild_id}/vanity-url", 
                    headers=self.headers, 
                    json=self.payload
                )
                if response.status_code == 409:
                    return True
                elif response.status_code == 429:
                    reset_after = int(response.headers.get("X-RateLimit-Reset-After", 30))
                    time.sleep(reset_after)
                elif response.status_code == 200:
                    return False
                time.sleep(random.uniform(1, 5))
            except Exception as ex:
                print(ex)
                time.sleep(5)

if __name__ == "__main__":
    sniper = Sniper()
    if sniper.check_vanity_url():
        print(f"Vanity URL {sniper.vanity_url} is taken.")
    else:
        print(f"Vanity URL {sniper.vanity_url} is available.")
