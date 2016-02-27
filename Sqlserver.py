# -*- coding: utf-8 -*-
import pyodbc

nxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=heima;UID=sa;PWD=ygj000')
cursor = nxn.cursor()
cursor.execute("select name,object_id,create_date,modify_date from sys.objects where type = 'u'")
for row in cursor:
    print 'name:{0} id:{1:15} create_date:{2:15} modify_date:{3:15}'.format(row[0],row[1],row[2],row[3])





