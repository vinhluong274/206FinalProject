import facebook
import requests
import sqlite3
import json


token = "EAACEdEose0cBACI4DNwsiiWGuVhlZATherxJeMvpN0MjXakvdN30aLJcLkf1d5rDUasN2bIe1BFni9AZC5ZALzbNqBzZCcBZCWNizjM7HzVD8OP1k60p9xCfmuUvZA3hP5ijFBoRcO6p75wnB5IZBwaFgutWJcLKpxZAvgeEWuke5YJZCZAbEtLkmb8qtd7IkGFTEZD"
graph = facebook.GraphAPI(token, version='2.1')

CACHE_FNAME = 'postsFB.json' # String for your file. We want the JSON file type, bcause that way, we can easily get the information into a Python dictionary!

def getFbPostsWithCaching(user):
    print("Making a request for new data...\n")
    posts = graph.get_connections(id=user, connection_name="posts")
    for post in posts:
        while True:
            try:
                with open(CACHE_FNAME,'a') as f:
                    for post in posts['data']:
                        f.write(json.dumps(post)+"\n")
                    posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                #ran out of posts
                break
        f.close() # Close the open file



cache_file = open("postsFB.json", 'r') # Try to read the data from the file
cache_contents = cache_file.read()  # If it's there, get it into a string
CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
cache_file.close() # Close the file, we're good, we got the data in a dictionary.
