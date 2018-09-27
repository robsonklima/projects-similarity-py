from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import mysql.connector

config = {'user': 'root', 'password': 'Mysql@2018', 'host': '127.0.0.1', 'database': 'projects_similarity', 'raise_on_warnings': True}

def get_projects():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(buffered=True)
        cursor.execute(u"SELECT id, title, project_chapter FROM projects ORDER BY 1 ASC")
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def insert_entity(project_id, name, type, salience, wikipedia_url):
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(buffered=True)
        query = u"INSERT INTO entities (project_id, name, type, salience, wikipedia_url, date_add) " \
                u"VALUES ('{project_id}', '{name}', '{type}', {salience}, '{wikipedia_url}', now())"\
            .format(project_id=project_id, name=name, type=type, salience=salience, wikipedia_url=wikipedia_url)
        cursor.execute(query)
        db.commit()

        if cursor.lastrowid:
            return cursor.lastrowid

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

client = language.LanguageServiceClient()

for (id, title, project_chapter) in get_projects():
    try:
        document = types.Document(content=project_chapter, type=enums.Document.Type.PLAIN_TEXT)
        entities = client.analyze_entities(document).entities
        entity_type = (
        'UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION', 'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

        for entity in entities:
            #insert_entity(id, entity.name, entity_type[entity.type], entity.salience, entity.metadata.get('wikipedia_url', '-'))
            print('Fake insert')
        print(u"Project {id} processed...".format(id=id))
    except Exception as e:
        print(e)