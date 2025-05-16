import yaml

import os,sys
from pathlib import Path
home_dir = Path.home()
from dotenv import load_dotenv

dotenv_path = Path('/workspace/.env')
load_dotenv(dotenv_path=dotenv_path)

project_name = os.getenv('PROJECT_NAME', 'inventory-ce_act.yml')
print(project_name)

act_inventory_file=f'/workspace/temp/{project_name}-inventory.yml'
if not os.path.exists(act_inventory_file):
    sys.exit("Missing file")

if not os.path.exists('/workspace/inventory.yml'):
    sys.exit("Missing file")

# Read file1
with open(act_inventory_file, 'r') as f:
    data1 = yaml.safe_load(f)

# Create a mapping of hostname to internal_ip
ip_mapping = {}
print(data1)
for device_type in data1[0]['devices']:
    for device in data1[0]['devices'][device_type]:
        ip_mapping[device['hostname']] = device['internal_ip']

# Read file2
with open('/workspace/inventory.yml', 'r') as f:
    data2 = yaml.safe_load(f)

# Update ansible_host values in file2
for group in data2['all']['children'].values():
    if 'hosts' in group:
        for host, host_vars in group['hosts'].items():
            if host in ip_mapping:
                host_vars['ansible_host'] = ip_mapping[host]

# Write updated file2 back to disk
with open('/workspace/inventory-updated.yml', 'w') as f:
    yaml.dump(data2, f)

print("Updated /workspace/inventory.yml with new ansible_host values.")
