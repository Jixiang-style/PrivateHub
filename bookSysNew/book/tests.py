from django.test import TestCase

# Create your tests here.


#
# l=[{"name":"alex","age":23},{"name":"egon","age":34}]
#
# import json
# print (json.dumps(l)) # [{"name": "alex", "age": 23}, {"name": "egon", "age": 34}]

def zhuang(func):
    def newfunc(res):
        print(111)
        func(res)
        print(222)
    return newfunc




@zhuang
def func(res):
    print(123)


func(55)









