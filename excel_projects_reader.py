#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import mysql.connector
import datetime

config = { 'user': 'root', 'password': 'Mysql@2018', 'host': '127.0.0.1', 'database': 'projects_similarity', 'raise_on_warnings': True }

xl = pd.ExcelFile('excel/projects.xlsx', encoding = "ISO-8859-1")
df = xl.parse('Planilha_1')

for key, row in df.iterrows():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    try:
        cursor.execute(u"INSERT INTO projects ("
                       u"client_id, "
                       u"title, "
                       u"project_chapter, "
                       u"final_forecast, "
                       u"domain, "
                       u"unity, "
                       u"accomplished, "
                       u"estimated_hours, "
                       u"performed_hours) VALUES("
                  u"'{client_id}', "
                  u"'{title}', "
                  u"'{project_chapter}', "
                  u"'{final_forecast}', "
                  u"'{domain}', "
                  u"'{unity}', "
                  u"'{accomplished}', "
                  u"{estimated_hours}, "
                  u"{performed_hours})".format(
                            client_id=row['CODIGO'],
                            title=row['TITULO'],
                            project_chapter=row['CENARIODESEJADO'],
                            final_forecast=row['PREVISAOFIM'],
                            domain=row['DOMINIO'],
                            unity=row['UNIDADE'],
                            accomplished=row['FIM'],
                            estimated_hours=row['HORASESTIMADAS'],
                            performed_hours=row['HORASREALIZADAS']
                         )
        )
        connection.commit()
    except Exception as error:
        print(error)
        connection.rollback()
    cursor.close()
    connection.close()

