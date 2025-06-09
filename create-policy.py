mport requests
import json

# Replace X with your pod number!

pod_number = "POD X"
source_ips = ['192.168.18.1']

url = "https://mp-api.prod.hypershield.engineering/api/v1/"
api_token = ""
tenant_id = ""

headers = {"Authorization": "Bearer " + api_token,
           "Content-Type": "application/json",
           "Accept": "application/json"
           }

# Create Object
operation_id = "object"
payload = {
    "tenantId": tenant_id,
    "name": f"{pod_number} Policy Object",
    "description": "",
    "objectType": "DAF_NETWORK_OBJECT",
    "contents": [
      {
        "sgt": [],
        "vlan": [],
        "@type": "DAF_NETWORK_CONTENT",
        "addresses": [
          {
            "ips": source_ips,
            "port": "",
            "awsTags": [],
            "vCenterTags": []
          }
        ]
      }
    ]
}

try:
    response = requests.request('POST', url + operation_id, headers=headers, data=json.dumps(payload))
    principal_object_id = response.json()['id']
    print(f"Principal object created ID is: {principal_object_id}")
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

# Create Policy Group

operation_id = "policy-group"
payload = {
  "tenantId": tenant_id,
  "name": f"{pod_number} Policy Group",
  "description": f"PARC for {pod_number}",
  "status": "OPEN",
  "type": "DEFAULT",
  "diffs": []
}

try:
    response = requests.request('POST', url + operation_id, headers=headers, data=json.dumps(payload))
    policy_group_id = response.json()['id']
    print (f"{pod_number} Policy Group created and ID is: {policy_group_id}")
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

# Add Objects to Group

operation_id = "policy-group/" + policy_group_id + "/add-policy"
resource_object_id = "4c5782a7-d6ad-4228-8e31-9e9d1041b87d"

payload = {
      "tenantId": tenant_id,
      "policyGroupId": policy_group_id,
      "name": "Policy",
      "description": "",
      "policyType": "FIREWALL",
      "cedar": {
        "action": {
          "op": "in",
          "entity": [
            {
              "id": "icmp",
              "type": "DAF_NETWORK_ACTION"
            }
          ]
        },
        "effect": "permit",
        "resource": {
          "op": "==",
          "entity": {
            "id": resource_object_id,
            "type": "DAF_NETWORK_ACTION"
          }
        },
        "effectAnd": "warn",
        "principal": {
          "op": "==",
          "entity": {
            "id": principal_object_id,
            "type": "DAF_NETWORK_ACTION"
          }
        }
      }
}

try:
    response = requests.request('POST', url + operation_id, headers=headers, data=json.dumps(payload))
    print (f"Policy added to {pod_number} Policy Group")
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
