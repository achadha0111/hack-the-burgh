#simport simplejson as json
import sklearn
from scipy import spatial
from sklearn import metrics
from scipy.spatial import distance
import json
import numpy as np
import pandas as pd

m10=[-100,[]]
m9=[-100,[]]
m8=[-100,[]]
m7=[-100,[]]
m6=[-100,[]]
m5=[-100,[]]
m4=[-100,[]]
m3=[-100,[]]
m2=[-100,[]]
m1=[-100,[]]
def getSimilarity(myVector,projectVector):
    myVector = np.asarray(myVector)
    myVector = myVector.reshape(1,-1)
    projectVector = np.asarray(projectVector)
    projectVector = projectVector.reshape(1,-1)
    dist = distance.euclidean(myVector,projectVector)
    #return 1- spatial.distance.cosine(myVector,projectVector)
    return 1.0/(1+dist)

def getCommonTags(myProject,projcet):
    me = np.asarray(myProject[0]['project_tags'])
    other = np.asarray(projcet['project_tags'])
    return (len(np.intersect1d(me,other))+1)/float((len(me)+ len(other)))
    #return len(np.intersect1d(me,other))

def updateS (x,i):
    if x > m10[0]:
        m10[0] = x
        m10[1] = i
    elif x > m9[0]:
        m9[0] = x
        m9[1] = i
    elif x > m8[0]:
        m8[0] = x
        m8[1] = i
    elif x > m7[0]:
        m7[0] = x
        m7[1] = i
    elif x > m6[0]:
        m6[0] = x
        m6[1] = i
    elif x > m5[0]:
        m5[0] = x
        m5[1] = i
    elif x > m4[0]:
        m4[0] = x
        m4[1] = i
    elif x > m3[0]:
        m3[0] = x
        m3[1] = i
    elif x > m2[0]:
        m2[0] = x
        m2[1] = i
    elif x > m1[0]:
        m1[0] = x
        m1[1] = i

def rank():
    with open('hackathon_database_100dim_unique.json') as data_file:
        projects = json.load(data_file)
    with open('myProject.json') as data_file2:
        myProject = json.load(data_file2)
    #print len(projects[60]['hack_vector'][0])

    #print projects[60]['project_name']
    myVector = myProject[0]['hack_vector']
    #print projects[60]['hack_vector']

    for i in range(len(projects)):
        similarity = getSimilarity(myVector,projects[int(i)]['hack_vector'])
        commonT = getCommonTags(myProject,projects[int(i)])

        similarity *=100
        similarity*= commonT
        updateS(similarity,projects[i])
        #print similarity
    '''
    print m1[0]
    print m1[1]['project_name']
    print "~~~~~~~~~~~~"
    print m2[0]
    print m2[1]['project_name']
    print "~~~~~~~~~~~~"
    print m3[0]
    print m3[1]['project_name']
    print "~~~~~~~~~~~~"
    print m4[0]
    print m4[1]['project_name']
    print "~~~~~~~~~~~~"
    print m5[0]
    print m5[1]['project_name']
    print "~~~~~~~~~~~~"
    print m6[0]
    print m6[1]['project_name']
    print "~~~~~~~~~~~~"
    print m7[0]
    print m7[1]['project_name']
    print "~~~~~~~~~~~~"
    print m8[0]
    print m8[1]['project_name']
    print "~~~~~~~~~~~~"
    print m9[0]
    print m9[1]['project_name']
    print
    print "~~~~~~~~~~~~"
    print m10[0]
    print m10[1]['project_name']
    print "~~~~~~~~~~~~"
    '''
    data=[]

    infoM = {}
    infoM = m1[1]
    infoM["similarity_score"] = m1[0]
    data.append(infoM)

    infoM = {}
    infoM = m2[1]
    infoM["similarity_score"] = m2[0]
    data.append(infoM)

    infoM = {}
    infoM = m3[1]
    infoM["similarity_score"] = m3[0]
    data.append(infoM)

    infoM = {}
    infoM = m4[1]
    infoM["similarity_score"] = m4[0]
    data.append(infoM)

    infoM = {}
    infoM = m5[1]
    infoM["similarity_score"] = m5[0]
    data.append(infoM)

    infoM = {}
    infoM = m6[1]
    infoM["similarity_score"] = m6[0]
    data.append(infoM)

    infoM = {}
    infoM = m7[1]
    infoM["similarity_score"] = m7[0]
    data.append(infoM)

    infoM = {}
    infoM = m8[1]
    infoM["similarity_score"] = m8[0]
    data.append(infoM)

    infoM = {}
    infoM = m9[1]
    infoM["similarity_score"] = m9[0]
    data.append(infoM)

    infoM = {}
    infoM = m10[1]
    infoM["similarity_score"] = m10[0]
    data.append(infoM)

    with open ('similarity_results.json','w') as outfile:
        json.dump(data,outfile,sort_keys=True,indent=2)
    print ("Write success")
