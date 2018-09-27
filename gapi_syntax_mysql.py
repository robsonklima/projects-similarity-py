from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import mysql.connector

client = language.LanguageServiceClient()

config = {'user': 'root', 'password': 'Mysql@2018', 'host': '127.0.0.1', 'database': 'projects_similarity', 'raise_on_warnings': True}

def get_requirements():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(buffered=True)
        cursor.execute(u"SELECT id, title, description FROM requirements")
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def insert_syntax(requirement_id, tag, content, lemma):
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(buffered=True)
        query = u"INSERT INTO syntax (requirement_id, tag, content, lemma) VALUES ({requirement_id}, '{tag}', '{content}', '{lemma}')"\
            .format(requirement_id=requirement_id, tag=tag, content=content, lemma=lemma)
        cursor.execute(query)
        db.commit()

        if cursor.lastrowid:
            return cursor.lastrowid

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

for (id, title, description) in get_requirements():
    try:
        document = types.Document(content=description, type=enums.Document.Type.PLAIN_TEXT)
        tokens = client.analyze_syntax(document).tokens
        pos_tag = (
        'UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

        for token in tokens:
            insert_syntax(id, pos_tag[token.part_of_speech.tag], token.text.content, token.lemma)

        print(u"Finishing requirement processing: {id}...".format(id=id))
    except Exception as error:
        print(id, error)

