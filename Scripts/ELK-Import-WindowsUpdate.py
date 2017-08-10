from elasticsearch_dsl import DocType,String,Boolean,Search,Date
from elasticsearch_dsl.connections import connections
from datetime import datetime
import json
filename= "../Files/ansibleresult.json"
settings = "../Files/settings.json"

with open(settings) as es_settings:
    esInfo=json.load(es_settings)
    es = connections.create_connection(hosts=esInfo['esIP']+":"+esInfo['esPort'], timeout=20)


class UpdateResults(DocType):
    hostname=String(index="not_analyzed")
    updateTitle = String(index="not_analyzed")
    kb = String(index="not_analyzed")
    installed = Boolean()
    date=Date()
    class Meta:
        index = 'updateresults'


#### Do this once only ####
UpdateResults.init()
#
with open(filename) as json_data:
    d = json.load(json_data)
    serverIP= list(d.keys())[0]
    d['server']=d.pop(serverIP)
    d['server']['hostname']=serverIP
    j = json.dumps(d['server'])
    runDate=datetime.now()
    for i in d['server']['updates']:
        print(i)
        added = UpdateResults(
            meta={
                'id':"-".join([d['server']['hostname'],*d['server']['updates'][i]['kb']])
            },
            hostname=d['server']['hostname'],
            updateTitle=d['server']['updates'][i]['title'],
            kb = d['server']['updates'][i]['kb'],
            installed = d['server']['updates'][i]['installed'],
            date=runDate
        ).save()
        print(added)


