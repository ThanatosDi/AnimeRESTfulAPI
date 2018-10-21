import asyncio
import json

import aiohttp
import requests
from flask import Flask, jsonify, make_response, request

from modules.mods import *


#loop = asyncio.get_event_loop()
#loop.run_until_complete(website.table('https://share.dmhy.org/topics/list?keyword=&sort_id=2&team_id=117&order=date-desc'))
tr_list = website.tr('https://share.dmhy.org/topics/list?keyword=&sort_id=2&team_id=117&order=date-desc')
title_list = website.title(tr_list)
magnet_list = website.magnet(tr_list)
message = {}


for index in range(len(tr_list)):
    message[index] = {}
    message[index]['title'] = title_list[index]
    message[index]['magnet'] = magnet_list[index]

app = Flask(__name__)

@app.route(f"/v{api.version}")
def home():
    #return http.status({'status': 200, 'message': 'Welcome to dmhy RESTful API.', 'version': '1.0'}, 200)
    return http.status(message, 200)

@app.route(f"/v{api.version}/<int:type>")
def anime_type(type):
    """ ???? """


if __name__ == "__main__":
    app.run()