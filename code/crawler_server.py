
# coding: utf-8

from bs4 import BeautifulSoup as bs
import urllib2
import re
import csv
from collections import OrderedDict
import cookielib
import time

def save_cookie(cookie_file):
    cookie = cookielib.MozillaCookieJar(cookie_file)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener.open('http://archiveofourown.org/works/5051548?view_full_work=true')
    cookie.save(ignore_discard=True, ignore_expires=True)

def load_cookie(cookie_file):
    cookie = cookielib.MozillaCookieJar()
    cookie.load(cookie_file, ignore_discard=True, ignore_expires=True)
    return cookie

def find_page(base_url, page_number):
    #go to any page number.
    return base_url+'?page=' +str(page_number)

def find_works(page):
    #Find all works from a works list page.
    works_page = bs(urllib2.urlopen(page))
    links = []
    for link in works_page.find_all('a'):
        url = link.get('href')
        url_s = [i for i in url.split('/') if i != '']
        if 'work' in url and len(url_s) == 2 and str(url_s[1]).isdigit():
                links.append('http://archiveofourown.org'+link.get('href'))
    return links

def show_full_contents(url):
    #go through adult contents filtering.
    base = bs(urllib2.urlopen(url))
    full_url = url
    for link in base.find_all('a'):
        if 'Proceed' in link.text:
            full_url = url +'?view_adult=true'

#     can't show full work in the same way.
#     base2 = bs(urllib2.urlopen(full_url))
#     print full_url
#     for link in base2.find_all('a'):
#         if 'Entire Work' in link.text:
#             full_url += '?view_full_work=true'

    return full_url


def get_next_chapter(url):
    #for multi chapter works, get next chapter link.
    req = urllib2.Request(url)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    page = bs(opener.open(req))
    next_chapter = ''
    for link in page.find_all('a'):
        if 'Next Chapter' in link.text:
            next_chapter = ('http://archiveofourown.org' + link.get('href'))
    return next_chapter

def get_download_link(url):
    #may use the download page alternatively, where the html page is cleaner. But this misses some features, so not use
    #at the moment.
    req = urllib2.Request(url)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    page = bs(opener.open(req))
    for link in page.find_all('a'):
        if 'HTML' in link.text:
            download_link = 'http://archiveofourown.org' + link.get('href')
    return download_link


def get_contents(url):
    #get work metadata and contents from the work page.
#     print 'Reading url:', url
    try:
        req = urllib2.Request(url)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        page = bs(opener.open(req))
        contents = str(page.body.text.encode('utf-8')).replace('\n','A')
    except:
        print 'Unable to read from this url'
        contents = ''
        with open('/Users/jingy/Desktop/problematic_url.csv', 'a') as g:
            g.write(url)
    return url, contents

def write_header(outfile):
    f = open(outfile, 'a')
    writer = csv.writer(f, delimiter=',')
    keys = ['AdditionalTags', 'ArchiveWarnings','Author','Bookmarks','Category','Chapters','Characters','Comments',\
            'CompleteDate','Fandoms','Hits','Kudos','Language','Notes','PublishDate','Rating','Relationship',\
            'Summary','Text','Title','Words']
    writer.writerow(keys)
    f.close()

def write_work_content(work_dict,outfile):
    #write work metadata and contents as values of a sorted dictionary.
    f = open(outfile, 'a')
    writer = csv.writer(f, delimiter=',')
    try:
        writer.writerow(OrderedDict(sorted(work_dict.items())).values())
    except:
        pass
    f.close()

#creates dictionary for information in a single work.
def create_work_dict(url, contents):
    #get work metadata and contents into a dictionary.
    #Know it's not elegent...
#     print 'Getting work information from:', url
    try:
        work = {}
        
        work['Rating'] = re.findall('Rating:(.*?)<br />',contents)[0]
        work['ArchiveWarnings'] = re.findall('Warnings:(.*?)<br />',contents)[0]         
        work['Fandoms'] = [i for i in re.findall('Fandoms:A          AAA(.*?)AAAA|Fandom:A          AAA(.*?)AAAA',contents)[0] if i != ''][0]

        category = re.findall('Category:A          AAA(.*?)AAAA',contents)#|Category:A          AAAF/M|Category:A          AAAGen|Category:A          AAAM/M|Category:A          AAAMulti|Category:A          AAAOther',contents)
        if category == []:
            work['Category'] = ''
        else:
            work['Category'] = category[0].strip()

        relationship = re.findall('Relationships:(.*?)<br />',contents)
        if relationship == []:
            work['Relationship'] = ''
        else:
            work['Relationship'] = relationship[0]

        characters = re.findall('Characters:(.*?)<br />',contents)
        if characters == []:
            work['Characters'] = ''
        else:
            work['Characters'] = characters[0].strip()

        additional = re.findall('Additional Tags:(.*?)<br />',contents)
        if additional == []:
            work['AdditionalTags'] = ''
        else:
            work['AdditionalTags'] = additional[0]

        language = re.findall('Language:A      AA(.*?)A      A',contents)
        if language == []:
            work['Language'] = ''
        else:
            work['Language'] = language[0].strip()

        publishdate = re.findall('Published:([0-9]*-[0-9]*-[0-9]*)',contents)
        if publishdate == []:
            work['PublishDate'] = ''
        else:
            work['PublishDate'] = publishdate[0].strip()
            
        completedate = re.findall('Completed:([0-9]*-[0-9]*-[0-9]*)',contents)
        if completedate == []:
            work['CompleteDate'] = ''
        else:
            work['CompleteDate'] = completedate[0].strip()
        
        words = re.findall('Words:([0-9]*)',contents)
        if words == []:
            work['Words'] = ''
        else:
            work['Words'] = words[0].strip()
        
        chapters = re.findall('Chapters:([0-9]*/[0-9]*)',contents)
        if chapters == []:
            work['Chapters'] = ''
        else:
            work['Chapters'] = chapters[0].strip()
        
        comments = re.findall('Comments:([0-9]*)',contents)
        if comments == []:
            work['Comments'] = ''
        else:
            work['Comments'] = comments[0].strip()
            
        kudos = re.findall('Kudos:([0-9]*)',contents)
        if publishdate == []:
            work['Kudos'] = ''
        else:
            work['Kudos'] = kudos[0].strip()
            
        bookmarks = re.findall('Bookmarks:([0-9]*)',contents)
        if bookmarks == []:
            work['Bookmarks'] = ''
        else:
            work['Bookmarks'] = bookmarks[0].strip()
        
        hits = re.findall('Hits:([0-9]*)',contents)
        if hits == []:
            work['Hits'] = ''
        else:
            work['Hits'] = hits[0].strip()
        
        author = re.findall('A    AA(.*?)AAA',contents)
        if author == []:
            work['Author'] = ''
        else:
            work['Author'] = author[0].strip()

        text = re.findall('Work Text:(.*?)AAAAAAAA|Chapter TextA(.*?)AAAAA',contents)
        if text == []:
            work['Test'] = ''
        else:
            work['Text']= [i for i in text[0] if i != ''][0].strip()

        title = re.findall('AAAAAAAA      (.*?)A    AA',contents)
        if title == []:
            work['Title'] = ''
        else:
            work['Title']  = title[0].strip()

        summary = re.findall('>Summary: <p>(.*?)</p>',contents)
        if summary == []:
            work['Summary'] = ''
        else:
            work['Summary'] = summary[0].strip()

        notes = re.findall('Notes:AA(.*?)AA',contents)
        if notes == []:
            work['Notes'] = ''
        else:
            work['Notes'] = notes[0].strip()
        
#     print 'Finished with:', url
    except:
        print 'Something went wrong.'
    return work

def read_single_work(url):
    url_full = show_full_contents(url)
    u, c = get_contents(url_full)
    work = create_work_dict(u, c)
    write_work_content(work,outfile)

def get_chapters(url):
    url_full = show_full_contents(url)
    chapters_list = []
    next_url = get_next_chapter(url_full)
    while next_url != '':
        chapters_list.append(next_url)
        next_url = get_next_chapter(next_url)
    return chapters_list

if __name__ == "__main__":

    cookie_file = './cookie'
    cookie = load_cookie(cookie_file)

    start = 'http://archiveofourown.org/tags/Sherlock%20(TV)/works'
    outfile = './ao3_work_sherlock_test.csv'
    max_page = 3944

    write_header(outfile)
    start_time = time.clock()
    count = 0

    for i in range(1,2):#,max_page+1,25):
        page = find_page(start, i)
        worklist = find_works(page)
        for w in worklist:
            ch_list = get_chapters(w)
            if ch_list != []:
                read_single_work(w)
                for ch in ch_list:
                    read_single_work(ch)
            else:
                read_single_work(w)
            count += 1
            
        print 'crawling page:', i

    print 'Saved %s works from %s pages of tag %s in %s seconds .' %(count, i, 'Sherlock', str(time.clock() - start_time))        



