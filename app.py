import asyncio
import json

import aiohttp
import requests
from flask import Flask, jsonify, make_response, request

from modules.mods import *


#loop = asyncio.get_event_loop()
#loop.run_until_complete(website.table('https://share.dmhy.org/topics/list?keyword=&sort_id=2&team_id=117&order=date-desc'))
"""
tr_list = dmhy.animesearch('黑色五葉草','117')
title_list = website.title(tr_list)
magnet_list = website.magnet(tr_list)
anime = {}


for index in range(len(tr_list)):
    anime[index] = {}
    anime[index]['anime_title'] = title_list[index]
    anime[index]['download_magnet'] = magnet_list[index]
"""
app = Flask(__name__)

@app.route(f"/v{api.version}")
def home():
    return http.status({'status': 200, 'message': 'Welcome to dmhy RESTful API.', 'version': '1.0'}, 200)
    #return http.status(anime, 200)

@app.route(f'/v{api.version}/', defaults={'anime_title': None})
@app.route(f"/v{api.version}/<string:anime_title>")
@app.route(f'/v{api.version}/<string:anime_title>', defaults={'team_id': None})
@app.route(f"/v{api.version}/<string:anime_title>/<int:team_id>")
def anime_search(anime_title,team_id):
    """ search anime """
    tr_list = dmhy.animesearch(anime_title,team_id)
    title_list = website.title(tr_list)
    magnet_list = website.magnet(tr_list)
    anime = {}
    for index in range(len(tr_list)):
        anime[index] = {}
        anime[index]['anime_title'] = title_list[index]
        anime[index]['download_magnet'] = magnet_list[index]
    return http.status(anime, 200)


if __name__ == "__main__":
    app.run()