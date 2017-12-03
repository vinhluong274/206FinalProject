from instagram.client import InstagramAPI
import httplib2
import simplejson
import six
import requests
import json


access_token = "19052523.4cb61e5.6bc76d6d06a54729a610aae7639faa50"
client_secret = "4cb61e5020ba43cda4754f9b1a0384cc"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)
recent_media = api.user_recent_media(user_id="userid", count=10)
