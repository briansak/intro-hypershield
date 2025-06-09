import requests
import json

url = "https://mp-api.prod.hypershield.engineering/api/v1/"
api_token = ""
headers = {"Authorization" : "Bearer " + api_token, "accept" : "application/json", "content-type" : "application/json"}

# Get Workloads with Shields
operation_id = "workload"

try:
    response = requests.request('GET', url + operation_id, headers=headers)
    workloads = response.json()

    for workload in workloads["data"]:
        if workload["shields"]:
            workload_id = (workload["id"])
            shield = (workload["shields"][0]["id"])
            print (f'Identified {shield} in workload with id: {workload_id}')		
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

# Deploy Shields
operation_id = "shield-status"

payload = {"shieldId": shield, "workloadId": workload_id, "enabled": "true"}

try:
    response = requests.request('POST', url + operation_id, headers=headers, data=json.dumps(payload))
    print (f'Shield for {shield} deployed successfully.')

except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
