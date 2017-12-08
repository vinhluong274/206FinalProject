import requests
import facebook  #pip install facebook-sdk
import json

access_token = None
if access_token is None:
    access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")


graph = facebook.GraphAPI(access_token)
all_fields = ['message', 'created_time', 'description', 'caption', 'link', 'place', 'status_type']
all_fields = ','.join(all_fields)
posts = graph.get_connections('me','posts', fields = all_fields) 

while True:
	try:
		with open('my_posts2.json','a') as f:
			for post in posts['data']:
				f.write(json.dumps(post)+"\n")
			posts = requests.get(posts['paging']['next']).json()
	except KeyError:
		#ran out of posts
		break