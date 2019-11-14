from urllib.request import urlopen
from link_scraper import LinkScraper
from housekeeping import *
from domain import *

class Crawler: #does the actual url crawling
    
    #requires class variables that are shared among them for threading purposes
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
    def crawl(thread_name, domain, page):
        if (page[0]=='\''):
            Crawler.todo.remove(page)
            page = domain + page
            Crawler.todo.add(page)
        if not page[0]=='h':
            page = ''
        if page not in Crawler.completed:
            print(thread_name + ' crawling '+page)
            print('Queued links: ' + str(len(Crawler.todo))+'|| Completed: '+ str(len(Crawler.completed)))
            Crawler.add_todo(Crawler.find_urls(domain, page), domain)
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
    def find_urls(domain, page):
        html_string = ''
        try:
            response = urlopen(page)
            html_bytes = response.read()
            html_string = html_bytes.decode('utf-8')
            scraper = LinkScraper(domain, page)
            scraper.feed(html_string)
        except:
            print('Error, page crawled/inaccessible')
            return set()
        return scraper.pages()

    @staticmethod
    def update():
        set_to_file(Crawler.todo_f, Crawler.todo)
        set_to_file(Crawler.completed_f, Crawler.completed)