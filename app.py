import asyncio
import re

import aiohttp
import requests
from flask import Flask, jsonify, make_response, request

from modules.mods import *

app = Flask(__name__)

@app.route(f"/v{api.version}")
def home():
    return http.sortstatus({'status': 200, 'message': 'Welcome to dmhy RESTful API.', 'version': '1.0'}, 200)
    #return http.status(anime, 200)
#/
@app.route(f'/v{api.version}/list/', defaults={'anime_title': '','page':'1','lang':'tc','episode':'','team_id':''})
@app.route(f"/v{api.version}/list/<string:anime_title>")
@app.route(f"/v{api.version}/list/<string:lang>")
@app.route(f"/v{api.version}/list/p<int:page>")
@app.route(f"/v{api.version}/list/team<int:team_id>")

@app.route(f"/v{api.version}/list/<string:anime_title>/p<int:page>")
@app.route(f"/v{api.version}/list/<string:anime_title>/<string:lang>")
@app.route(f"/v{api.version}/list/<string:anime_title>/ep<int:episode>")
@app.route(f"/v{api.version}/list/<string:anime_title>/team<int:team_id>")

@app.route(f"/v{api.version}/list/<string:anime_title>/<string:lang>/p<int:page>")
@app.route(f"/v{api.version}/list/<string:anime_title>/<string:lang>/ep<int:episode>")
@app.route(f"/v{api.version}/list/<string:anime_title>/<string:lang>/team<int:team_id>")

@app.route(f"/v{api.version}/list/<string:lang>/p<int:page>")
@app.route(f"/v{api.version}/list/<string:lang>/team<int:team_id>")

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

@app.route(f"/v{api.version}/fansubs")
def fansub():
    try:
        return http.status(dmhy.fansub(),200)
    except Exception as e:
        log.write(f'>> app.fansub : {str(e)}')
        return http.internal_server_error(str(e))

@app.route(f"/v{api.version}/test")
def test():
    try:
        return http.status(['sdada','abbb','caas'],200)
    except Exception as e:
        log.write(f'>> app.fansub : {str(e)}')
        return http.internal_server_error(str(e))

@app.errorhandler(404)
def _not_found(e):
    """ 404 not found"""
    return http.not_found('404 not found')

@app.errorhandler(500)
def _internal_server_error(e):
    """ Internal Server Error """
    return http.internal_server_error('Server Error')


if __name__ == "__main__":
    app.run(port=7000)
