import csv
import database

class MusicDatabase:
    def load(self):
        self.tsv = csv.reader(file(r"music/music.tsv"), delimiter = '\t')

    def refresh(self):
        for row in self.tsv:
            if self.tsv.line_num==1 : continue

            # Parse data
            bpm = row[4].split('-')
            minbpm = None
            maxbpm = None
            if len(bpm) == 1 :
                minbpm = int(bpm[0])
            else :
                minbpm = int(bpm[0])
                maxbpm = int(bpm[1])

            version = int(row[0])
            name = row[1].decode('utf-8')
            genre = row[2].decode('utf-8')
            artist = row[3].decode('utf-8')
            dspn = self.parseDifficulty(row[5])
            dsph = self.parseDifficulty(row[6])
            dspa = self.parseDifficulty(row[7])
            dspb = self.parseDifficulty(row[8])
            ddpn = self.parseDifficulty(row[9])
            ddph = self.parseDifficulty(row[10])
            ddpa = self.parseDifficulty(row[11])
            ddpb = self.parseDifficulty(row[12])
            nspn = self.parseDifficulty(row[13])
            nsph = self.parseDifficulty(row[14])
            nspa = self.parseDifficulty(row[15])
            nspb = self.parseDifficulty(row[16])
            ndpn = self.parseDifficulty(row[17])
            ndph = self.parseDifficulty(row[18])
            ndpa = self.parseDifficulty(row[19])
            ndpb = self.parseDifficulty(row[20])

            self.checkAndUpdateMusic(version, name, genre, artist, minbpm, maxbpm, dspn, dsph, dspa, dspb, ddpn, ddph, ddpa, ddpb, nspn, nsph, nspa, nspb, ndpn, ndph, ndpa, ndpb)

    def deleteAllMusicData(self):
        for music in database.MusicData.all():
            self.deleteMusicFumenData(music)
            music.delete()

    def deleteMusicFumenData(self, music):
        for fumen in database.FumenData.gql("WHERE music=:music", music=music):
            self.deleteFumenScoreData(fumen)
            fumen.delete()

    def deleteFumenScoreData(self, fumen):
        for score in database.ScoreData.gql("WHERE fumen=:fumen", fumen=fumen):
            score.delete()

    def deleteAllFumenData(self):
        for fumen in database.FumenData.all():
            self.deleteFumenScoreData(fumen)
            fumen.delete()

    def deleteAllScoreData(self):
        for score in database.ScoreData.all():
            score.delete()

    def parseDifficulty(self, numberstr):
        if numberstr == '-' : return -1
        else : return int(numberstr)

    def checkAndUpdateMusic(self, version, name, genre, artist, minbpm, maxbpm, dspn, dsph, dspa, dspb, ddpn, ddph, ddpa, ddpb, nspn, nsph, nspa, nspb, ndpn, ndph, ndpa, ndpb):
        querymusic = database.MusicData.gql("WHERE name=:name", name=name)
        if querymusic.count(1) == 0:
            self.registerNewMusic(version, name, genre, artist, minbpm, maxbpm, dspn, dsph, dspa, dspb, ddpn, ddph, ddpa, ddpb, nspn, nsph, nspa, nspb, ndpn, ndph, ndpa, ndpb)
        else:
            music = querymusic.get()
            if music.genre != genre :
                music.genre = genre
                music.put()
            if music.artist != artist :
                music.artist = artist
                music.put()
            if music.minbpm != minbpm :
                music.minbpm = minbpm
                music.put()
            if music.maxbpm != maxbpm :
                music.maxbpm = maxbpm
                music.put()
            if dspn != -1 : self.checkAndUpdateFumen(music, 1, dspn, nspn)
            if dsph != -1 : self.checkAndUpdateFumen(music, 2, dsph, nsph)
            if dspa != -1 : self.checkAndUpdateFumen(music, 3, dspa, nspa)
            if dspb != -1 : self.checkAndUpdateFumen(music, 4, dspb, nspb)
            if ddpn != -1 : self.checkAndUpdateFumen(music, 5, ddpn, ndpn)
            if ddph != -1 : self.checkAndUpdateFumen(music, 6, ddph, ndph)
            if ddpa != -1 : self.checkAndUpdateFumen(music, 7, ddpa, ndpa)
            if ddpb != -1 : self.checkAndUpdateFumen(music, 8, ddpb, ndpb)

    def registerNewMusic(self, version, name, genre, artist, minbpm, maxbpm, dspn, dsph, dspa, dspb, ddpn, ddph, ddpa, ddpb, nspn, nsph, nspa, nspb, ndpn, ndph, ndpa, ndpb):
        music = database.MusicData(version=version, name=name, genre=genre, artist=artist, minbpm=minbpm, maxbpm=maxbpm).put()
        if dspn != -1 : self.registerNewFumen(music, 1, dspn, nspn)
        if dsph != -1 : self.registerNewFumen(music, 2, dsph, nsph)
        if dspa != -1 : self.registerNewFumen(music, 3, dspa, nspa)
        if dspb != -1 : self.registerNewFumen(music, 4, dspb, nspb)
        if ddpn != -1 : self.registerNewFumen(music, 5, ddpn, ndpn)
        if ddph != -1 : self.registerNewFumen(music, 6, ddph, ndph)
        if ddpa != -1 : self.registerNewFumen(music, 7, ddpa, ndpa)
        if ddpb != -1 : self.registerNewFumen(music, 8, ddpb, ndpb)

    def checkAndUpdateFumen(self, music, difficultytype, difficulty, notes):
        queryfumen = database.FumenData.gql("WHERE music=:music and difficultytype=:difficultytype", music=music, difficultytype=difficultytype)
        if queryfumen.count(1) == 0:
            self.registerNewFumen(self, music, difficultytype, difficulty, notes)
        else:
            fumen = queryfumen.get()
            if fumen.difficulty != difficulty :
                fumen.difficulty = difficulty
                fumen.put()
            if fumen.notes != notes :
                fumen.notes = notes
                fumen.put()

    def registerNewFumen(self, music, difficultytype, difficulty, notes):
        database.FumenData(music=music, difficultytype=difficultytype, difficulty=difficulty, notes=notes).put()