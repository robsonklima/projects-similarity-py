# -*- coding: utf-8 -*-
from googletrans import Translator
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import mysql.connector

config = {'user': 'root', 'password': 'Mysql@2018', 'host': '127.0.0.1', 'database': 'test', 'raise_on_warnings': True}

def get_projects():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(buffered=True)
        cursor.execute(u"SELECT id, nome, escopo FROM projeto")
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def get_category(title):
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(buffered=True)
        query = u"SELECT id, title FROM categories WHERE title = '{}' LIMIT 1".format(title)
        cursor.execute(query)
        return cursor.fetchall()[0]
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def insert_category(title):
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(buffered=True)
        query = u"INSERT INTO categories (title) VALUES ('{title}')"\
            .format(title=title)
        cursor.execute(query)
        db.commit()

        if cursor.lastrowid:
            return cursor.lastrowid

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def insert_project_category(project_id, category_id, confidence):
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(buffered=True)
        query = u"INSERT INTO projects_categories (project_id, category_id, confidence) VALUES ({project_id}, {category_id}, {confidence})"\
            .format(project_id=project_id, category_id=category_id, confidence=confidence)
        cursor.execute(query)
        db.commit()

        if cursor.lastrowid:
            return cursor.lastrowid

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def translatePtEn(text):
    translator = Translator()
    translated = translator.translate(text, dest='en')

    client = language.LanguageServiceClient()
    return types.Document(content=translated.text.encode('utf-8'), type=enums.Document.Type.PLAIN_TEXT).content

def translateEnPt(text):
    translator = Translator()
    translated = translator.translate(text, dest='pt')

    client = language.LanguageServiceClient()
    return types.Document(content=translated.text.encode('utf-8'), type=enums.Document.Type.PLAIN_TEXT).content


for (id, nome, escopo) in get_projects():
    try:
        translator = Translator()
        translated = translator.translate(escopo, dest='en')

        client = language.LanguageServiceClient()
        document = types.Document(content=translated.text.encode('utf-8'), type=enums.Document.Type.PLAIN_TEXT)

        data = client.classify_text(document).categories

        for category in data:
            print(category)

        print(u"Project {id} processed...".format(id=id))
    except Exception as error:
        print(id, error)