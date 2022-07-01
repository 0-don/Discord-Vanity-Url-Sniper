from datetime import datetime
from itertools import cycle
import signal
from lxml.html import fromstring
import requests
import os
import time

# pip install requests lxml
vanity_url = "testingtesting"
guild_id = "9396788123117356767342"
token = "OTkyNDMwMzI2NjQxMDc0MjM3.GVRQUl.WcoDseoKYNhJMuYkBAZ9ui9pnOOlxsB7ISfEKE"


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
                    proxy = ":".join(
                        [i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                    proxies.add(proxy)
            print("new proxies")
            return proxies
        except:
            pass


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
        while response == "" or response.status_code != 200:
            self.proxies = grab_proxies()
            for proxy in self.proxies:
                self.proxy = next(self.proxy_pool)
                try:
                    url = f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url"
                    response = requests.patch(
                        url, timeout=10, headers=self.headers, json=payload, proxies={"https": self.proxy})
                    if response.status_code == 200:
                        print(
                            f"{self.datetime}VANITY SNIPED : discord.gg/{vanity_url} has been sniped successfully!")
                        os._exit(1)
                    else:
                        print(
                            f"Unknown Error! Could not snipe discord.gg/{vanity_url}! Status Code : {response.status_code} | Better luck next time :(")
                except:
                    print(f"error change_vanity: {self.proxy}")

    def check_vanity(self):
        for proxy in self.proxies:
            response = ""
            while response == "":
                self.proxy = next(self.proxy_pool)
                try:
                    url = f"https://discord.com/api/v9/invites/{vanity_url}?with_counts=true&with_expiration=true"
                    # print(url)
                    response = requests.get(url, timeout=10,  proxies={
                                            "https": self.proxy})
                    if response.status_code == 404 or response.status_code == 401:
                        Change().change_vanity()
                    else:
                        print(
                            f'Status code: {response.status_code} - Proxy: {self.proxy} - still taken. attempting to snipe discord.gg/{vanity_url}')
                except:
                    print(f"error check vanity: {self.proxy}")


while True:
    Change().check_vanity()
    self.proxies = grab_proxies()
