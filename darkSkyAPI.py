import requests
import sqlite3
import json
import datetime
import time
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

#My Dark Sky API Key; will work as long as no more than 1000 requests are made per day.
accessKey = "9f0f97798ec11a765d3ffcb52c72aef8"
try:
    #this is stores the inputted city and makes a request from the Google Maps Geocoding API
    #it then stores the latitude and longitude of that city into the lat and lng variables
    city = input("Please enter in a name of a city: ")
    results = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+ city)
    jsonResults = results.json()
    coordinates = jsonResults['results'][0]['geometry']['location']
    lat = str(coordinates["lat"])
    lng =str(coordinates["lng"])
except:
    print("Please enter a valid city name!")#if not a valid city name the API will throw an error
    exit()


CACHE_FNAME = 'darksky-cache.json'

try:
    #tries to open the cache file
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE = json.loads(cache_contents)#if its there read it in and dump it
    cache_file.close()
except:
    CACHE = {}#if no file make the cache an empty dictionary

def getWeatherData(lat, lon):
    #if the coordinates are already in the cache, no need to make a new API request
    if float(lat) and float(lon) in CACHE.values():
        print("Data was already in the cache")
        return CACHE
    else:
        #if not, make a request for new data
        print("Making a request for new data...\n")
        fw = open(CACHE_FNAME, "w")#open the cache file
        fw.write('{"latitude": %s, "longitude": %s, "weather": [' % (lat, lon))#writes the new coordinates to the file in JSON format
        t = int(time.time())#must get today's UNIX time because Dark Sky only uses UNIX time.
        for i in range(99):#get 99 days worth of weather data
            url = "https://api.darksky.net/forecast/" + accessKey + "/" + lat + "," + lon + "," + str(t)#requests weather from the specified city's coordinates.
            data = requests.get(url).json()
            CACHE_DICTION = data['daily']['data'][0]
            dumped_json = json.dumps(CACHE_DICTION)
            fw.write(dumped_json + ",")#write a comma to separate the dictionaries
            t -= 86400 #one day's time in UNIX time.
        url = "https://api.darksky.net/forecast/" + accessKey + "/" + lat + "," + lon + "," + str(t) #get one more day
        data = requests.get(url).json()
        CACHE_DICTION = data['daily']['data'][0]
        dumped_json = json.dumps(CACHE_DICTION)
        fw.write(dumped_json)
        fw.write("]}")#don't write a comma, but close the list of dictionaries and dictionary
        fw.close()
        f = open(CACHE_FNAME, "r")
        jsonstring = f.read()
        diction = json.loads(jsonstring)
        return diction#returns json loaded data in the form of a dictionary

#call the function to get data
weatherInfo = getWeatherData(lat, lng)

#WRITE DATA TO DATABASE
print("Writing and accessind data...\n")
conn = sqlite3.connect("darksky-db.sqlite")
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Weather')
cur.execute('''CREATE TABLE "Weather" (
    "post_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    "time" INTEGER,
    "date" DATETIME,
    "icon" TEXT,
    "summary" TEXT
    ) ''')

for day in weatherInfo["weather"]:
    unixtime = day["time"]
    date = time.strftime("%d %b %Y", time.localtime(unixtime))#write the weather in a readable format.
    icon = day["icon"]
    summary = day["summary"]
    tup = (unixtime, date, icon, summary)
    cur.execute('''INSERT INTO Weather (
                    time,
                    date,
                    icon,
                    summary)
                    VALUES (?,?,?,?)
                    ''', tup)#tuple that was created above.

conn.commit()#commit the changes.

#Get data from Database
icons = cur.execute("SELECT icon FROM Weather").fetchall()

clearDay = icons.count(('clear-day',))
rain = icons.count(('rain',))
partlyCloudy = icons.count(('partly-cloudy-day',)) + icons.count(('partly-cloudy-night',)) #these are the same
fog = icons.count(('fog',))
wind = icons.count(('wind',))
snow = icons.count(('snow',))


#PYPLOT Info and Graphing the DATA
print("Graphing data and redirecting browser...")
plotly.tools.set_credentials_file(username='vinhnillarice', api_key='if3NnzKFAELnEqDijVJ0')
trace1 = Bar(
    x=["Sunny", "Rainy", "Partly Cloudy", "Foggy", "Windy","Snowy"],
    y=[clearDay, rain, partlyCloudy, fog, wind, snow]
)
data = Data([trace1])
py.plot(data, filename = 'weather-chart')#plot the data publicly online
