import csv
import database
import json

class MusicDatabase:
    version_data = {
    '1st style':0, 'substream':1, '2nd style':2, '3rd style':3, '4th style':4,
    '5th style':5, '6th style':6, '7th style':7, '8th style':8, '9th style':9,
    '10th style':10, 'IIDX RED':11, 'HAPPYSKY':12, 'DistorteD':13, 'GOLD':14,
    'DJ TROOPERS':15, 'EMPRESS':16, 'SIRIUS':17, 'Resort Anthem':18, 'Lincle':19,
    'tricoro':20, 'SPADA':21,
    }

    def refresh_data(self, music_json_str):
        data = json.loads(music_json_str)
        # fp = open('music/music_data.json', 'r')
        # data = json.load(fp)
        for key in data:
            version = self.version_data[data[key]['version']]
            name = data[key]['name']
            dspn = self.parseDifficulty(data[key]['spn_level'])
            dsph = self.parseDifficulty(data[key]['sph_level'])
            dspa = self.parseDifficulty(data[key]['spa_level'])
            ddpn = self.parseDifficulty(data[key]['dpn_level'])
            ddph = self.parseDifficulty(data[key]['dph_level'])
            ddpa = self.parseDifficulty(data[key]['dpa_level'])
            nspn = self.parseDifficulty(data[key]['spn_notes'])
            nsph = self.parseDifficulty(data[key]['sph_notes'])
            nspa = self.parseDifficulty(data[key]['spa_notes'])
            ndpn = self.parseDifficulty(data[key]['dpn_notes'])
            ndph = self.parseDifficulty(data[key]['dph_notes'])
            ndpa = self.parseDifficulty(data[key]['dpa_notes'])

            self.checkAndUpdateMusic(version, name, dspn, dsph, dspa, ddpn, ddph, ddpa, nspn, nsph, nspa, ndpn, ndph, ndpa)

    def deleteAllMusicData(self):
        for fumen in database.MusicData.all():
            # self.deleteFumenScoreData(fumen)
            fumen.delete()

    def deleteFumenScoreData(self, fumen):
        for score in database.ScoreData.gql("WHERE fumen=:fumen", fumen=fumen):
            score.delete()

    def deleteAllScoreData(self):
        for score in database.ScoreData.all():
            score.delete()

    def parseDifficulty(self, numberstr):
        if numberstr == '-' : return -1
        else : return int(numberstr)

    def checkAndUpdateMusic(self, version, name, dspn, dsph, dspa, ddpn, ddph, ddpa, nspn, nsph, nspa, ndpn, ndph, ndpa):
        # if dspn != -1 : self.checkAndUpdateFumen(version, name, 1, dspn, nspn)
        # if dsph != -1 : self.checkAndUpdateFumen(version, name, 2, dsph, nsph)
        # if dspa != -1 : self.checkAndUpdateFumen(version, name, 3, dspa, nspa)
        # if ddpn != -1 : self.checkAndUpdateFumen(version, name, 5, ddpn, ndpn)
        # if ddph != -1 : self.checkAndUpdateFumen(version, name, 6, ddph, ndph)
        # if ddpa != -1 : self.checkAndUpdateFumen(version, name, 7, ddpa, ndpa)

        database.MusicData(
            version = version,
            name = name,
            spn_level = dspn,
            sph_level = dsph,
            spa_level = dspa,
            dpn_level = ddpn,
            dph_level = ddph,
            dpa_level = ddpa,
            spn_notes = nspn,
            sph_notes = nsph,
            spa_notes = nspa,
            dpn_notes = ndpn,
            dph_notes = ndph,
            dpa_notes = ndpa,
            ).put()

    # def registerNewMusic(self, version, name, genre, artist, minbpm, maxbpm, dspn, dsph, dspa, dspb, ddpn, ddph, ddpa, ddpb, nspn, nsph, nspa, nspb, ndpn, ndph, ndpa, ndpb):
    #     music = database.MusicData(version=version, name=name, genre=genre, artist=artist, minbpm=minbpm, maxbpm=maxbpm).put()
    #     if dspn != -1 : self.registerNewFumen(music, 1, dspn, nspn)
    #     if dsph != -1 : self.registerNewFumen(music, 2, dsph, nsph)
    #     if dspa != -1 : self.registerNewFumen(music, 3, dspa, nspa)
    #     if dspb != -1 : self.registerNewFumen(music, 4, dspb, nspb)
    #     if ddpn != -1 : self.registerNewFumen(music, 5, ddpn, ndpn)
    #     if ddph != -1 : self.registerNewFumen(music, 6, ddph, ndph)
    #     if ddpa != -1 : self.registerNewFumen(music, 7, ddpa, ndpa)
    #     if ddpb != -1 : self.registerNewFumen(music, 8, ddpb, ndpb)

    def checkAndUpdateFumen(self, version, name, difficultytype, difficulty, notes):
        queryfumen = database.FumenData.gql("WHERE name=:name and difficultytype=:difficultytype", name=name, difficultytype=difficultytype)
        if queryfumen.count(1) == 0:
            self.registerNewFumen(version, name, difficultytype, difficulty, notes)
        # else:
        #     fumen = queryfumen.get()
        #     if fumen.difficulty != difficulty :
        #         fumen.difficulty = difficulty
        #         fumen.put()
        #     if fumen.notes != notes :
        #         fumen.notes = notes
        #         fumen.put()

    def registerNewFumen(self, version, name, difficultytype, difficulty, notes):
        database.FumenData(version=version, name=name, difficultytype=difficultytype, difficulty=difficulty, notes=notes).put()

    def refresh_score(self, id, json_str):
        data = json.loads(json_str)
        for fumen in data:
            self.register_score(id, fumen["name"], fumen["type"], 0, fumen["score"], 0)

    def register_score(self, id, name, type, lamp, score, bp):
        queryscore = database.ScoreData.gql("WHERE id=:id and name=:name", id=id, name=name)
        if queryscore.count(1) == 0:
            database.ScoreData(
                id = id,
                name = name,
                type = type,
                lamp = lamp,
                score = score,
                bp = bp
                ).put()
        else:
            fumen = queryscore.get()
            fumen.lamp = lamp
            fumen.score = score
            fumen.bp = bp
            fumen.put()