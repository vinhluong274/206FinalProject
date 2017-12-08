import requests
import facebook  #pip install facebook-sdk
import json

access_token = "EAACEdEose0cBALVqDDnTEc18J4keJ5MnprZCaCsiPP0nzX3oyZBKRo3v99OKVqGWKJPv2QaRqIm0JIX2GFAHeY9aecIGBjSZCssURrsZA6IxuoHeZCE5ijPZC0UMFp43D2C5ABxNicsTERobfXbGlw19ZBDTUNFSWWjVcVpe420vkt3Huua2W1YZA8y8gweLAooZD"
if access_token is None:
    access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")


graph = facebook.GraphAPI(access_token)
posts = graph.get_connections('me','posts')

while True:
	try:
		with open('my_posts.json','a') as f:
			for post in posts['data']:
				f.write(json.dumps(post)+"\n")
			posts = requests.get(posts['paging']['next']).json()
	except KeyError:
		#ran out of posts
		break
