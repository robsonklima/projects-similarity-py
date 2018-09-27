# -*- coding: utf-8 -*-
from googletrans import Translator
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.projects_similarity
collection = db['projects']
cursor = collection.find({})

for i, project in enumerate(cursor):
    print(u'{} - {}'.format(str(i), project['name']))

    client = language.LanguageServiceClient()
    document = types.Document(content=project['description'].encode('utf-8'), type=enums.Document.Type.PLAIN_TEXT)

    try:
        categories = []
        data = client.classify_text(document).categories
        for category in data:
            categories.append({
                'name': category.name,
                'confidence': category.confidence
            })

        print(categories)

        collection.find_one_and_update(
            {'_id': project["_id"]},
            {'$set': {'categories': categories}}
        )
    except:
        print(u"Nothing found!")