import requests
import facebook  #pip install facebook-sdk
import json

#To set up your account acces go to: https://developers.facebook.com/

print("Welcome")
access_token = None
if access_token is None:
    access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")

graph = facebook.GraphAPI(access_token)
profile = graph.get_object('me', fields = 'name,location') #fields is an optional key word argument
# profile = graph.get_object('me', fields = 'name,location{location}') #fields is an optional key word argument
print(json.dumps(profile, indent = 4))
