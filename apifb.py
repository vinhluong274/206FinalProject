import facebook
import requests
import sqlite3
import json
import datetime
import plotly
import plotly.plotly as py
from plotly.graph_objs import *


#API Connection Information; Establishes a connection to FB's Graph API
token="EAACEdEose0cBAKBajheFgdZArN1LKbVZCMVCkFevJZAzXGbkk3ayesAslHUF0Xh6MOVZBz0ngzNMsDD9vZBhENaKtuvkiPNuaq5bQtmOqOZB67tV3nbZBmZAuH7Ky1QkcEI0Rv8AtzjxRudzrjmBdVKz2m4hVjGLSk1DXvtnItu6A8bhAt4ohagc5Omw3iuvWh0ZD"
graph = facebook.GraphAPI(token, version="2.1")
CACHE_FNAME = "facebook-cache.json" #Cache filename to store requested data from FB API


#DEFINE A FUNCTION TO GET USER POSTS FROM FB
#accepts no arguments and will cache all user posts
def getFbPostsWithCaching():
    print("Making a request for new data...\n")
    posts = graph.get_connections(id="me", connection_name="posts")
    for post in posts:
        while True:
            try:
                with open(CACHE_FNAME,'a') as f:
                    #this will write each post to a new line in the cache file
                    for post in posts['data']:
                        f.write(json.dumps(post)+"\n")
                    #due to Pagination, we have to request the next page of posts
                    posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                #ran out of posts
                break
        f.close() # Close the open file

    #Now that we got the data in the cache, we need to extract 100 posts:
    count = 0
    cache_file = open(CACHE_FNAME, 'r')
    while count <= 100: #only gets 100 posts
        diction = cache_file.readline() #reads line by line since each post is a separate dictionary
        if "message" in diction: #only gets posts with text, "Life Events" for example contains no text
            DBPosts.append(json.loads(diction)) #loads the line's string to dictionary and appends to list
            count += 1
    cache_file.close() # Close the file we got the data needed


#Tries to open cache file to extract data, if none calls function to get and cache data.
try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    count = 0 #if it's there, we only want 100 posts
    DBPosts = [] #this will be the list of dictionaries that will store 100 fb posts
    while count <= 100: #only gets 100 posts
        diction = cache_file.readline() #reads line by line since each post is a separate dictionary
        if "message" in diction: #only gets posts with text, "Life Events" for example contains no text
            DBPosts.append(json.loads(diction)) #loads the line's string to dictionary and appends to list
            count += 1
    cache_file.close() # Close the file we got the data needed
    print("Data was in the cache. Extracted 100 posts for use.")
except ValueError: #in the event two or more dictionaries are loaded
    print("Decoding JSON Failed")
    exit()
except: #in the event it is an empty/nonexistent file.
    DBPosts = []
    getFbPostsWithCaching() #calls the function to get new data


#STORE 100 POSTS AND DATA INTO DATABASE:
#Establish a connection to the sqlite3
conn = sqlite3.connect("facebook-posts.sqlite")
cur = conn.cursor()

#Create a table to Store user posts and data:
print("Creating Database Table...")
cur.execute('DROP TABLE IF EXISTS FbPosts')
cur.execute('''CREATE TABLE "FbPosts" (
    "post_id_str" TEXT PRIMARY KEY NOT NULL UNIQUE,
    "status" TEXT,
    "date_posted" DATE,
    "time_posted" TIME,
    "weekday" TEXT
    ) ''')

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"]
print("Writing to database...")
for post in DBPosts:
    status = post["message"]
    post_id_str = post["id"]
    date = post['created_time'][0:10]
    time = post["created_time"][11:19]
    dates = date.split("-")
    year = int(dates[0])
    month = int(dates[1])
    day = int(dates[2])
    weekday = weekdays[datetime.datetime(year, month, day).weekday()]
    tup = (post_id_str, status, date, time, weekday)

    cur.execute('''INSERT OR IGNORE INTO FbPosts (
                post_id_str,
                status,
                date_posted,
                time_posted,
                weekday)
                VALUES (?,?,?,?,?)
                ''', tup)#tuple that was created above.

conn.commit()
print("Finished writing to database.")


#VISUALIZATION IF DATA
plotly.tools.set_credentials_file(username='vinhnillarice', api_key='if3NnzKFAELnEqDijVJ0')

trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = Data([trace0, trace1])
py.plot(data, filename = 'basic-line')
