import facebook
import requests
import sqlite3


token = "EAACEdEose0cBAHFvkitBDoI9h6Ij8UnDyw06AOTduOPoyfuYLSn1PhWty7CkAktMChb0mdZCXZAFvA47hYQZBFXNYnEscCOfqlh20VheNrVzNjWZBwNq4UvdTZBwaG8JDwrl9ZAKpn4VWlv4JZCxSZCv2ToSja0U1YyrW8kF1w7ZBZAb8bVFZBvQ5wGo3SP4XMowsAZD"
graph = facebook.GraphAPI(token)

friends = graph.get_connections(id="me", connection_name="posts")

print(friends)
for friend in friends:
    print(friend)
