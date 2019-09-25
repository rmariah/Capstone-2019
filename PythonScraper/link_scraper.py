from html.parser import HTMLParser
from urllib import parse

class LinkScraper(HTMLParser): #overwriting some of HTMLParsers methods for specific functionality in finding URLs

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs): #finds <a> tag and then if 'href' is a class attribute, pull the value and store it
        if tag == 'a':
            for (attr,value) in attrs:
                if attr == 'href':
                    url = parse.urljoin(self.base_url, value) #if full url, do nothing, else attach base url to value
                    self.links.add(url)
    
    def pages(self):
        return self.links

    def error(self, message): #required error handler inherited from HTMLParser
        pass

