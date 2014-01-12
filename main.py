# Webapp
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

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'test' : 0,
            }

        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path, template_values))

class GetHTMLHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("<div>abcd</div>")

class GetJSONHandler(webapp2.RequestHandler):
    def get(self):
        queryfumen = database.FumenData.gql("WHERE difficulty=10")
        result = '{\"result\": ['
        for fumen in queryfumen:
            result += json.dumps({
                'name':fumen.music.name, 'genre':fumen.music.genre, 'artist':fumen.music.artist, 'minbpm':fumen.music.minbpm, 'maxbpm':fumen.music.maxbpm, 'difficultytype':fumen.difficultytype, 'difficulty':fumen.difficulty, 'notes':fumen.notes
                },ensure_ascii=False) + ","
        result += ']}'
        self.response.out.write(result)

class DebugHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('m')=='add':
            data = musicdb.MusicDatabase()
            data.load()
            data.refresh()
        elif self.request.get('m')=='delete':
            data = musicdb.MusicDatabase()
            data.deleteAllMusicData()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/get-html', GetHTMLHandler),
    ('/get-json', GetJSONHandler),
    ('/debug', DebugHandler)
    ], debug=True)