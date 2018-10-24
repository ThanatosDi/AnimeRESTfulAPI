import asyncio
import json
import re
import time

import aiohttp
import requests
from bs4 import BeautifulSoup
from flask import Response, jsonify, make_response, request

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
    
    @staticmethod
    def tr(url):
        try:
            htmlcode = website.html(url)
            tbody = htmlcode.find('tbody')
            tr_list = tbody.find_all('tr')
            return tr_list
        except Exception as e:
            log.write(f'>> website.tr : {str(e)}')

class dmhy:
    @staticmethod
    def animesearch(keyword=None,team_id=None,page=1,lang=None,episode=None):
        """
        # Search anime from dmhy
        # dmhy.animesearch(keyword=None,team_id=None,page=1,lang=None,ep=None)
        """
        try:
            print(f'https://share.dmhy.org/topics/list/page/{page}?keyword={keyword}+{lang}+{episode}&sort_id=2&team_id={team_id}&order=date-desc')
            return website.tr(f'https://share.dmhy.org/topics/list/page/{page}?keyword={keyword}+{lang}+{episode}&sort_id=2&team_id={team_id}&order=date-desc')
        except Exception as e:
            return log.write(f'>> dmhy.animesearch : {str(e)}')
    @staticmethod
    def title(tr_list):
        try:
            title_list = []
            for tr in tr_list:
                title_list.append((tr.find('a',{'target':'_blank'}).text).replace('\n\t\t\t\t',''))
            return title_list
        except Exception as e:
            log.write(f'>> website.title : {str(e)}')

    @staticmethod
    def teamname(tr_list):
        try:
            teamname_list = []
            for tr in tr_list:
                if (tr.find('span',{'class':'tag'})):
                    teamname_list.append(((tr.find('span',{'class':'tag'})).text).replace('\n\n\t\t\t\t',''))
                else:
                    teamname_list.append('')
            return teamname_list
        except Exception as e:
            log.write(f'>> website.teamname : {str(e)}')

    @staticmethod
    def teamid(tr_list):
        try:
            teamid_list = []
            for tr in tr_list:
                if re.findall(r'team_id/\d+',str(tr)):
                    id = (re.findall(r'team_id/\d+',str(tr))[0]).split('/')[1]
                else:
                    id = ''
                teamid_list.append(id)
            return teamid_list
        except Exception as e:
            log.write(f'>> website.teamid : {str(e)}')

    @staticmethod
    def magnet(tr_list):
        try:
            magnet_list = []
            for tr in tr_list:
                magnet_list.append((tr.find('a',{'class':'download-arrow arrow-magnet'})['href']))
            return magnet_list
        except Exception as e:
            log.write(f'>> website.magnet : {str(e)}')

    @staticmethod
    def postid(tr_list):
        try:
            postid_list = []
            for tr in tr_list:
                postid_list.append((re.findall(r'view/\d+',str(tr))[0]).split('/')[1])
            return postid_list
        except Exception as e:
            log.write(f'>> website.postid : {str(e)}')
    @staticmethod
    def fansub():
        """
        # show all fansub on dmhy
        """
        try:
            fansublist = (((website.html('https://share.dmhy.org/topics/advanced-search?team_id=0&sort_id=0&orderby=')).find('select',{'id':'AdvSearchTeam'})).find_all('option'))
            fansubs = {}
            for fansub in fansublist:
                fansubs[fansub.text] = fansub['value']
            return fansubs
        except Exception as e:
            log.write(f'>> dmhy.fansub : {str(e)}')


class log:
    @staticmethod
    def _get_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

    @staticmethod
    def write(message):
         with open( f'{config.appname}.log','a',encoding='UTF-8') as logfile:
            logfile.write(log._get_time()+' '+message+'\n')


class http:
    @staticmethod
    def sortstatus(obj, status_code):
        http.req(status_code)
        return make_response(jsonify(obj), status_code)
    
    def status(obj, status_code):
        http.req(status_code)
        return Response(json.dumps(obj, ensure_ascii=False).encode("utf8"), mimetype='application/json',status=status_code)

    @staticmethod
    def req(status_code):
        with open( f'{config.appname}.req.log','a',encoding='UTF-8') as logfile:
            message = f'{request.headers.get("X-Real-Ip", request.remote_addr)} - - {log._get_time()} {request.method} {request.path}'
            if request.args.get("page") or request.args.get("lang") or request.args.get("team"):
                message += f'?page={request.args.get("page")}&lang={request.args.get("lang")}&team={request.args.get("team")}'
            message += f' {request.environ.get("SERVER_PROTOCOL")} {status_code} -\n'
            return logfile.write(message)

    @staticmethod
    def not_found(e):
        """ 404 not found"""
        return http.sortstatus({'message':str(e),'status':'404'},404)
    
    @staticmethod
    def internal_server_error(e):
        """ Internal Server Error """
        return http.sortstatus({'message':str(e),'status':'500'},500)

class api:
    version = '1'
