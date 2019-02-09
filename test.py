import os
import json

dic = {
    "test" : "value",
    "raju" : 'dd'
}
with open('config.json', 'w+') as rf:
    try:
        data = json.load(rf)
        #data.update(dic)
        #print(data)
    except Exception as e:
        print(e)
        data = json.dumps(dic)
        rf.write(data)


