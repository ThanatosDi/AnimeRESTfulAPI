from utils.response import Resp
from utils.rss import RSS


class Route:
    def home(self):
        return Resp({'message':'Anime RSS API','support':{'動漫花園 DMHY':'https://api-anime.kawai.moe/dmhy/list','愛戀動漫 kisssub':'https://api-anime.kawai.moe/kisssub/list'}, 'status': 200}, 200)._dict

    def dmhy_list(self, search):
        rss = RSS(f'https://share.dmhy.org/topics/rss/sort_id/2/rss.xml?keyword={search}').filter
        return Resp({'message': 'success', 'status': 200, 'data': rss}, 200)._dict

    def kisssub_list(self, search):
        rss = RSS(f'http://www.kisssub.org/rss-{search}.xml').filter
        return Resp({'message': 'success', 'status': 200, 'data': rss}, 200)._dict
