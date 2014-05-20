import os
import sys
from django.db import models

CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
sys.path.insert(0, PARENT_DIR)
from helper.vimeo import curation_database_creator_vimeo as cdcv

VALUES_ALL = cdcv.VALUES_ALL
VALUES_DICT = cdcv.VALUES_DICT

# Create your models here.

def create_django_field_dict():
    """creates appropiate django fields using the descriptions decleared in the above CONSTANTS"""
    django_field_dict = {}

    for i in VALUES_ALL:
        item = VALUES_DICT[i]
        max_length = 128
        if item[1] == "integer":
            fieldType = models.IntegerField(max_length = max_length)
        elif item[1] == "date" or "string":
            if item[0] == "thumbnail_medium" or "thumbnail_large":
                max_length = 256
            elif item[0] == "description" or "date_commit" or "description_tr":
                max_length = 1000
            fieldType = models.CharField(max_length = max_length, null=True)
        elif item[1] == "real":
            fieldType = models.URLField(max_length = max_length)

        django_field_dict[item[0]] = fieldType

    return django_field_dict

def __unicode__(self): # not sure about the definition of unicode here and latter appending, am I not overwriting the unicode of the module itself?
    return self.title

django_field_dict = create_django_field_dict()
django_field_dict["__module__"] = __name__

Video = type("Video", (models.Model,), django_field_dict)
Video.__unicode__ = __unicode__