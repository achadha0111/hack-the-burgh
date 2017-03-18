from urllib import FancyURLopener
import json
from bs4 import SoupStrainer, BeautifulSoup
import time


#Class to provide custom user header to prevent 
#blocking by Google\'s bot watchers. 
class MyOpener(FancyURLopener):
  version = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
openurl = MyOpener().open

data = [] # Empty list used later to create json

page_number = 0
base_url = 'https://devpost.com'


#iterate through 8 pages
for i in range(1,5):

  page_number = i
  append_url = '/hackathons?challenge_type=all&page='+str(page_number)+'&search=United+Kingdom&sort_by=Recently+Added&utf8=%E2%9C%93'
  page_url = base_url+append_url
  page = BeautifulSoup(openurl(page_url).read(), "lxml",parse_only=SoupStrainer('div',{'class':'content-section'}))

  #iterate through hackathons in the page
  for hackathon in page.find_all('a',{'class':'clearfix'}):
    time.sleep(1)
    hackathon_name = hackathon.find('h2',{'class':'title'}).text.strip()
    print hackathon_name
    dodgy_url = hackathon['href'][8:]
    hackathon_url = 'https://'+dodgy_url[:(dodgy_url.index('/'))]
    hackathonSubs_page = BeautifulSoup(openurl(hackathon_url+'/submissions').read(),"lxml",parse_only=SoupStrainer('div',id='submission-gallery'))
    submission_pageNumbers = hackathonSubs_page.find('ul',{'class':'pagination'})

    #if the submissions page does not have a set of page numbers
    if not submission_pageNumbers:
      for project in hackathonSubs_page.find_all('a',{'class':'block-wrapper-link fade link-to-software'}):
        #a dictionary to store information for each project
        info = {}
        
        info['hackathon_name'] = hackathon_name
        project_page=BeautifulSoup(openurl(project['href']).read(),"lxml")
        info['project_name'] = project_page.find('h1',id='app-title').text.strip()
        info['project_url'] = project['href']
        project_page=BeautifulSoup(openurl(project['href']).read(),"lxml",parse_only=SoupStrainer('div',{'class':'large-9 columns'}))
        project_description = project_page.find('div',id='')
        info['project_description']=project_description.text.strip()
        project_tags = project_page.find_all('span',{'class':'cp-tag recognized-tag'})
        project_tags_list=[]
        for tag in project_tags:
          project_tags_list.append(tag.text.strip())
        info['project_tags'] = project_tags_list
        data.append(info)
    else:
      for submissions_page in submission_pageNumbers.find_all('a',href=True):
        if submissions_page['href'] != '#':
          hackathon_submission_url = hackathon_url + submissions_page['href']
          
          hackathonSubs_page = BeautifulSoup(openurl(hackathon_submission_url).read(),"lxml",parse_only=SoupStrainer('div',id='submission-gallery'))
          for project in hackathonSubs_page.find_all('a',{'class':'block-wrapper-link fade link-to-software'}):
            #a dictionary to store information for each project
            info = {}

            info['hackathon_name'] = hackathon_name
            project_page=BeautifulSoup(openurl(project['href']).read(),"lxml")
            info['project_name'] = project_page.find('h1',id='app-title').text.strip()
            info['project_url'] = project['href']
            project_page=BeautifulSoup(openurl(project['href']).read(),"lxml",parse_only=SoupStrainer('div',{'class':'large-9 columns'}))
            project_description = project_page.find('div',id='')
            info['project_description']=project_description.text.strip()
            project_tags = project_page.find_all('span',{'class':'cp-tag recognized-tag'})
            project_tags_list=[]
            for tag in project_tags:
              project_tags_list.append(tag.text.strip())
            info['project_tags'] = project_tags_list
            data.append(info)

with open('projects.json', 'w') as outfile:
  json.dump(data,outfile,sort_keys = True, indent = 2)


  