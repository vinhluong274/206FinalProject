import facebook
import requests
import sqlite3


token = "EAACEdEose0cBAJ7K8VE8dINY3uUwjoquo04Q1IBS4AYDnFRDhdMWfViAX0uf2QCE0EcUxOyvhVjoraf2tZAgwsjKtvnKZBwlTXlWwxFb8r3MkvVxhKlAnMZCoIF0ZBwBNL10lyif7DQXwACJoWrRrk8q1xSfQV7NsAdNqnvIVaZCm3M5hvWXRx4lmDpnZAaP0ZD"
graph = facebook.GraphAPI(token, version='2.1')

friends = graph.get_connections(id="me", connection_name="friends")

cachefile = open("FB-Cache.txt", "w")
string = str(friends)
cachefile.write(string)

names = []

for item in friends["data"]:
    print(item["id"])
