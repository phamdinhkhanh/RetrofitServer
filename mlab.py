import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds163020.mlab.com:63020/retrofitserver
host = "ds163020.mlab.com"
port = 63020
db_name = "retrofitserver"
username = "khanh"
password = "khanh"

def connect():
    mongoengine.connect(db_name,host = host,port = port, username = username, password = password)

def listjson(l):
    import json
    return [json.loads(item.to_json()) for item in l]

def itemjson(item):
    import json
    return json.loads(item.to_json())