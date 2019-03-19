
# coding: utf-8

# In[76]:

from bs4 import BeautifulSoup as bs
import urllib2
import re
import csv
from collections import OrderedDict
import cookielib
import time


# In[77]:

start = 'http://archiveofourown.org/tags/Sherlock%20(TV)/works'
outfile = './ao3_work_sherlock_all_4.csv'
start_page = 1581
max_page = 3870


# In[78]:

cookie_file = './cookie'


# In[79]:

def save_cookie(cookie_file):
    cookie = cookielib.MozillaCookieJar(cookie_file)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open('http://archiveofourown.org/works/5051548?view_adult=true')
    cookie.save(ignore_discard=True, ignore_expires=True)


# In[80]:

def load_cookie(cookie_file):
    cookie = cookielib.MozillaCookieJar()
    cookie.load(cookie_file, ignore_discard=True, ignore_expires=True)
    return cookie


# In[81]:

# save_cookie(cookie_file)
cookie = load_cookie(cookie_file)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))


# In[82]:

def find_page(base_url, page_number):
    #go to any page number.
    return base_url+'?page=' +str(page_number)


# In[83]:

def find_works(page):
    #Find all works from a works list page.
    works_page = bs(urllib2.urlopen(page))
    links = []
    for link in works_page.find_all('a'):
        try:
            url = link.get('href')
            url_s = [i for i in url.split('/') if i != '']
            if 'work' in url and len(url_s) == 2 and str(url_s[1]).isdigit():
                    links.append('http://archiveofourown.org'+link.get('href'))
        except:
            pass
    return links


# In[84]:

def show_full_contents(url):
    #go through adult contents filtering.
    base = bs(urllib2.urlopen(url))
    full_url = url
    for link in base.find_all('a'):
        if 'Proceed' in link.text:
            full_url = url +'?view_adult=true'
    return full_url


# In[85]:

def get_contents(url, opener=opener):
#     get work metadata and contents from the work page.
#     print 'Reading url:', url
    try:
        req = urllib2.Request(url)
        page = bs(opener.open(req))
        contents = str(page.body.text.encode('utf-8')).replace('\n','A')
    except:
#         print 'Unable to read from this url'
        contents = ''
        pass
    return url, contents


# In[86]:

def write_header(outfile):
    f = open(outfile, 'a')
    writer = csv.writer(f, delimiter=',')
    keys = ['Additional_Tags', 'Archive_Warnings', 'Author', 'Bookmarks', 'Category', 'Chapters', 'Characters',             'Comments', 'CompleteDate', 'Fandoms', 'Hits', 'Kudos', 'Language', 'Notes', 'PublishDate', 'Rating',             'Relationship', 'Summary', 'Text', 'Title', 'Words']
    writer.writerow(keys)
    f.close()


# In[87]:

def write_work_content(work_dict,outfile):
    #write work metadata and contents as values of a sorted dictionary.
    f = open(outfile, 'a')
    writer = csv.writer(f, delimiter=',')
    try:
        writer.writerow(OrderedDict(sorted(work_dict.items())).values())
    except:
        pass
    f.close()


# In[88]:

#creates dictionary for information in a single work.
def create_work_dict(url, contents):
#     get work metadata and contents into a dictionary.

#     print 'Getting work information from:', url
    try:
        work = {}

        rating = re.findall('Rating:(.*?)<br />',contents) 
        warning = re.findall('Warnings:(.*?)<br />',contents)
        fandom = re.findall('Fandoms:A          AAA(.*?)AAAA|Fandom:A          AAA(.*?)AAAA',contents) 
        category = re.findall('Category:A          AAA(.*?)AAAA',contents)
        relationship = re.findall('Relationships:(.*?)<br />',contents)
        characters = re.findall('Characters:(.*?)<br />',contents)
        additional = re.findall('Additional Tags:(.*?)<br />',contents) 
        language = re.findall('Language:A      AA(.*?)A      A',contents)
        author = re.findall('A    AA(.*?)AAA',contents)
        text = re.findall('Work Text:(.*?)AAAAAAAA|Chapter TextA(.*?)AAAAA|Chapter TextAAAAAA(.*?)',contents)
        text = [i for i in text[0] if i != ''] if text != [] else []
        title = re.findall('AAAAAAAA      (.*?)A    AA',contents)
        summary = re.findall('>Summary: <p>(.*?)</p>',contents)
        notes = re.findall('Notes:AA(.*?)AA',contents)
        publishdate = re.findall('Published:([0-9]*-[0-9]*-[0-9]*)',contents)
        completedate = re.findall('Completed:([0-9]*-[0-9]*-[0-9]*)',contents)
        words = re.findall('Words:([0-9]*)',contents)
        chapters = re.findall('Chapters:([0-9]*/[0-9]*)',contents)
        comments = re.findall('Comments:([0-9]*)',contents)
        kudos = re.findall('Kudos:([0-9]*)',contents)
        bookmarks = re.findall('Bookmarks:([0-9]*)',contents)
        hits = re.findall('Hits:([0-9]*)',contents)       
        
        work['Rating'] = rating[0] if rating != [] else ''
        work['Archive_Warnings'] = warning[0] if warning != [] else ''
        work['Fandoms'] = [i for i in fandom[0] if i != ''][0] if fandom != [] else ''
        work['Category'] = category[0] if category != [] else ''
        work['Relationship'] = relationship[0] if relationship != [] else '' 
        work['Characters'] = characters[0] if characters != [] else ''
        work['Additional_Tags'] = additional[0] if additional != [] else ''
        work['Language'] = language[0] if language != [] else ''
        work['Author'] = author[0] if author != [] else ''
        work['Text']= text[0] if text != [] else ''
        work['Title']  = title[0] if title != [] else ''
        work['Summary'] = summary[0] if summary != [] else ''
        work['Notes'] = notes[0] if notes != [] else ''
        work['Comments'] = comments[0] if comments != [] else ''
        work['PublishDate'] = publishdate[0] if publishdate != [] else ''
        work['CompleteDate'] = completedate[0] if completedate != [] else ''
        work['Words'] = words[0] if words != [] else ''
        work['Chapters'] = chapters[0] if chapters != [] else ''
        work['Comments'] = comments[0] if comments != [] else ''
        work['Kudos'] = kudos[0] if kudos != [] else ''
        work['Bookmarks'] = bookmarks[0] if bookmarks != [] else ''
        work['Hits'] = hits[0] if hits != [] else ''
    
#     print 'Finished with:', url
    except:
#         print 'Something went wrong.'
        pass
    return work


# In[89]:

def get_chapters_list(url,opener=opener):
    url_full = show_full_contents(url)
    chapters_list = []
    navigate = ''
    
    req = urllib2.Request(url_full)
    page = bs(opener.open(req))
    for link in page.find_all('a'):
        if 'Chapter Index' in link.text and len(link.get('href')) > 1:
            navigate = 'http://archiveofourown.org' + link.get('href')
    
    if navigate != '':
        req2 = urllib2.Request(navigate)
        page2 = bs(opener.open(req2))
        for link in page2.find_all('a'):
            if 'chapters' in link.get('href'):
                chapters_list.append('http://archiveofourown.org' + link.get('href'))
    return chapters_list


# In[90]:

def read_single_work(url):
    url_full = show_full_contents(url)
    u, c = get_contents(url_full)
    work = create_work_dict(u, c)
    write_work_content(work,outfile)


# In[91]:

# get_next_chapter('http://archiveofourown.org/works/3078407?view_adult=true')


# In[92]:

# s = get_contents('http://archiveofourown.org/works/5051548?view_adult=true')


# In[93]:

# d = create_work_dict('u',str(s))


# In[94]:

# d = create_work_dict('http://archiveofourown.org/works/5205566',str(c))


# In[95]:

# c = bs(urllib2.urlopen('http://archiveofourown.org/works/5051548?view_adult=true'))


# In[96]:

# req2 = urllib2.Request('http://archiveofourown.org/works/5051548/navigate')
# page2 = bs(opener.open(req2))
# for link in page2.find_all('a'):
#     if 'Chapter' in link.text:
#         print link.text, link.get('href')


# In[97]:

# ch = get_chapters_list('http://archiveofourown.org/works/5144414/')


# In[ ]:

#main loop
if __name__ == "__main__":

    write_header(outfile)
    start_time = time.clock()
    count = 0

    for i in range(start_page, max_page+1):
        try:
            page = find_page(start, i)
            worklist = find_works(page)
            for w in worklist:
                ch_list = get_chapters_list(w)
                if ch_list != []:
                    read_single_work(w)
                    for ch in ch_list:
                        read_single_work(ch)
                else:
                    read_single_work(w)
                count += 1

            with open('./records', 'a') as g:
                g.write('crawling page:'+str(i))
                g.write('\n')

            # print 'crawling page:', i
        except:
            pass

# print 'Saved %s works from %s pages of tag %s in %s seconds .' %(count, i, 'Sherlock Holmes', str(time.clock() - start_time))        


# In[ ]:




# In[ ]:




# In[ ]:



