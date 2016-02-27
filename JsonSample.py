# -*- coding: utf-8 -*-

#import demjson
import json

class Person:
    Name = ''
    Age = 0
    Sex = ''

    def __init__(self,name,age,sex):
        self.Name = name
        self.Age = age
        self.Sex = sex

    def say(self):
        print 'name:{0},sex:{1},age{2}'.format(self.Name,self.Sex,self.Age)


if __name__ == '__main__':
    p = Person('张三',18,'男')
    p.say()

    print json.dumps(p.__dict__)

    # json = demjson.encode(p)
    #
    # print p
