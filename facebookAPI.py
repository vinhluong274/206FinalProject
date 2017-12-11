import facebook
import requests
import sqlite3
import json
import datetime
import plotly
import plotly.plotly as py
from plotly.graph_objs import *


# token = input("\nPlease copy and paste your Facebook Access token from https://developers.facebook.com/tools/explorer\n>  ")
#API Connection Information; Establishes a connection to FB's Graph API
token="EAACEdEose0cBAO7XrKcYNbgOFoZAkcJZC3un4b9ENlwHDhitVFWJrkRCZCazvlm5ituhqoY4W5Mvu0b4z9OJFZAenEuo2jQuEiokWiZC8rZBtVWQD3WzFYidCuy9GFDv2eqkQaoevWjt0TbpiOiZBig2oY51M1yzJZCUSxQQlWBlfsr1uxNPTKSlcuFuXfnMU00ZD"
graph = facebook.GraphAPI(token)
CACHE_FNAME = "facebook-cache.json" #Cache filename to store requested data from FB API

try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
    cache_file.close() # Close the file, we're good, we got the data in a dictionary.
except:
    CACHE_DICTION = {}

CACHE_DICTION = CACHE_DICTION

nameURL = "https://graph.facebook.com/v2.11/me?access_token=" + token
nameDict = requests.get(nameURL).json()
User = json.dumps(nameDict)
user_id = nameDict["id"]
user_id_int = int(user_id)
user_id_str = str(user_id)

#DEFINE A FUNCTION TO GET USER POSTS FROM FB
#accepts no arguments and will cache all user posts
def getFbPostsWithCaching(cache):
    if user_id_int in cache.values():
        print("Data was in the cache")
        return cache
    else:
        print("Making a request for new data...\n")
        posts = graph.get_connections(id="me", connection_name="posts")
        f = open(CACHE_FNAME, "w")
        f.write('{"user_id":' + user_id_str + ',"posts": [')
        for post in posts:
            while True:
                try:
                    #this will write each post to a new line in the cache file
                    for post in posts['data']:
                        f.write(json.dumps(post) + ",")
                    #due to Pagination, we have to request the next page of posts
                    posts = requests.get(posts['paging']['next']).json()
                except KeyError:
                    #ran out of posts
                    break
        empty = "{}"
        f.write(empty + "]}")
        f.close() # Close the open file
        newCache = open(CACHE_FNAME, "r")
        c = json.loads(newCache.read())
        return c

postsdata = getFbPostsWithCaching(CACHE_DICTION)
print(type(postsdata))
