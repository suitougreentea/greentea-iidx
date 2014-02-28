import csv
import database
import json

class MusicDatabase:
    version_data = {
    '1st style':1, 'substream':2, '2nd style':3, '3rd style':4, '4th style':5,
    '5th style':6, '6th style':7, '7th style':8, '8th style':9, '9th style':10,
    '10th style':11, 'IIDX RED':12, 'HAPPYSKY':13, 'DistorteD':14, 'GOLD':15,
    'DJ TROOPERS':16, 'EMPRESS':17, 'SIRIUS':18, 'Resort Anthem':19, 'Lincle':20,
    'tricoro':21, 'SPADA':22,
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

    def deleteAllFumenData(self):
        for fumen in database.FumenData.all():
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