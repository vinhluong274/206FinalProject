import requests
import sqlite3
import json
import datetime
import time
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

#Dark Sky API Key
accessKey = "9f0f97798ec11a765d3ffcb52c72aef8"
try:
    city = input("Please enter in a name of a city: ")
    results = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+ city)
    jsonResults = results.json()
    coordinates = jsonResults['results'][0]['geometry']['location']
    lat = str(coordinates["lat"])
    lng =str(coordinates["lng"])
except:
    print("Please enter a valid city name!")
    exit()


CACHE_FNAME = 'darksky-cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE = {}

def getWeatherData(lat, lon):
    if float(lat) and float(lon) in CACHE.values():
        print("Data was already in the cache")
        return CACHE
    else:
        print("Making a request for new data...\n")
        fw = open(CACHE_FNAME, "w")
        fw.write('{"latitude": %s, "longitude": %s, "weather": [' % (lat, lon))
        t = int(time.time())
        for i in range(99):
            url = "https://api.darksky.net/forecast/" + accessKey + "/" + lat + "," + lon + "," + str(t)
            data = requests.get(url).json()
            CACHE_DICTION = data['daily']['data'][0]
            dumped_json = json.dumps(CACHE_DICTION)
            fw.write(dumped_json + ",")
            t -= 86400 #one day's time in UNIX time.
        url = "https://api.darksky.net/forecast/" + accessKey + "/" + lat + "," + lon + "," + str(t)
        data = requests.get(url).json()
        CACHE_DICTION = data['daily']['data'][0]
        dumped_json = json.dumps(CACHE_DICTION)
        fw.write(dumped_json)
        fw.write("]}")
        fw.close()
        f = open(CACHE_FNAME, "r")
        jsonstring = f.read()
        diction = json.loads(jsonstring)
        return diction


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
    date = time.strftime("%d %b %Y", time.localtime(unixtime))
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

conn.commit()

#Get data from Database
icons = cur.execute("SELECT icon FROM Weather").fetchall()

clearDay = icons.count(('clear-day',))
rain = icons.count(('rain',))
partlyCloudy = icons.count(('partly-cloudy-day',)) + icons.count(('partly-cloudy-night',))
fog = icons.count(('fog',))
wind = icons.count(('wind',))
snow = icons.count(('snow',))


#PYPLOT Info and Graphing the DATA
print("Graphing data and redirecting browser...")
plotly.tools.set_credentials_file(username='vinhnillarice', api_key='if3NnzKFAELnEqDijVJ0')
trace1 = Bar(
    x=["Sunny", "Rain", "Partly Cloudy", "Fog", "Wind","Snow"],
    y=[clearDay, rain, partlyCloudy, fog, wind, snow]
)
data = Data([trace1])
py.plot(data, filename = 'weather-chart')#plot the data publicly online
