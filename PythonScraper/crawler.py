from urllib3 import *
from link_scraper import LinkScraper
from housekeeping import *
from domain import *

class Crawler: #does the actual url crawling
    
    #requires class variables that are shared among them for threading purpose
    domain = ''
    todo_f = 'todo.txt'
    completed_f = 'completed.txt'
    todo = set()
    completed = set()
    
    def __init__(self):
        self.start()
    
    @staticmethod
    def start(): #the initial Crawler has to produce the necessary files, and future crawlers must read in the todo and completed
        create_files()
        Crawler.todo = load_file(Crawler.todo_f)
        Crawler.completed = load_file(Crawler.completed_f)

    @staticmethod
    def crawl(thread_name, domain, page, Dict):
        if (page[0]=="/"):
            Crawler.todo.remove(page)
            if (page[1]=="/"):
                page = "https:"+page
            else:
                page = domain + page
            Crawler.todo.add(page)
        if not page[0]=='h':
            page = ''
        if page not in Crawler.completed:
            print(thread_name + ' crawling '+page)
            print('Queued links: ' + str(len(Crawler.todo))+'|| Completed: '+ str(len(Crawler.completed)))
            if (not domain in Dict):
                Dict[domain]=0
            file_name = domain + "_" +str(Dict[domain])+".html"
            Dict[domain] = Dict[domain]+1
            Crawler.add_todo(Crawler.find_urls(domain, page, file_name, Dict), domain)
            if(page!=''):
                Crawler.todo.remove(page)
            Crawler.completed.add(page)
            Crawler.update()

    @staticmethod
    def add_todo(links, domain):
        for url in links:
            if url in Crawler.todo:
                continue
            if url in Crawler.completed:
                continue
            if domain not in url:
                continue
            Crawler.todo.add(url)

    @staticmethod
    def find_urls(domain, page, file_name, Dict):
        html_string = ''
        try:
            https = PoolManager()
            response = https.request('GET', page)
            html_bytes = response.data
            html_string = html_bytes.decode('utf-8')
            f = open("HTML/"+file_name, 'wb')
            f.write(html_bytes)
            f.close()
            scraper = LinkScraper(domain, page)
            scraper.feed(html_string)
        except:
            print('Error, page crawled/inaccessible')
            Dict[domain]-=1
            return set()
        return scraper.pages()

    @staticmethod
    def update():
        set_to_file(Crawler.todo_f, Crawler.todo)
        set_to_file(Crawler.completed_f, Crawler.completed)