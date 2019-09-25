import threading
from queue import Queue
from crawler import Crawler
from domain import *
from housekeeping import *

DIRECTORY = 'ABC'
HOMEPAGE = 'https://abcnews.go.com/'
DOMAIN = get_domain(HOMEPAGE)
TODO_FILE = DIRECTORY+'/todo.txt'
COMPLETED_FILE = DIRECTORY+'/completed.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Crawler(DIRECTORY, HOMEPAGE, DOMAIN) #first crawler scrapes the homepage and exits cleanly

def create_threads(): #creates threads and tasks them with job function
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=job)
        t.daemon = True
        t.start()

def create_jobs():
    for link in load_file(TODO_FILE):
        queue.put(link)
    queue.join()
    crawl()

def job():
    while True: #endless loop so long as there is more in the queue
        url = queue.get()
        Crawler.crawl(threading.current_thread().name, HOMEPAGE, url)
        queue.task_done()

def create_queue(): #takes the todo file and reads into the queue for threading
    queued_links = load_file(TODO_FILE)
    if len(queued_links) > 0:
        create_jobs()

def crawl():
    queued_links = load_file(TODO_FILE)
    if (len(queued_links) > 0):
        print(str(len(queued_links))+' links in the queue.')
        create_queue()
pass
create_threads()
crawl()