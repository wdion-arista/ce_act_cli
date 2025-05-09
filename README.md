# CE Act CLI 

### Description:
A cli tool using actrac python modules https://gitlab.aristanetworks.com/arista-eosplus/ACT/actrac
The idea behind this is to create a cli for easier use of the CE ACT API with auto completing commands. All commands have help / descriptions.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Install a devcontaiber(or Fork)
Follow Install guide in https://gitlab.aristanetworks.com/westley.dion/deployment_ce-act_lab1
This package is already installed with ce_act.

You can install the package standalone, but it is better with all the avd / devcontainer features.

``` bash
python3.12 -m venv venv
pip install git+ssh://git@github.com/wdion-arista/ce_act_cli.git
```

## Usage
All commands autocomplete in the devcontainer using double tapping TAB key.
There are 2 main service comamnds **labs** and **topology**.

### Search Topology
``` bash
ce_act topology list search --topo_name West_Lab_3
```
``` json
[
  {
    "schema_type": "topology_resource",
    "schema_version": "0.1.0",
    "id": "f1591df8-8c93-506e-9c46-19c8ff0b44b8",
    "name": "West_Lab_3",
    "description": "West LAb3",
    "topology": null,
    "topology_pathname": "West_Lab_3.yml",
    "diagram_pathname": "",
    "created_at": "2025-03-29T21:04:30",
    "created_by": "westley.dion",
    "modified_by": "unknown",
    "device_count": 10,
    "version": 1,
    "ref_count": 0,
    "self_link": "https://ce.act.arista.com/rest/v1/topologies/f1591df8-8c93-506e-9c46-19c8ff0b44b8"
  }
]
```
``` bash
-== CE ACT CLI ==-
READ TOPO List Search
Found 1 Lab items.
```

### Search Labs
``` bash
ce_act labs list search --labs_name West
```
``` json
[
  {
    "schema_type": "lab_resource",
    "schema_version": "0.1.0",
    "id": "ffb6359468894eb194dd8cd77b714ce2",
    "name": "West_LAB_1",
    "description": "single-dc-l3ls-example",
    "created_at": "2025-03-21T19:12:41",
    "updated_at": "2025-03-25T13:08:14",
    "stage": "",
    "state": 4,
    "user": "westley.dion",
    "topology_definition": "deployment_ce-act_lab1.yml",
    "devices": null,
    "attributes": {
      "locked": false,
      "timeout": 720,
      "deployment_count": 3,
      "deployment_expiration": 129600,
      "enable_lab_deployment_expiration": false
    },
    "self_link": "https://ce.act.arista.com/rest/v1/labs/ffb6359468894eb194dd8cd77b714ce2"
  },
  {
    "schema_type": "lab_resource",
    "schema_version": "0.1.0",
    "id": "4410a77f2dd94df497185fe9dc2c00c2",
    "name": "West_Lab_3",
    "description": "West LAB 3a",
    "created_at": "2025-03-29T21:17:08",
    "updated_at": "2025-03-29T21:18:03",
    "stage": "",
    "state": 5,
    "user": "westley.dion",
    "topology_definition": "West_Lab_3.yml",
    "devices": null,
    "attributes": {
      "locked": false,
      "timeout": 720,
      "deployment_expiration": 129600,
      "deployment_count": 0,
      "enable_lab_deployment_expiration": false
    },
    "self_link": "https://ce.act.arista.com/rest/v1/labs/4410a77f2dd94df497185fe9dc2c00c2"
  }
]

```
``` bash
-== CE ACT CLI ==-
READ LABS List Search
Found 2 Lab items.
```

## Support
Any problems create a ticket in the Issues section of this repo.


## Roadmap
 - TODO:
   - deployment for topology using diagam isn't work on the actrac module.

## Contributing

Anyone can contribute and I welcome the help! 
Here is a quick way to edit locally.

## Testing and editing the python code

``` bash
# Unisntall pip
pip uninstall ce_act

# local build
python setup.py sdist bdist_wheel && \
pip install .

# Testings:
# req: 
# From AVD ENV clone repo into /workspace/repo
cd /workspace/repo
pip install setuptools
pip install pytest
pip install -e . 

```



## Authors and acknowledgment

- Creator: Westley Dion

## License
For open source projects, say how it is licensed.

## Project status
 
