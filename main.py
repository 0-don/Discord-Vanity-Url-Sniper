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
        
        self.headers = {"authorization": self.token, "user-agent": generate_user_agent()}
        self.session = requests.Session()
        self.session.mount("", HTTPAdapter(max_retries=1))
        
        self.payload = {"code": self.vanity_url}
        self.proxy_pool = cycle(self.grab_proxies())
        self.proxy = next(self.proxy_pool)
        
    def grab_proxies(self):
        proxies = set()
        
        page = self.request("https://sslproxies.org/", "get", proxies={})
        soup = BeautifulSoup(page.text, "html.parser")

        table = soup.find(
            "table", attrs={"class": "table table-striped table-bordered"})
        for row in table.findAll("tr"):
            count = 0
            proxy = ""
            for cell in row.findAll("td"):
                if count == 1:
                    proxy += ":" + cell.text.replace("&nbsp;", "")
                    proxies.add(proxy)
                    break
                proxy += cell.text.replace("&nbsp;", "").replace("\r", "")
                count += 1
                
        text = self.request("https://www.proxy-list.download/api/v1/get?type=https", "get", proxies={}).text

        for proxy in text.split("\n"):
            if len(proxy) > 0:
                proxies.add(proxy.replace("\r", ""))

        proxies = list(proxies)
        random.shuffle(proxies)
        proxies.append("end")
        return proxies

    def change_vanity(self):
        url = f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url"
        response = self.request(url=url, type="patch", proxies={"https": self.proxy})
        if response.status_code == 200:
            print(f"{self.datetime} VANITY SNIPED : discord.gg/{vanity_url} has been sniped successfully!")
            os._exit(1)
        else:
            print(f"Could not snipe discord.gg/{vanity_url}! Status Code : {response.status_code} | Better luck next time :(")

    def check_vanity(self):
        url = f"https://discord.com/api/v9/invites/{self.vanity_url}?with_counts=true&with_expiration=true"
        response = self.request(url=url, type="get", proxies={"https": self.proxy})
        try:
            if response.status_code == 404:
                print(f"proxy is free trying to change: {self.proxy}")
                # os._exit(1)
                self.change_vanity()
            elif response.status_code == 200:
                print(f'Proxy is good: {self.proxy} but url is still taken')
                # os._exit(1)
                time.sleep(5)
            elif response.status_code == 429:
                print(f'Proxy has made to many requests: {self.proxy}')
                next(self.proxy_pool)
            elif response.status_code:
                print(f'Status code: {response.status_code} - Proxy: {self.proxy} - still taken. attempting to snipe discord.gg/{self.vanity_url}')
        except:
            print(response)
                    
    def request(self, url, type, proxies):
        try:
            if(type == "get"):
                return self.session.get(url, timeout=5, proxies=proxies, headers={"user-agent": generate_user_agent()})
            elif(type == "patch"):
                return self.session.patch(url, timeout=5, proxies=proxies, headers=self.headers, json=self.payload)
        except requests.exceptions.Timeout:
            self.proxy = next(self.proxy_pool)
            return f"Timeout: {self.proxy}"
        except requests.exceptions.ProxyError:
            self.proxy = next(self.proxy_pool)
            return f"ProxyError: {self.proxy}"
        except requests.exceptions.SSLError:
            self.proxy = next(self.proxy_pool)
            return f"SSLError: {self.proxy}"
    
    def start(self):
        self.check_vanity()
        

            
Sniper().start()
# print(datetime.now().strftime('[On %Y-%m-%d @ %H:%M:%S]'))
