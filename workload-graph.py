import json
import requests

url = "https://mp-api.prod.hypershield.engineering/api/v1/ts-agent"
api_token = ""

headers = {"Authorization" : "Bearer " + api_token,
           "Content-Type": "application/json",
           "Accept": "application/json"}
try:
  response = requests.request('GET', url, headers=headers)
except requests.exceptions.HTTPError as err:
  raise SystemExit(err)

agents = []
agents_data = response.json()["data"]

print('Listing agents in tenant:')
for agent in agents_data:
    agents.append({'name': {agent["name"]}, 'id': {agent["id"]}})
    print(f'  Name: {agent["name"]}')
    print(f'  Id: {agent["id"]}')
    print(f'  Description: {agent["description"]}')
    print(f'  Status: {agent["status"]}')
    print(f'  ----------')
    
for agent in agents_data:
    print (f'\nGenerating Workload Graph for UUID {agent["id"]}')
    try:
      response = requests.request('GET', url + "/" + agent["id"] + "/workload-graph", headers=headers)
      filename = 'graph_' + agent["id"] + '.json'
      with open(filename , 'w') as f:
          f.write(json.dumps(response.json(), indent=2))
          print(f'Created {filename}')
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)
