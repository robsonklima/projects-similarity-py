#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import mysql.connector

config = { 'user': 'root', 'password': 'Mysql@2018', 'host': '127.0.0.1', 'database': 'projects_similarity', 'raise_on_warnings': True }

xl = pd.ExcelFile('excel/requirements.xlsx', encoding = "ISO-8859-1")
df = xl.parse('Planilha_1')

for key, row in df.iterrows():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    try:
        cursor.execute(u"INSERT INTO requirements "
              u"(id_project, title, description) VALUES("u"'{id_project}', '{title}', '{description}')".format(
              id_project=row['PROJETO'], title=row['TITULO'], description=row['DESCRICAO']))
        connection.commit()
    except Exception as error:
        print(error)
        connection.rollback()
    cursor.close()
    connection.close()