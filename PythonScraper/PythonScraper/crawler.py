from urllib.request import urlopen
from link_scraper import LinkScraper
from housekeeping import *

class Crawler: #does the actual url crawling
    
    #requires class variables that are shared among them for threading purposes
    domain = 'go.com'
    todo_f = 'ABC/todo.txt'
    completed_f = 'ABC/completed.txt'
    todo = set()
    completed = set()
    
    def __init__(self, directory, base_url, domain):
        self.directory = directory
        self.base_url = base_url
        self.domain = domain
        self.start(directory, base_url)
        self.crawl("1st crawler", base_url, base_url)
    
    @staticmethod
    def start(directory, base_url): #the initial Crawler has to produce the necessary files, and future crawlers must read in the todo and completed
        make_dir(directory);
        create_files(directory, base_url)
        Crawler.todo = load_file(Crawler.todo_f)
        Crawler.completed = load_file(Crawler.completed_f)

    @staticmethod
    def crawl(thread_name, base_url, page):
        if page not in Crawler.completed:
            print(thread_name + ' crawling '+page)
            print('Queued links: ' + str(len(Crawler.todo))+'|| Completed: '+ str(len(Crawler.completed)))
            Crawler.add_todo(Crawler.find_urls(base_url, page))
            Crawler.todo.remove(page)
            Crawler.completed.add(page)
            Crawler.update()

    @staticmethod
    def add_todo(links):
        for url in links:
            if url in Crawler.todo:
                continue
            if url in Crawler.completed:
                continue
            if Crawler.domain not in url:
                continue
            Crawler.todo.add(url)

    @staticmethod
    def find_urls(base_url, page):
        html_string = ''
        try:
            response = urlopen(page)
            html_bytes = response.read()
            html_string = html_bytes.decode('utf-8')
            scraper = LinkScraper(base_url, page)
            scraper.feed(html_string)
        except:
            print('Error, can not crawl page')
            return set()
        return scraper.pages()

    def update():
        set_to_file(Crawler.todo_f, Crawler.todo)
        set_to_file(Crawler.completed_f, Crawler.completed)