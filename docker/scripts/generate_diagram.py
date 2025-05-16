#!/usr/bin/env python3
"""
# Mermaid cli test
docker run -v $LOCAL_WORKSPACE_FOLDER:/data minlag/mermaid-cli -i temp/test_netowrk_arch.mmd -o output2.svg -c temp/config.json --iconPacks '@iconify-json/clarity' --iconPacks '@iconify-json/logos' --iconPacks '@iconify-json/lucide' --iconPacks '@iconify-json/bi'
"""
import yaml
from pathlib import Path
import subprocess
import os
from collections import defaultdict
import os,sys
from pathlib import Path

home_dir = Path.home()
from dotenv import load_dotenv

# Create node groups
grouped_nodes = defaultdict(list)
styles = []
PROJECT_PATH='/workspace'


dotenv_path = Path(f'{PROJECT_PATH}/.env')
if not os.path.exists(dotenv_path):
    sys.exit("Missing file")
load_dotenv(dotenv_path=dotenv_path)

PROJECT_NAME = str(os.getenv('PROJECT_NAME', 'test')).strip('"')
print(PROJECT_NAME)

ACT_PATH_ENV = str(os.getenv('ACT_PATH', 'act')).strip('"')

ACT_OUTPUT_PATH_ENV = str(os.getenv('ACT_OUTPUT_PATH', 'documentation/images')).strip('"')

AVD_DOCUMENT_PATH_ENV = str(os.getenv('AVD_DOCUMENT_PATH', 'documentation/fabric/FABRIC-documentation.md')).strip('"')

DIAGRAM_SITES_ENV = str(os.getenv('DIAGRAM_SITES', None)).strip('"')
LOCAL_WORKSPACE_FOLDER_ENV = os.getenv('LOCAL_WORKSPACE_FOLDER', '.')

for key, value in os.environ.items():
    print(f"{key} = {value}")


## MKDIR
# Act topology File
ACT_PATH=f'{PROJECT_PATH}/{ACT_PATH_ENV.strip('"')}'
# images Folder
ACT_OUTPUT_PATH=f'{PROJECT_PATH}/{ACT_OUTPUT_PATH_ENV}'
# Diagram base name
ACT_OUTPUT_NAME=f"{ACT_OUTPUT_PATH}/{PROJECT_NAME}_network_diagram"
# Input README md File
AVD_DOCUMENT_PATH=f"{PROJECT_PATH}/{AVD_DOCUMENT_PATH_ENV}"
# Local working direcoty
LOCAL_WORKSPACE_FOLDER = LOCAL_WORKSPACE_FOLDER_ENV
MERMAID_ACT_OUTPUT_NAME=f"/data/{ACT_OUTPUT_PATH_ENV}/{PROJECT_NAME}_network_diagram"
Path(f"{ACT_OUTPUT_PATH}").mkdir(parents=True, exist_ok=True)


def mermaid_cli(app_folder,input_filename, output_filename):
    try:
        result = subprocess.run([
            "docker","run","--rm","-v",f"{app_folder}:/data","minlag/mermaid-cli",
            "-i", str(input_filename),
            "-o", str(output_filename),
            #"--puppeteerConfigFile", "scripts/puppeteer-config.json",
            "--scale", "2",
            "--iconPacks", "'@iconify-json/clarity'",
            "--iconPacks", "'@iconify-json/logos'", 
            "--iconPacks", "'@iconify-json/lucide'", 
            "--iconPacks", "'@iconify-json/bi'"
        ], check=True, capture_output=True, text=True)

        print("STDOUT:\n", result.stdout)
        print("SVG diagram generated successfully.")

    except subprocess.CalledProcessError as e:
        print("Command failed:")
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)
        raise

# Load the YAML file

yaml_file = f"{ACT_PATH}/{PROJECT_NAME}.yml"
print(yaml_file)
with open(yaml_file, "r") as f:
    data = yaml.safe_load(f)

nodes = {}
for node_entry in data["nodes"]:
    for name, details in node_entry.items():
        nodes[name] = details

if DIAGRAM_SITES_ENV is not None:
    diagram_sites = DIAGRAM_SITES_ENV.split(",")
    for name in nodes:
        for site in diagram_sites:
            #if name.upper().startswith(site):
            site_name, site_description = site.split("=")
            if site_name.upper() in name.upper():

                grouped_nodes[site_description].append(name)
                break

for name in nodes:

    # Style based on BLUE, RED, PURPLE
    color = None
    if "BLUE" in name or name.endswith("-B"):
        color = "#cce5ff"
    elif "RED" in name or name.endswith("-R"):
        color = "#ffcccc"
    elif "PURPLE" in name or name.endswith("-P"):
        color = "#e6ccff"
    elif "leaf" in name:
        color = "#ffffcc"
    elif "spine" in name:
        color = "#ccffff"
    if color:
        styles.append(f'style {name} fill:{color},stroke:#333,stroke-width:1px')


# Generate Mermaid graph
mermaid_lines = ["graph RL"]
#mermaid_lines = ["flowchart RL"]
# mermaid_lines.append(f"dummy(( )) --> title")
# mermaid_lines.append(f"'' --> SPINES")

# mermaid_lines.append(f"subgraph TITLE[\"{PROJECT_NAME} - Network Topology Diagram\"]\n direction TB\n BANFF\n  TORONTO\n  PKML\n YYC\nend")
################mermaid_lines.append(f"subgraph SPINES[\" SPINES \"]\n direction TB\n SPINE1\n  SPINE2\n\nend")
# mermaid_lines.append(f"subgraph LEAFS[\" LEAFS \"]\n direction TB\n LEAF1\n  LEAF2\n\nend")

# mermaid_lines.append(f"title[\"🏗️ {PROJECT_NAME} - Network Topology Diagram\"]")
mermaid_lines.append(f"subgraph TITLE[\"{PROJECT_NAME}\"]\n    direction TB")
for site in diagram_sites:
    site_name, site_description = site.split("=")
    mermaid_lines.append(f"    {site_description}")
mermaid_lines.append("end")
styles.append(f'style TITLE fill:#fafafa,stroke:#ccc,stroke-width:6px,white-space:nowrap;')

# Add subgraphs for groups
for group_name, members in grouped_nodes.items():
    mermaid_lines.append(f"subgraph {group_name}\n    direction RL")
    for node in members:
        mermaid_lines.append(f"    {node}")
    mermaid_lines.append("end")
    styles.append(f'style {group_name} fill:#f2f2fa,stroke:#ccc,stroke-width:3px,rx:10,ry:10;')
    


# Add links
for link in data["links"]:
    endpoints = link["connection"]
    if len(endpoints) != 2:
        continue
    dev1, dev2 = endpoints
    dev1_name, port1 = dev1.split(":")
    dev2_name, port2 = dev2.split(":")
    port1_s = port1.replace("thernet", "")
    port2_s = port2.replace("thernet", "")

    mermaid_lines.append(
        f'    {dev1_name} -- "{port1_s} ⇄ {port2_s}" --> {dev2_name}'
    )

# Add styles
mermaid_lines += styles

#mermaid_lines.append(f"style _pad fill:transparent,stroke:transparent")
##############mermaid_lines.append(f'    SPINE1 <--> SPINE2')
# mermaid_lines.append(f'    SPINE1 --> LEAF1')
# mermaid_lines.append(f'    SPINE1 --> LEAF2')
# mermaid_lines.append(f'    SPINE2 --> LEAF1')
# mermaid_lines.append(f'    SPINE2 --> LEAF2')
mermaid_diagram = "\n".join(mermaid_lines)

# Save .mmd file
mmd_path = Path(f"{ACT_OUTPUT_NAME}.mmd")
mermaid_mmd_path = Path(f"{MERMAID_ACT_OUTPUT_NAME}.mmd")
mmd_path.write_text(mermaid_diagram)
# TEST 2
# mmd_path = Path(f"{ACT_OUTPUT_NAME}2.mmd")
# Generate SVG using Mermaid CLI
svg_path = Path(f"{ACT_OUTPUT_NAME}.svg")
mermaid_svg_path = Path(f"{MERMAID_ACT_OUTPUT_NAME}.svg")

mermaid_cli(LOCAL_WORKSPACE_FOLDER,mermaid_mmd_path,mermaid_svg_path)

png_path = Path(f"{ACT_OUTPUT_NAME}.png")
mermaid_png_path = Path(f"{MERMAID_ACT_OUTPUT_NAME}.png")
mermaid_cli(LOCAL_WORKSPACE_FOLDER,mermaid_mmd_path,mermaid_png_path)

print(f"Generated files:\n- {mmd_path}\n- {svg_path}\n- {png_path}")
print(AVD_DOCUMENT_PATH)
if os.path.exists(AVD_DOCUMENT_PATH):
    print("Prepending Diagram")
    insert_text = f"# {PROJECT_NAME} - Network Diagram\n\n"
    insert_text += f"![Network Diagram](../../{ACT_OUTPUT_PATH_ENV}/{PROJECT_NAME}_network_diagram.svg)\n\n"
    # Read the existing content
    with open(AVD_DOCUMENT_PATH, "r") as f:
        original = f.read()

    # Write new content with inserted text
    if insert_text.strip() not in original:
        with open(AVD_DOCUMENT_PATH, "w") as f:
            f.write(insert_text + original)