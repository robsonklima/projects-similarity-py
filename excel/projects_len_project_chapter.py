import mysql.connector

config = {'user': 'root', 'password': 'Mysql@2018', 'host': '127.0.0.1', 'database': 'projects_similarity', 'raise_on_warnings': True}

def get_projects():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(buffered=True)
        cursor.execute(u"SELECT id, title, project_chapter FROM projects")
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()


for (id, title, project_chapter) in get_projects():
    print(len(project_chapter))