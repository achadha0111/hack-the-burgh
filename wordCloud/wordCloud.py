from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import json
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy as np
import re
import time

start = time.time()

with open('../scrapers/projects_wordcloud.json') as data_file:    
    projects = json.load(data_file)

text=""

#words = ["Challenges","ran","next","Inspiration","Accomplishments","proud","built","make","create","also","event","use","using","learned"]

for project in projects:
  descrp = project["project_description"]
  text+=descrp


  text+=project["project_description"]

img = Image.open("mlh.png")
img = img.resize((2142,917), Image.ANTIALIAS)
hcmask = np.array(img)
image_colors = ImageColorGenerator(hcmask)

wc = WordCloud(background_color="white", max_words=12000, mask=hcmask, stopwords=STOPWORDS)
wc.generate(text)

wc.to_file("edwc.png")
#plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
#plt.figure()
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")

end = time.time() - start
print str(end)+" seconds"
plt.show()



