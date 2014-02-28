# Webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import webapp2
import json

# Template
import os
from google.appengine.ext.webapp import template

# Music Database
import sys
sys.path.append('./music')
import musicdb
import database

# Debug
import time

def is_mobile(useragent, force):
    if force: return True
    if useragent.find('iPhone')>-1: return True
    if useragent.find('iPod')>-1: return True
    if useragent.find('iPad')>-1: return True
    if useragent.find('Android')>-1: return True
    return False

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'test' : 0,
            }

        if is_mobile(self.request.user_agent, False): path = os.path.join(os.path.dirname(__file__), 'main_mobile.html')
        else: path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path, template_values))

class GetHTMLHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(is_mobile(self.request.user_agent, True))

class GetJSONHandler(webapp2.RequestHandler):
    def get(self):
        #queryfumen = database.MusicData.gql("WHERE difficulty>=11")
        queryfumen = database.MusicData.all()
        #self.response.out.write('[')
        #listfumen = queryfumen.fetch(500)

        musiclist = {}

        for fumen in queryfumen:
            musiclist[fumen.name] = {
                'version' : fumen.version,
                # 'name' : fumen.name,
                'spn_level' : fumen.spn_level,
                'sph_level' : fumen.sph_level,
                'spa_level' : fumen.spa_level,
                'dpn_level' : fumen.dpn_level,
                'dph_level' : fumen.dph_level,
                'dpa_level' : fumen.dpa_level,
                'spn_notes' : fumen.spn_notes,
                'sph_notes' : fumen.sph_notes,
                'spa_notes' : fumen.spa_notes,
                'dpn_notes' : fumen.dpn_notes,
                'dph_notes' : fumen.dph_notes,
                'dpa_notes' : fumen.dpa_notes,
            }
        self.response.out.write(json.dumps(musiclist, separators=(',',':') ,ensure_ascii=False))

class AddDataHandler(webapp2.RequestHandler):
    def post(self):
        data = musicdb.MusicDatabase()
        self.response.out.write(data.refresh_data(self.request.get('music_json')))

class DebugHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('m')=='delete':
            data = musicdb.MusicDatabase()
            data.deleteAllFumenData()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/get-html', GetHTMLHandler),
    ('/get-json', GetJSONHandler),
    ('/add', AddDataHandler),
    ('/debug', DebugHandler)
    ], debug=True)