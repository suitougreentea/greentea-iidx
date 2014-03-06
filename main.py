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

        if is_mobile(self.request.user_agent, False): path = os.path.join(os.path.dirname(__file__), 'public/main_mobile.html')
        else: path = os.path.join(os.path.dirname(__file__), 'public/main.html')
        self.response.out.write(template.render(path, template_values))

class GetHTMLHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(is_mobile(self.request.user_agent, True))

class GetJSONHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get("user") == "":
            queryfumen = database.MusicData.all()

            musiclist = {}

            for fumen in queryfumen:
                musiclist[fumen.name] = {
                    'version' : fumen.version,
                    # 'name' : fumen.name,
                    'level' : [fumen.spn_level, fumen.sph_level, fumen.spa_level, fumen.dpn_level, fumen.dph_level, fumen.dpa_level],
                    'notes' : [fumen.spn_notes, fumen.sph_notes, fumen.spa_notes, fumen.dpn_notes, fumen.dph_notes, fumen.dpa_notes],
                }
            self.response.out.write(json.dumps(musiclist, separators=(',',':') ,ensure_ascii=False))
        if self.request.get("user") == "test":
            queryscore = database.ScoreData.gql("WHERE id=:id", id=1)

            scorelist = {}

            for score in queryscore:
                scorelist[score.name+"-"+str(score.type)] = {
                    "name": score.name,
                    "type": score.type,
                    "lamp": score.lamp,
                    "score": score.score,
                    "bp": score.bp
                }
            self.response.out.write(json.dumps(scorelist, separators=(',',':') ,ensure_ascii=False))

class AddDataHandler(webapp2.RequestHandler):
    def post(self):
        data = musicdb.MusicDatabase()
        self.response.out.write(data.refresh_data(self.request.get('music_json')))

class RegisterHandler(webapp2.RequestHandler):
    def post(self):
        data = musicdb.MusicDatabase()
        data.refresh_score(1,self.request.get('changes_json'))
        self.response.out.write(self.request.get('changes_json'))


class DebugHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('m')=='delete':
            data = musicdb.MusicDatabase()
            data.deleteAllMusicData()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/get-html', GetHTMLHandler),
    ('/get-json', GetJSONHandler),
    ('/add', AddDataHandler),
    ('/register', RegisterHandler),
    ('/debug', DebugHandler)
    ], debug=True)