import urllib2
from urllib import FancyURLopener
from bs4 import BeautifulSoup
import simplejson as json
import numpy as np
import nltk 
from nltk.corpus import stopwords
from nltk.stem.porter import *
import re 


stemmer = PorterStemmer()
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
         description2 += name2 + " "
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
    json_data[keywords] = extractKeywords(text_preprocessing(json_data[description]))
    print json_data
    return json_data

'''def to_words(content):
    letters_only = re.sub("[^a-zA-Z", " ", content)
    words = letters_only.lower().split()
    stopw = set(stopwords.words("english"))
    meaningful_words = [w for w in words if not w in stops]
    return (" ".join(meaningful_words))'''


def text_preprocessing(description):
    description = re.sub("[^a-zA-Z", " ", description).lower()
    for project in range(len(description)):
        tokens = nltk.word_tokenize(content[project])
        try:
            singles = [stemmer.stem(token) for token in tokens]
        except:
            pass
        singles = ' '.join(singles)
        content[project] = ''.join(singles)
    return content

def extractKeywords(description):
    processed_text = text_preprocessing(description)
    vectorizer = TfidfVectorizer(analyzer='word')
    result = vectorizer.fit_transform('processed_text')

    feature_array = np.array(vectorizer.get_feature_names())
    tfidf_sorting = np.argsort(result.toarray()).flatten()[::-1]

    n = 20

    top_keywords = feature_array[tfidf_sorting][:n]
    print top_keywords
    return top_keywords

extractKeywords('We wanted to embrace the theme of travelling by making a game in which you would be running to catch your plane, dodging usual airport items and people on your way. Due to the extreme lack of  free 3D assets and our lack of expertise with making them, we eventually restricted it to the theme of space, which did open our game to new physics and possibilities.This is a really fun game in which you use your hands, free of any controller, to move obstacles out of your path to the finish line using a LEAP Motion.We used Unity as the main development tool. The LEAP Motion SDK allowed us to implement a pair of virtual hands that would mimic your real hands in the game, using the sensor. Then we made a playing field that would spawn obstacles in waves of increasing speed and complexity, which moves relative to the player, giving the illusion of infinite motion.The main issue was the fact that none of us had used Unity before. The similarities between Java and the C# Unity uses thankfully helped us.\nThe second biggest issue was the act that the newest version of Unity, which we were using, has changed incredibly much of the inheritance relations between components, methods used by objects and the way you interact with them. This made many of the online resources obsolete.We have successfully proven our understanding of object oriented programming by successfully going way beyond our comfort zone (plain Java).For us, this was a great learning experiment of how we can write a program that interacts in a true way with the real world.The game can easily be made to fit any theme : the airport, te beach, mountains etc. The only things standing in the way of this are the prices of good assets but mostly lack of Blender skills to make them on our own.')

