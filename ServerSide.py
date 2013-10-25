#!/usr/bin/env python
import webapp2
import json
import logging

from httplib2 import Http
from urllib import urlencode

CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'https://<appengine_instance>.appspot.com/'
#REDIRECT_URI = 'http://localhost:14084/'

AUTH_URL = 	"https://accounts.google.com/o/oauth2/auth?client_id=" + CLIENT_ID +"&response_type=code&redirect_uri=" + REDIRECT_URI +"&state=mysecurestate&scope=https://www.googleapis.com/auth/userinfo.email%20https://www.googleapis.com/auth/plus.me%20https://www.googleapis.com/auth/drive"

class MainHandler(webapp2.RequestHandler):
  def get(self):
    code = self.request.get('code', None)
    if code is None:
  	  self.redirect(AUTH_URL)
    else:
  	  h = Http()
  	  data = dict(code=code, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,grant_type="authorization_code")
  	  resp, access_content = h.request('https://accounts.google.com/o/oauth2/token', 'POST', urlencode(data))
  	  
  	  #this call gets us email info. however, decrypting the ID_TOKEN would have done it too
  	  userinfo_endpoint = 'https://www.googleapis.com/oauth2/v3/userinfo' 
  	  data = json.loads(access_content)
  	  headers = {'Authorization': 'Bearer ' + data['access_token']}
  	  resp, profile_content = h.request(userinfo_endpoint, 'GET', headers=headers)

  	  drive_endpoint = 'https://www.googleapis.com/drive/v2/files'
  	  resp, drive_content = h.request(drive_endpoint, 'GET', headers=headers)
   	  
  	  self.response.out.write(access_content+'<br><br>'+profile_content+'<br><br>')

  	  driveFiles = json.loads(drive_content)
  	  for file in driveFiles['items']:
  	  	self.response.out.write('<p><img src=\"' + file['iconLink'] + '\"> '+ file['title'] + '</p>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
