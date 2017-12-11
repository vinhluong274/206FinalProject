import facebook
import requests
import sqlite3
import json
import datetime
import plotly
import plotly.plotly as py
from plotly.graph_objs import *


token = input("\nPlease copy and paste your Facebook Access token from https://developers.facebook.com/tools/explorer\n>  ")
# API Connection Information; Establishes a connection to FB's Graph API
# token="EAACEdEose0cBAB79NtGPEdzBfg5MlYdZBpkZCiIfwYgJyF9ChLM2Lcc0Wj7uLwErk8pIZBg579yH38pbeF1wjsqGr991UxGUjEFN7TZCU1Rtqn6CGJ1HUKC2EAxCP2R518cAgpP2QFYDJ3rDajrVopOYkK5SA0L09wdzWkA7KZBRRAlhoDjFTvnxFmxUpK8gZD"
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
count = 0
for post in postsdata["posts"]:
    if count < 101:
        if "message" in post:
            count+=1
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
        elif post == {}:
            print("User does not have up to 100 posts") #User does not have up to 100 posts.
            continue
        else:
            continue #some posts are "Stories"-- I did not count these as user posts. They will return Key Errors because they have no "message"/status update

conn.commit()
print("Finished writing to database.")


#VISUALIZATION IF DATA
#establishes credentials for connection to plotly
plotly.tools.set_credentials_file(username='vinhnillarice', api_key='if3NnzKFAELnEqDijVJ0')

#We need to access the database and retrieve frequency of activity for each day of the week
#This will make a list of tuples with the respective weekday for each occurence of it in the DB
activity = cur.execute("SELECT weekday FROM FbPosts").fetchall()
monday = activity.count(("Monday",))#storing the count of times each day occurs
tuesday = activity.count(("Tuesday",))
wednesday = activity.count(("Wednesday",))
thursday = activity.count(("Thursday",))
friday = activity.count(("Friday",))
saturday = activity.count(("Saturday",))
sunday = activity.count(("Sunday",))

trace1 = Bar(
    x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"],
    y=[monday, tuesday, wednesday, thursday, friday, saturday, sunday]
)
data = Data([trace1])
py.plot(data, filename = 'facebook-posts-bar-chart')#plot the data publicly online
