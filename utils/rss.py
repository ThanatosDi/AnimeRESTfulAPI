import requests
import feedparser

class RSS:
    def __init__(self, RSS):
        """Get anime RSS
        
        Arguments:
            RSS {str} -- anime rss url or text.
        """
        self.RSS = RSS

    def request(self, url):
        """request
        
        Arguments:
            url {str} -- RSS url
        """
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
        with requests.get(url, headers=header) as req:
            if req.status_code!=200:
                return None
            req.encoding = 'utf-8'
            return req.text

    def feedparser(self, RSS):
        """feedparser
        
        Arguments:
            RSS {str} -- RSS url or text
        """
        return feedparser.parse(RSS)
    
    @property
    def text(self):
        return self.request(self.RSS)

    @property
    def feed_detail(self):
        feed = self.feedparser(self.text).feed
        return feed

    @property
    def feeddict(self):
        feed_list = []
        for feed in self.feedparser(self.text).entries:
            feed_dict = {}
            feed_dict['title'] = feed.title
            feed_dict['link'] = feed.link
            feed_dict['short_magnet'] = feed.links[1].href.split('&')[0]
            feed_dict['magnet'] = feed.links[1].href
            feed_list.append(feed_dict)
        return feed_list
    
    @property
    def filter(self):
        feed_list = []
        dict_filter = {
            'dmhy':{
                'title': 'title',
                'link': 'link',
                'short_magnet': 'links[1].href.split("&")[0]',
                'magnet': 'links[1].href'
            }
        }
        if 'kisssub' in self.feed_detail.link:
            feed_list = []
            for feed in self.feedparser(self.text).entries:
                feed_dict = {}
                feed_dict['title'] = feed.title
                feed_dict['link'] = feed.link
                feed_dict['magnet'] = 'magnet:?xt=urn:btih:'+feed.link.split('-')[1].split('.')[0]
                feed_list.append(feed_dict)
            return feed_list
        elif 'dmhy' in self.feed_detail.link:
            feed_list = []
            for feed in self.feedparser(self.text).entries:
                feed_dict = {}
                feed_dict['title'] = feed.title
                feed_dict['link'] = feed.link
                feed_dict['short_magnet'] = feed.links[1].href.split('&')[0]
                feed_dict['magnet'] = feed.links[1].href
                feed_list.append(feed_dict)
            return feed_list