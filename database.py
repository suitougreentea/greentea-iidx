from google.appengine.ext import db

class FumenData(db.Model):
    version = db.IntegerProperty()
    name = db.StringProperty()
    difficultytype = db.IntegerProperty()
    difficulty = db.IntegerProperty()
    notes = db.IntegerProperty()

class MusicData(db.Model):
    version = db.IntegerProperty()
    name = db.StringProperty()
    spn_level = db.IntegerProperty()
    sph_level = db.IntegerProperty()
    spa_level = db.IntegerProperty()
    dpn_level = db.IntegerProperty()
    dph_level = db.IntegerProperty()
    dpa_level = db.IntegerProperty()
    spn_notes = db.IntegerProperty()
    sph_notes = db.IntegerProperty()
    spa_notes = db.IntegerProperty()
    dpn_notes = db.IntegerProperty()
    dph_notes = db.IntegerProperty()
    dpa_notes = db.IntegerProperty()

class ScoreData(db.Model):
    id = db.IntegerProperty()
    name = db.StringProperty()
    type = db.IntegerProperty()
    lamp = db.IntegerProperty()
    score = db.IntegerProperty()
    bp = db.IntegerProperty()