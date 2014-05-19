import urllib2
import sqlite3
import json
import os
import datetime
import time
import sys

#TO DO: you can try to fetch tags from description file?

class CreateCurationDatabase(object):

    def __init__(self, jsonFileName=None):
        self.VALUE_LIST = ["id", "upload_date", "stats_number_of_likes", "thumbnail_large", "thumbnail_medium", "title", "tags", "user_name", "description", "url"]
        self.EXTRA_VALUES = ["date_commit", "to_commit", "alt_url", "title_simple", "title_tr", "description_tr", "credits", "tags_tr", "video_category"]

        self.VALUE_DICT = {"id":("video_id", "integer"), "upload_date":("upload_date", "date"), "stats_number_of_likes":("noLikes", "integer"), 
                "thumbnail_large":("thumbnail_large", "string"), "thumbnail_medium":("thumbnail_medium", "string"), "title":("title", "string"), "tags":("tags", "string"), 
                "user_name":("user_name","string"), "description":("description", "string"), "url":("video_url", "real"),
                "date_commit":("date_commit", "real"), "to_commit":("to_commit", "string"), "alt_url":("alt_url", "string"), "title_simple":("title_simple", "string"),
                "title_tr":("title_tr", "string"), "description_tr":("description_tr", "string"), "credits":("credits", "string"), 
                "tags_tr":("tags_tr", "string"), "video_category":("video_category", "string")
                }

        self.currentPath = os.path.dirname(__file__)
        if jsonFileName:
            self.jsonFilePath = os.path.abspath(os.path.join(self.currentPath, jsonFileName))
        else:
            self.jsonFilePath = None
        self.databasePath = os.path.join(self.currentPath, "nostill_curation.db")

        exists = os.path.exists(self.jsonFilePath)
        if exists:
            self.main()


    def main(self):
        creates = self.createDatabase(self.databasePath)
        self.createDatabaseColumns(self.databasePath)

        if self.jsonFilePath and os.path.exists(self.jsonFilePath):
            jsonContent = self.getJsonContent(self.jsonFilePath)
            for i in jsonContent:
                data = self.getVimeoData(i)
                self.updateDatabase(data, self.databasePath)
            print "database is updated with the provided json file"


    def getJsonContent(self, jsonPath):
        json_file = open(jsonPath)
        data = json.load(json_file)
        json_file.close()
        return data


    def constructVimeoPathsFromIDs(self, jsonPath):
        json_file = open(jsonPath)
        data = json.load(json_file)
        json_file.close()
        prefix = "http://vimeo.com"
        vimeoPathList = []

        for i in data:
            newPath = prefix + i
            vimeoPathList.append(newPath)

        return vimeoPathList


    def getVimeoData(self, givenId):
        time.sleep(0.5)
        output = "json"
        requestPath = "http://vimeo.com/api/v2/video{0}.{1}".format(givenId, output)

        page = urllib2.urlopen(requestPath)
        data = page.read()
        json_data = json.loads(data)
        return json_data[0]


    def createDatabase(self, databasePath):
        exists = os.path.exists(databasePath)
        if not exists:
            db = sqlite3.connect(databasePath)
            cursor = db.cursor()
            cursor.execute('''CREATE TABLE videos (db_id INTEGER)''')

            db.commit()
            db.close()
            return True

        else:
            print "a database file already exists at the given path"
            return False


    def createDatabaseColumns(self, databasePath):
        db = sqlite3.connect(databasePath)
        cursor = db.cursor()

        all_values = self.VALUE_LIST[:]
        for j in self.EXTRA_VALUES:
            all_values.append(j)

        for i in all_values:
            item = self.VALUE_DICT[i]
            if item[1] == "integer":
                valueType = "INTEGER"
            if item[1] == "date":
                valueType = "TEXT"
            if item[1] == "string":
                valueType = "TEXT"
            if item[1] == "real":
                valueType = "BLOB"
            try:
                cursor.execute("ALTER TABLE videos ADD COLUMN '%s' '%s'" % (item[0], valueType))
            except Exception as e:
                print e

        db.commit()
        db.close()


    def updateDatabase(self, data, databasePath):
        db = sqlite3.connect(databasePath)
        cursor = db.cursor()

        query =  "SELECT * FROM videos ORDER BY db_id DESC"
        fetch = cursor.execute(query)
        allEntries = fetch.fetchall()

        if not allEntries:
            lastId = 0
        else: 
            lastId = len(allEntries)
        currentId = lastId + 1

        dataEntryTuple = (currentId, )
        dataEntryList = []

        for i in self.VALUE_LIST:
            exists = data.get(i)
            if exists:
               value = (data[i],)
            else:
                value = ("NONE", )
            dataEntryTuple += value

        for j in self.EXTRA_VALUES:
            if j == "date_commit":
                now = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                value = (now,)
            elif j == "commit":
                value = ("true", )
            else:
                value = ("NONE", )
            dataEntryTuple += value


        dataEntryList.append(dataEntryTuple)

        query = "SELECT * FROM videos WHERE video_id = ?"
        currentVideoId = data["id"]
        fetch = cursor.execute(query, [(currentVideoId)])
        fetched = fetch.fetchall()

        if not fetched:
            try:
                cursor.executemany('''INSERT INTO videos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', dataEntryList)
                db.commit()
            except Exception as e:
                db.rollback()
                print e
                #raise e
        else:
            print "given video_id already exists"

        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        jsonFileName = sys.argv[1]
    else:
        jsonFileName = None
    ccd = CreateCurationDatabase(jsonFileName)