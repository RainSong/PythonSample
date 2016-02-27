# -*- coding: utf-8 -*-

fields = ['name','age','sex']
values = ['张三',19,'男']
obj = {}
index = 0
for f in fields:
    obj[f]=values[index]
    index=index+1

print obj
print str(obj)