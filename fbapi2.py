import requests
import facebook  #pip install facebook-sdk
import json


print("Welcome")
access_token = None
if access_token is None:
    access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")

graph = facebook.GraphAPI(access_token)
user = graph.get_object('me') 
friends = graph.get_connections(user['id'],"friends")
print(json.dumps(friends, indent = 4))
