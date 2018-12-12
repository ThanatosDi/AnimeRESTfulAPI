import asyncio
import re
import time

import aiohttp
import requests
from flask import (Flask, jsonify, make_response, render_template, request,
                   send_from_directory)

from modules.mods import *

app = Flask(__name__)

@app.route(f"/v1")
def v1home():
    return http.sortstatus({'status': 200, 'message': 'Welcome to dmhy RESTful API.', 'version': '1.0'}, 200)
    #return http.status(anime, 200)
#/
@app.route(f'/v1/list/', defaults={'anime_title': '','page':'1','lang':'tc','episode':'','team_id':''})
@app.route(f"/v1/list/<string:anime_title>")
@app.route(f"/v1/list/<string:lang>")
@app.route(f"/v1/list/p<int:page>")
@app.route(f"/v1/list/team<int:team_id>")

@app.route(f"/v1/list/<string:anime_title>/p<int:page>")
@app.route(f"/v1/list/<string:anime_title>/<string:lang>")
@app.route(f"/v1/list/<string:anime_title>/ep<int:episode>")
@app.route(f"/v1/list/<string:anime_title>/team<int:team_id>")

@app.route(f"/v1/list/<string:anime_title>/<string:lang>/p<int:page>")
@app.route(f"/v1/list/<string:anime_title>/<string:lang>/ep<int:episode>")
@app.route(f"/v1/list/<string:anime_title>/<string:lang>/team<int:team_id>")

@app.route(f"/v1/list/<string:lang>/p<int:page>")
@app.route(f"/v1/list/<string:lang>/team<int:team_id>")

def anime_search(anime_title='', team_id='', page=1, lang='', episode=''):
    """ search anime """
    try:
        if lang=='tc':
            lang = '繁體'
        elif lang=='sc':
            lang = '简体'
        if episode:
            episode = '{:0>2d}'.format(episode)
        tr_list = dmhy.animesearch(anime_title,team_id,page,lang,episode)
        title_list = dmhy.title(tr_list)
        magnet_list = dmhy.magnet(tr_list)
        teamid_list = dmhy.teamid(tr_list)
        teamname_list = dmhy.teamname(tr_list)
        postid_list = dmhy.postid(tr_list)
        anime = []
        for index in range(len(tr_list)):
            animedict = {}
            animedict['anime_title'] = title_list[index]
            animedict['anime_Fansub_team_id'] = teamid_list[index]
            animedict['anime_Fansub_team_name'] = teamname_list[index]
            animedict['anime_Post_id'] = postid_list[index]
            animedict['download_magnet'] = magnet_list[index]
            animedict[f'download_magnet_{postid_list[index]}'] = magnet_list[index]
            anime.append(animedict)
        return http.sortstatus(anime, 200)
    except TypeError as e:
        log.write(str(e))
        return http.not_found(f'第 {page} 頁無資料')
    except Exception as e:
        log.write(str(e))
        return http.internal_server_error(str(e))

@app.route(f"/v1/fansubs")
def fansub():
    try:
        return http.status(dmhy.fansub(),200)
    except Exception as e:
        log.write(f'>> app.fansub : {str(e)}')
        return http.internal_server_error(str(e))

@app.route(f'/v2')
def v2home():
    return http.status({'message': 'Welcome to dmhy RESTful API.', 'version': '2.0','documentation':'','status': 200}, 200)

@app.route(f'/v2/list',defaults={'keyword': ''})
@app.route(f'/v2/list/<string:keyword>')
def animelist(keyword):
    anime_list  = dmhy.animelist(keyword)
    title_list  = dmhy.title(anime_list)
    tag_list    = dmhy.tag(anime_list)
    magnet_list = dmhy.magnet(anime_list)
    size_lsit   = dmhy.filesize(anime_list)
    postid_list = dmhy.postid(anime_list)
    posturl_list = dmhy.posturl(anime_list)
    anime = []
    for index in range(len(anime_list)):
        animedict = {}
        animedict['tag']    = tag_list[index]
        animedict['postid'] = postid_list[index]
        animedict['title']  = title_list[index]
        animedict['size']   = size_lsit[index]
        animedict['lang']   = dmhy.lang(title_list[index])
        animedict['url']    = posturl_list[index]
        animedict['magnet'] = magnet_list[index]
        animedict['download'] = f'https://{config.hostname}/v2/get?keyword={keyword}&postid={postid_list[index]}'
        anime.append(animedict)
    return http.status(anime, 200)

@app.route(f'/v2/get',defaults={'keyword':'','postid':''})
@app.route(f'/v2/get?keyword=<string:keyword>&postid=<string:postid>')
def getmagnet(keyword,postid):
    start = time.time()
    keyword = request.args.get('keyword')
    postid = request.args.get('postid')
    if keyword is None or postid is None:
        return http.not_found('miss keyword or postid')
    anime_list   = dmhy.animelist(keyword)
    postid_list  = dmhy.postid(anime_list)
    if postid_list.index(postid) is not None:
        resp = requests.get(f'http://127.0.0.1:7000/v2/list/{keyword}')
        if resp.status_code!=200:
            return http.not_found('404 not found')
        animelist = json.loads(resp.text)
        anime = animelist[postid_list.index(postid)]
        animedict = {}
        animedict['title']  = anime['title']
        animedict['tag']    = anime['tag']
        animedict['magnet'] = anime['magnet']
        animedict['magnet_1'] = dmhy.magnet_in_post(anime['url'])[0]
        animedict['magnet_2'] = dmhy.magnet_in_post(anime['url'])[1]
        animedict['filesize']   = anime['size']
        animedict['lang']   = anime['lang']
    end = time.time()
    animedict['time']  = "{:.2f}".format(end-start)
    return render_template('index.html',**animedict)

@app.route(f'/v2/fansub')
def fansublist():
    return http.status(dmhy.fansub(), 200)

@app.route(f'/v2/tracker',defaults={'type':''})
@app.route(f'/v2/tracker?format=<string:type>')
def trackerlist(type):
    format_list = ['json','list']
    trackers = dmhy.tracker()
    format_ = request.args.get('format')
    if format_=='list':
        tracker = ''
        for values in list(trackers.values()):
            tracker +='<br/><br/>'.join(values)+'<br/><br/>'
        return tracker
    return http.status(trackers,200)

@app.errorhandler(404)
def _not_found(e):
    """ 404 not found"""
    return http.not_found('404 not found')

@app.errorhandler(500)
def _internal_server_error(e):
    """ Internal Server Error """
    return http.internal_server_error('Server Error')

@app.after_request
def add_header(response):
    response.cache_control.public = True
    response.cache_control.max_age = 300
    return response

if __name__ == "__main__":
    app.run(port=7000)
