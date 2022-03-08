from datetime import datetime
from itertools import cycle
import signal
from lxml.html import fromstring
import requests
import os
import time

# pip install requests lxml
vanity_url = "your_url"
guild_id = "693908423486143824"
webhook = "https://discord.com/api/webhooks/693908423486143824/BwKrOBsuhjkhjkhjkhkjf26swxxjeFUPRuDaWj2LDmrJft"
token = "mfa.BmuKasdasdaCf9IPnlwwWb8uZTdnneBUhKLghjgsXp5rY44bPk9fRgRmMOnvdfgdfgYH1"

def grab_proxies():
    url = 'https://sslproxies.org/'
    r = ""
    while r == "":
        try: 
            r = requests.get(url)
            parser = fromstring(r.text)
            proxies = set()
            for i in parser.xpath('//tbody/tr')[:10]:
                if i.xpath('.//td[7][contains(text(),"yes")]'):
                    proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                    proxies.add(proxy)
            print("new proxies")
            return proxies
        except:
            time.sleep(5)

class Change:
    def __init__(self):
        self.proxies = grab_proxies()
        self.proxy_pool = cycle(self.proxies)
        self.proxy = next(self.proxy_pool)
        self.datetime = datetime.now().strftime('[On %Y-%m-%d @ %H:%M:%S]')
        self.headers = {"authorization": token,
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}

    def change_vanity(self):
        payload = {"code": vanity_url}
        response = ""
        while response == "":
            try:
                response = requests.patch(f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url", headers=self.headers, json=payload, proxies={"http": self.proxy})
                if response.status_code == 200:
                    data = {"content" : f"Vanity URL : discord.gg/{vanity_url} has been sniped successfully! | GGs :flushed: ", "username" : "Bot."}
                    requests.post(webhook, json=data)
                    print(f"{self.datetime}VANITY SNIPED : discord.gg/{vanity_url} has been sniped successfully!")
                    os._exit(1)
                else:
                    print(f"Unknown Error! Could not snipe discord.gg/{vanity_url}! Status Code : {response.status_code} | Better luck next time :(")
            except:
                time.sleep(1)

    def check_vanity(self):
        for proxy in self.proxies:
            self.proxy = next(self.proxy_pool)
            response = ""
            while response == "":
                try:
                    response = requests.get(f"https://discord.com/api/v9/invites/{vanity_url}?with_counts=true&with_expiration=true", headers=self.headers, proxies={"http": self.proxy})
                    if response.status_code == 404:
                        Change().change_vanity()
                    else:
                        print(f'Status code: {response.status_code} - Proxy: {self.proxy} - still taken. [attempting to snipe discord.gg/{vanity_url}')
                except:
                    time.sleep(1)

while True:
    Change().check_vanity()
