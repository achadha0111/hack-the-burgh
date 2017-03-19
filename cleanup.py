import json

with open('database.json') as data_file:    
    projects = json.load(data_file)

uniqueProjects = { project['project_name'] : project for project in projects }.values()
print len(uniqueProjects)

