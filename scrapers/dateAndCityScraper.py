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
for i in range(1,9):

  page_number = i
  append_url = '/hackathons?challenge_type=all&page='+str(page_number)+'&search=United+Kingdom&sort_by=Recently+Added&utf8=%E2%9C%93'
  page_url = base_url+append_url
  page = BeautifulSoup(openurl(page_url).read(), "lxml",parse_only=SoupStrainer('div',{'class':'content-section'}))

  #iterate through hackathons in the page
  for hackathon in page.find_all('a',{'class':'clearfix'}):
    info={}
    time.sleep(1)
    hackathon_name = hackathon.find('h2',{'class':'title'}).text.strip()
    print hackathon_name
    hackathon_location = hackathon.find('p',{'class':'challenge-location'}).text.strip()
    print hackathon_location
    

    if hackathon_location != "Online":
      info["hackathon_name"] = hackathon_name
      info["hackathon_location"] = hackathon_location
      hackathon_date = hackathon.find('span',{'class':'value date-range'}).text.strip()
      print hackathon_date
      info["hackathon_date"] = hackathon_date

    else:
      info["hackathon_name"] = hackathon_name
      info["hackathon_location"] = hackathon_location
      info["hackathon_date"] = "null"

    data.append(info)

with open('hackathonInfo.json', 'w') as outfile:
  json.dump(data,outfile,sort_keys = True, indent = 2)



