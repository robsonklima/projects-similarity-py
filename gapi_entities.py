# -*- coding: utf-8 -*-
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.projects_similarity
collection = db['projects']
cursor = collection.find({})

for i, project in enumerate(cursor):
    print(u'{} - {} - {}'.format(str(i), project['_id'], project['name']))

    try:
        client = language.LanguageServiceClient()
        document = types.Document(content=project['description'], type=enums.Document.Type.PLAIN_TEXT)
        data = client.analyze_entities(document).entities
        entity_type = (u'UNKNOWN', u'PERSON', u'LOCATION', u'ORGANIZATION', u'EVENT', u'WORK_OF_ART', u'CONSUMER_GOOD', u'OTHER')

        entities = []
        for entity in data:
            if (u'UNKNOWN' not in entity_type[entity.type] and u'OTHER' not in entity_type[entity.type]):
                entities.append({
                    'name': entity.name,
                    'type': entity_type[entity.type],
                    'metadata': entity.metadata,
                    'salience': entity.salience,
                    'wikipedia_url': entity.metadata.get('wikipedia_url', '-')
                })

        print(entities)

        collection.find_one_and_update(
            {'_id': project["_id"]},
            {'$set': {'entities': entities}}
        )
    except:
        print(u'Something failed!')