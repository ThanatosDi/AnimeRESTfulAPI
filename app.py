from flask import Flask

from utils.logger import Logger
from utils.response import Resp
from utils.route import Route
from utils.rss import RSS

app = Flask(__name__)
route = Route()
logger = Logger(name='app')

@app.route('/')
def home():
    return route.home()

@app.route('/dmhy/list', defaults={'search': ''})
@app.route('/dmhy/list/', defaults={'search': ''})
@app.route('/dmhy/list/<string:search>')
def dmhy_list(search):
    return route.dmhy_list(search)

@app.route('/kisssub/list', defaults={'search': ''})
@app.route('/kisssub/list/', defaults={'search': ''})
@app.route('/kisssub/list/<string:search>')
def kisssub_list(search):
    return route.kisssub_list(search)

if __name__ == "__main__":
    logger.info('main', 'DMHY API start')
    app.run(port=6000, debug=False)
    pass
