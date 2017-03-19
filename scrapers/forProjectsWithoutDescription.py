import urllib2
from urllib import FancyURLopener
from bs4 import BeautifulSoup
import  json
import unicodedata
class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
openurl = MyOpener().open

class ProjectData:
  #Constructor
    def __init__(self,url, name, hackathon, description, tags):
        self.url = url
        self.name = name
        self.hackathon = hackathon
        self.description = description
        self.tags = tags
        #self.likes = likes
  #Pretty Printer
    def __repr__(self):
        return '"name": "%s", "hackathon": "%s", "description": "%s", "tags": "%s", "likes": "%d"' % (self.name, self.hackathon, self.description, self.tags)

def scrapeProject(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page,'html.parser')


    #name
    name2 = soup.find('h1',{'id':'app-title'}).text.strip()

    #hackathon
    hackathon2 = soup.find('div',{'class':'software-list-content'}).text.strip()

    #description
    text = soup.find(id="")
    paragraphs = text.find_all('p')
    description2 = ''
    for paragraph in paragraphs:
         description2 += paragraph.text.strip()

    #tags
    tags2 = []
    t = soup.find_all('span', {'class':'cp-tag'})
    for x in t:
       tags2.append(x.text.strip())

    #print description2

    #likes
    likes2 = soup.find('span', {'class':'like-counts'})
    likes2 = likes2.text.strip()
    a = likes2.split(' ')
    #numberOfLikes2 = int(a[0])
    data = ProjectData(url,name2,hackathon2,description2,tags2)
    #json_data = json.dumps(data, indent=2, default=lambda o: o.__dict__)
    #description2 = unicodedata.normalize('NFKD', description2).encode('ascii','ignore')

    return description2

with open('projects.json','r') as data_file:    
    projects = json.load(data_file)


for project in projects:
  print project["hackathon_name"]
  projectData = scrapeProject(project["project_url"])
  #print projectData
  project["project_description"] = projectData
    
with open('projects.json', 'w') as outfile:
  json.dump(projects,outfile,sort_keys = True, indent = 2)
