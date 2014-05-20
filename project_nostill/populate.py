import sqlite3
import os
from helper.vimeo import curation_database_creator_vimeo as cdcv

CURRENT_DIR = os.path.dirname(__file__)
VIMEO_DIR = os.path.join(CURRENT_DIR, "helper", "vimeo")
DATABASE_CURATION = "nostill_curation.db"

VALUES_LIST = cdcv.VALUES_ALL
VALUES_DICT = cdcv.VALUES_DICT
TABLE_VALUES_LIST = []
TEMP = [TABLE_VALUES_LIST.append(VALUES_DICT[i][0]) for i in VALUES_LIST]

DATABASE_PATH = os.path.join(VIMEO_DIR, DATABASE_CURATION)


def add_page(table, **kwargs):
    print kwargs
    p = table.objects.get_or_create(**kwargs)[0]
    return p

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def fetch_database_entries(databasePath):
    db = sqlite3.connect(databasePath)
    db.row_factory = dict_factory
    cursor = db.cursor()
    query =  "SELECT * FROM videos ORDER BY db_id DESC"
    fetch = cursor.execute(query)
    allEntries = fetch.fetchall()

    return allEntries


def populate(allEntries, databaseTable):
    for entry in allEntries:
        newDict = {}
        for item in entry.iteritems():
            if item[1] == "NONE":
                value = None
            else:
                value = item[1]
            newDict[item[0]] = value

        add_page(table=table_01, **newDict)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_nostill.settings")
    from nostill.models import Video as table_01
    allEntries = fetch_database_entries(DATABASE_PATH)
    populate(allEntries, table_01)

