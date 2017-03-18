import urllib2
from urllib import FancyURLopener
from bs4 import BeautifulSoup
import simplejson as json
class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
openurl = MyOpener().open

class ProjectData:
	#Constructor
    def __init__(self,url, name, hackathon, description, tags, likes):
        self.url = url
        self.name = name
        self.hackathon = hackathon
        self.description = description
        self.tags = tags
        self.likes = likes
	#Pretty Printer
    def __repr__(self):
        return '"name": "%s", "hackathon": "%s", "description": "%s", "tags": "%s", "likes": "%d"' % (self.name, self.hackathon, self.description, self.tags, self.likes)

def scrapeProject(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page,'html.parser')


    #name
    name2 = soup.find('h1',{'id':'app-title'}).text.strip()

    #hackathon
    hackathon2 = soup.find('div',{'class':'software-list-content'}).text.strip()

    #description
    text = soup.find(id="gallery").next_sibling.next_sibling
    paragraphs = text.find_all('p')
    description2 = ''
    for paragraph in paragraphs:
         description2 += paragraph.text.strip()

    #tags
    tags2 = []
    t = soup.find_all('span', {'class':'cp-tag'})
    for x in t:
    	 tags2.append(x.text.strip())


    #likes
    likes2 = soup.find('span', {'class':'like-counts'})
    likes2 = likes2.text.strip()
    a = likes2.split(' ')
    numberOfLikes2 = int(a[0])
    data = ProjectData(url,name2,hackathon2,description2,tags2,numberOfLikes2)
    json_data = json.dumps(data, indent=4, default=lambda o: o.__dict__)
    return json_data
