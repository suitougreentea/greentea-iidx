from google.appengine.ext import db

class MusicData(db.Model):
    version = db.IntegerProperty()
    name = db.StringProperty()
    genre = db.StringProperty()
    artist = db.StringProperty()
    minbpm = db.IntegerProperty()
    maxbpm = db.IntegerProperty()

class FumenData(db.Model):
    music = db.ReferenceProperty(MusicData, collection_name='fumen')
    difficultytype = db.IntegerProperty()
    difficulty = db.IntegerProperty()
    notes = db.IntegerProperty()

class ScoreData(db.Model):
    id = db.IntegerProperty()
    fumen = db.ReferenceProperty(FumenData, collection_name='userscore')
    lamp = db.IntegerProperty()
    score = db.IntegerProperty()