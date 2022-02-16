from elasticsearch import Elasticsearch
import json
import requests

es = Elasticsearch(['localhost'])

file = open('asset_mapping.json', 'r')
# print(file.read())
# data = json.dumps(file.read())
data = file.read()
# print(data)
res = requests.put("http://localhost:9200/dai-aave-v1/_mapping", data=data, headers={'content-type': 'application/json'})
print(res)
# es.put_script(id=1, body="dai1-aave-v1", context=data)
# es.index("dai1-aave-v1", id="04943y334i_bfndmd",  document=data)

# es.index(f"usdt-aave-v1/_mapping/", id=12345678, document=data)
# # self.output_elasticsearch.index(f"{asset}-aave-v1", id=es_id, document=send_data)