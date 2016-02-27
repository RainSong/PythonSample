# -*- coding: utf-8 -*-

from pymongo import *

client = MongoClient('localhost',27017)

print client.database_names()

testDb = client['test']

users = testDb['users']

user = users.find({'name':'王五'})
count = user.count()

if count == 0:
 users.insert({'name':'王五','age':20,'sex':'男','work':'programer'})


