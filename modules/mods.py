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
    """ website class """
    @staticmethod
    def html(url):
        """ Get html code"""
        try:
            html = requests.get(url=url)
            html.encoding = 'utf-8'
            htmlcode = BeautifulSoup(html.text, "html.parser")
            return htmlcode
        except Exception as e:
            log.write(f'>> website.html : {str(e)}')
    
    @staticmethod
    def tr(url):
        """ Get tr list """
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
        v1 defind
        # Search anime from dmhy
        # dmhy.animesearch(keyword=None,team_id=None,page=1,lang=None,ep=None)
        """
        try:
            print(f'https://share.dmhy.org/topics/list/page/{page}?keyword={keyword}+{lang}+{episode}&sort_id=2&team_id={team_id}&order=date-desc')
            return website.tr(f'https://share.dmhy.org/topics/list/page/{page}?keyword={keyword}+{lang}+{episode}&sort_id=2&team_id={team_id}&order=date-desc')
        except Exception as e:
            return log.write(f'>> dmhy.animesearch : {str(e)}')

    @staticmethod        
    def animelist(*args,page=1):
        """
        # Get anime list from dmhy\n
        # dmhy.animelist(*args(keyword),page=1)
        """
        try:
            keyword = '+'.join(args)
            return website.tr(f'https://share.dmhy.org/topics/list/page/{page}?keyword={keyword}&sort_id=2&team_id=0&order=date-desc')
        except Exception as e:
            return log.write(f'>> dmhy.animesearch : {str(e)}')

    @staticmethod
    def teamname(tr_list):
        """ v1 defind """
        try:
            teamname_list = []
            for tr in tr_list:
                if (tr.find('span',{'class':'tag'})):
                    teamname_list.append(((tr.find('span',{'class':'tag'})).text).replace('\n\n\t\t\t\t',''))
                else:
                    teamname_list.append('')
            return teamname_list
        except Exception as e:
            log.write(f'>> dmhy.teamname : {str(e)}')

    @staticmethod
    def lang(title):
        """ return anime sub language """
        try:
            list_filed = re.sub(r'(?:\[|\【|\]|\】)',' ',title).split(' ')
            while '' in list_filed:
                list_filed.remove('')
            lang = re.findall(r'(?:BIG5|GB|繁體|简体|繁中|简中|繁\/日|繁日|简日|简繁日|简繁)',' '.join(list_filed))
            if any(lang):
                lang = lang[0].upper()
                if lang.find('BIG5')==0:
                    lang = '繁體'
                if lang.find('GB')==0:
                    lang = '簡體'
            else:
                lang = '未知'
            lang =  lang.replace('简','簡').replace('体','體')
            return lang
        except Exception as e:
            log.write(f'>> dmhy.teamname : {str(e)}')

    @staticmethod
    def tag(animelist):
        """ Get anime tag  """
        try:
            tag_list = []
            for anime in animelist:
                if anime.find('span',{'class':'tag'}) is None:
                    tag_list.append('Unknow')
                else:
                    tag_list.append(anime.find('span',{'class':'tag'}).text.replace('\n','').replace('\t',''))
            return tag_list
        except Exception as e:
            return log.write(f'>> dmhy.tag : {str(e)}')
    
    @staticmethod
    def title(animelist):
        try:
            title_list = []
            for anime in animelist:
                title_list.append((anime.find('a',{'target':'_blank'}).text).replace('\n','').replace('\t',''))
            return title_list
        except Exception as e:
            log.write(f'>> dmhy.title : {str(e)}')
    
    @staticmethod
    def teamid(animelist):
        try:
            teamid_list = []
            for anime in animelist:
                if re.findall(r'team_id/\d+',str(anime)):
                    id = (re.findall(r'team_id/\d+',str(anime))[0]).split('/')[1]
                else:
                    id = 'Unknow'
                teamid_list.append(id)
            return teamid_list
        except Exception as e:
            log.write(f'>> dmhy.teamid : {str(e)}')

    @staticmethod
    def magnet(animelist):
        try:
            magnet_list = []
            for anime in animelist:
                magnet_list.append((anime.find('a',{'class':'download-arrow arrow-magnet'})['href']))
            return magnet_list
        except Exception as e:
            log.write(f'>> dmhy.magnet : {str(e)}')

    @staticmethod
    def postid(animelist):
        try:
            postid_list = []
            for anime in animelist:
                postid_list.append((re.findall(r'view/\d+',str(anime))[0]).split('/')[1])
            return postid_list
        except Exception as e:
            log.write(f'>> dmhy.postid : {str(e)}')

    @staticmethod
    def posturl(animelist):
        try:
            posturl_list = []
            for anime in animelist:
                posturl_list.append(re.findall(r'view/\d+[\S]+\"',str(anime))[0].replace('"','').split('/')[1])
            return posturl_list
        except Exception as e:
            log.write(f'>> dmhy.postid : {str(e)}')

    @staticmethod
    def filesize(animelist):
        try:
            filesize_list = []
            for anime in animelist:
                filesize_list.append(re.findall(r'[0-9]+(?:.|)[0-9]+(?:M|G)B',str(anime))[0])
            return filesize_list
        except Exception as e:
            log.write(f'>> dmhy.filesize : {str(e)}')
    
    @staticmethod
    def magnet_in_post(posturl):
        try:
            url = f'https://share.dmhy.org/topics/view/{posturl}'
            html = website.html(url)
            a_list = re.findall(r'href=\"magnet:\?xt=urn:btih:[\S]+\"',str(html))
            a_list = [a.replace('href=','').replace('"','') for a in a_list]
            return a_list
        except Exception as e:
            log.write(f'>> dmhy.title_in_post : {str(e)}')

    @staticmethod
    def fansub():
        """
        # show all fansub on dmhy
        """
        try:
            fansublist = (((website.html('https://share.dmhy.org/topics/advanced-search?team_id=0&sort_id=0&orderby=')).find('select',{'id':'AdvSearchTeam'})).find_all('option'))
            fansubs = []
            for fansub in fansublist:
                fansubsdict = {}
                fansubsdict['fansub'] = fansub.text
                fansubsdict['id'] = fansub['value']
                fansubs.append(fansubsdict)
            del fansubs[0]
            return fansubs
        except Exception as e:
            log.write(f'>> dmhy.fansub : {str(e)}')

    @staticmethod
    def tracker():
        """
        # show all tracker
        """
        try:
            tracker = {
                '動漫花園':[
                    'udp://104.238.198.186:8000/announce',
                    'http://104.238.198.186:8000/announce',
                    'http://t.nyaatracker.com/announce',
                    'http://opentracker.acgnx.se/announce',
                    'https://opentracker.acgnx.se/announce',
                    'http://opentracker.acgnx.com:6869/announce',
                    'http://tracker.xfsub.com:6868/announce',
                    'http://tracker.dm258.cn:7070/announce'
                ],
                'AxgnX末日動漫資源庫':[
                    'http://opentracker.acgnx.se/announce',
                    'https://opentracker.acgnx.se/announce',
                    'http://opentracker.acgnx.com:6869/announce'
                ],
                'ACG.RIP':[
                    'http://t.acg.rip:6699/announce',
                    'http://share.camoe.cn:8080/announce'
                ],
                '萌番組':[
                    'udp://tr.bangumi.moe:6969/announce',
                    'https://tr.bangumi.moe:9696/announce',
                    'http://tr.bangumi.moe:6969/announce'
                ],
                '旋風動漫':[
                    'http://tracker.xfsub.com:6868/announce',
                    'http://tracker.dm258.cn:7070/announce'
                ],
                'Nyaa.si':[
                    'http://nyaa.tracker.wf:7777/announce'
                ],
                'Nyaa Pantsu':[
                    'udp://tracker.doko.moe:6969'
                ],
                'AcgnX Torrent Global':[
                    'http://tracker.acgnx.se/announce',
                    'https://tracker.acgnx.se/announce',
                    'udp://tracker.acgnx.se/announce'
                ]
            }
            return tracker
        except Exception as e:
            log.write(f'>> dmhy.tracker : {str(e)}')


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
        
    @staticmethod
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
