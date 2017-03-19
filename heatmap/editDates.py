from urllib import FancyURLopener
import json
from bs4 import SoupStrainer, BeautifulSoup
import time

with open('../scrapers/hackathonInfo.json') as data_file:    
    hackathons = json.load(data_file)

for hackathon in hackathons:
  date = hackathon["hackathon_date"]
  if date != "null":
   year = hackathon["hackathon_date"][-4:]
   print year
   hackathon["year"] = year
  
with open('hackathonAndYears.json', 'w') as outfile:
  json.dump(hackathons,outfile,sort_keys = True, indent = 2)