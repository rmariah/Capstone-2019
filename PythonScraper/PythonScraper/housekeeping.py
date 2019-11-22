import os
# just a generic space to manage directories and and files.

def make_dir(directory): #makes a folder for the site being scraped
    if(os.path.exists(directory)): 
        pass
    else:
        os.makedirs(directory)

def create_files(directory, base_url): #creating files to save progress of the scraper as needed
    if not os.path.isfile(directory+'/todo.txt'):
        write_file(directory+"/todo.txt", base_url)
    if not os.path.isfile(directory+'/completed.txt'):
        write_file(directory+'/completed.txt', '')

def write_file(file, data): #write to the file
    f = open(file, 'w')
    f.write(data)
    f.close

def append_file(file, data): #add to a written file
  with open(file, 'a') as f:
    f.write(data+'\n')

def clear(file): #used to replace data as it's updated
   f = open(file, 'w')
   f.write('')

def load_file(file): #load the file into a set
    data = set()
    with open(file, 'rt') as f:
        for line in f:
            data.add(line.replace('\n',''))
    return data

def set_to_file(file, data): #goes through a set and saves it to a file
    clear(file)
    for link in data:
        append_file(file, link)