import asyncio
import time

import aiohttp
import requests
from bs4 import BeautifulSoup
from flask import jsonify, make_response

from config import *


class website:
    @staticmethod
    def html(url):
        try:
            html = requests.get(url=url)
            html.encoding = 'utf-8'
            htmlcode = BeautifulSoup(html.text, "html.parser")
            return htmlcode
        except Exception as e:
            log.write(f'>> website.html : {str(e)}')
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await resp.text()
                htmlcode = BeautifulSoup(html, "html.parser")
                return htmlcode
        """

    @staticmethod
    def tr(url):
        htmlcode = website.html(url)
        tbody = htmlcode.find('tbody')
        tr_list = tbody.find_all('tr')
        return tr_list

    @staticmethod
    def title(tr_list):
        title_list = []
        for tr in tr_list:
            title_list.append((tr.find('a',{'target':'_blank'}).text).replace('\n\t\t\t\t',''))
        return title_list

    @staticmethod
    def magnet(tr_list):
        magnet_list = []
        for tr in tr_list:
            magnet_list.append((tr.find('a',{'class':'download-arrow arrow-magnet'})['href']))
        return magnet_list


class log:
    @staticmethod
    def _get_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

    @staticmethod
    def write(message):
         with open( f'{config.appname}.log','a',encoding='UTF-8') as log:
            log.write(log._get_time()+' '+message+'\n')


class http:
    @staticmethod
    def status(message, status_code):
        return make_response(jsonify(message), status_code)

class api:
    version = '1'
