
# Copyright (c) 2022, Arista Networks, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   Neither the name of Arista Networks nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import pyinputplus as pyip
import pprint
pp = pprint.PrettyPrinter(indent=2)

#from constants import *
from ce_act.functions import *

from actrac.client import ACTClient

''' Topology '''
def topology_commands(api_key, arg_values=None, output_type = "print", debug = False ):
    logger_topo = setup_logger(__name__, f"log_{__name__}.log")
    logger_topo.propagate = False
    logger_topo.info(f"LABS: This is logged in {__name__}.log")
    logger_topo.setLevel(arg_values.log)
    logger_topo.info(f"Topology: ")
    # Defaults
    return_result = {
        "ERROR":[],
        "PRINT":[],
        "CODE":200,
        "RESULTS":[]
        }
    result = None

    #Client connect
    client = client_connect(
        api_key, 
        arg_values.base_url,  
        debug=debug
    )
    
    # LIST

    if arg_values.action_command == 'list':
        logger_topo.info(f"READ TOPO List")
        if arg_values.topo_list_command == "search":
            
            return_result["PRINT"].append(color_txt("GREEN",f"READ TOPO List Search"))
            if "user_name" in arg_values and arg_values.user_name is not None:
                logger_topo.info(f"User_name arg found")
                result = client.api.read_topologies(user=arg_values.user_name)
            elif "topo_name" in arg_values and arg_values.topo_name is not None:
                logger_topo.info(f"Lab_name arg found")
                result = client.api.read_topologies(name=arg_values.topo_name)
            else:
                return_result["PRINT"].append(color_txt("RED",f"Need a username or Topo name to search"))
                return_result["ERROR"].append("Need a username or Topo name to search")
        elif arg_values.topo_list_command == "all":
            result = client.api.read_topologies()
        else:
            result = client.api.read_topologies()
        
    
    if result:
        
        result_cnt = len(result)
        
        return_result["PRINT"].append(print_found(result_cnt,"Lab items."))
        #  SORT
        if "sort_type" in arg_values and arg_values.sort_desc is not None:
            sort_type=arg_values.sort_type
        else:
            sort_type='name'

        if "sort_desc" in arg_values and arg_values.sort_desc is not None and arg_values.sort_desc == True:
            sort_reverse=True
        else:
            sort_reverse=False

        result_sorted = sorted(result, key=lambda x: x[sort_type], reverse=sort_reverse)

        #  LIMIT
        if "limit" in arg_values and arg_values.limit is not None and arg_values.limit > 0:
            output_limit = arg_values.limit
        else:
            output_limit = None
        if output_limit:
            result_render = result_sorted[:arg_values.limit]
            return_result["PRINT"].append(color_txt("YELLOW",f"Count over {arg_values.limit} Reducing query to {len(result_render)}"))
        else:
            result_render = result_sorted

        pp_data=pp.pformat(result_render)
            
        return_result["RESULTS"] = result_render
            

    # GET (Nodes / DeviceModels?)

    if arg_values.action_command == 'get':
        #define args:

        # Get Nodes
        if arg_values.topo_get_command == "nodes":
            return_result["PRINT"].append(color_txt("GREEN",f"TOPO getting Nodes"))
            get_topo_id_result = client.api.available_node_versions()
            get_topo_id_result_cnt = len(get_topo_id_result)
            return_result["RESULTS"] = get_topo_id_result
        # Get Models
        #elif arg_values.topo_get_command == "device_models":
        #    return_result["PRINT"].append(color_txt("GREEN",f"TOPO getting Device Models"))
        #    get_topo_id_result = client.api.available_node_versions()
        #    get_topo_id_result_cnt = len(get_topo_id_result)
        #    return_result["RESULTS"] = get_topo_id_result
        else:
            return_result["PRINT"].append(color_txt("RED",f"No action selected!"))

    # CREATE

    if arg_values.action_command == 'create':
        return_result["PRINT"].append(color_txt("GREEN",f"TOPO Create"))
        
        if arg_values.topo_def is not None and arg_values.topo_name is not None:
            topo_def = arg_values.topo_def
            topo_name = arg_values.topo_name
            topo_description = None
            name_exists = None
            result = client.api.read_topologies(name=topo_name)
            result_cnt = len(result)
            if result_cnt > 0:
                return_result["PRINT"].append(color_txt("RED",f"Topology Already called {topo_name}. Please user another name."))
                name_exists = True
            #  Description
            if arg_values.topo_description is not None:
                topo_description = arg_values.topo_description
            else:
                topo_description = f"Topo {topo_name}"
            #  Image
            if arg_values.topo_image is not None:
                topo_image = arg_values.topo_image
            else:
                topo_image = None
            if name_exists is None:
                return_result["PRINT"].append(color_txt("GREEN",f"Lab name:{topo_name}\nTopology name:{topo_def}\nDescription:{topo_description}\nImage:{topo_image}"))

            result = client.api.create_topology(
                name=topo_name,
                topo_def_file_path=topo_def,
                description=topo_description,
                diagram_file_path=topo_image
            )
            return_result["RESULTS"] = [client.api.poll_operation(result,poll_iterations=10)]
            

    # READ
    if arg_values.action_command == 'read':
        #define args:
        topo_id = None
        return_result["PRINT"].append(color_txt("GREEN",f"TOPO Read"))
        if "topo_id" in arg_values and arg_values.topo_id is not None:
            topo_id = arg_values.topo_id
        elif "topo_name" in arg_values and arg_values.topo_name is not None:
            return_result["PRINT"].append(color_txt("GREEN",f"Starting search for topo name: {arg_values.topo_name}"))
            get_topo_id_result = client.api.read_topologies(name=arg_values.topo_name)
            get_topo_id_result_cnt = len(get_topo_id_result)
            logger_topo.info(str(get_topo_id_result))
            if get_topo_id_result_cnt == 0:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found 0 Entries!"))
            elif get_topo_id_result_cnt == 1:
                return_result["PRINT"].append(color_txt("GREEN",f"Search found 1 Entry!"))
                topo_id = get_topo_id_result[0]['id']
            elif get_topo_id_result_cnt > 1:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found {get_topo_id_result_cnt} Entries! Query should only return 1"))
            else:
                topo_id = None   
        elif "topo_def" in arg_values and arg_values.topo_def is not None:
            return_result["PRINT"].append(color_txt("GREEN",f"Starting search for topo def: {arg_values.topo_def}"))
            get_topo_id_result = client.api.read_topologies(topology_file=arg_values.topo_def)
            get_topo_id_result_cnt = len(get_topo_id_result)
            logger_topo.info(str(get_topo_id_result))
            if get_topo_id_result_cnt == 0:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found 0 Entries!"))
            elif get_topo_id_result_cnt == 1:
                return_result["PRINT"].append(color_txt("GREEN",f"Search found 1 Entry!"))
                topo_id = get_topo_id_result[0]['id']
            elif get_topo_id_result_cnt > 1:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found {get_topo_id_result_cnt} Entries! Query should only return 1"))
            else:
                topo_id = None   

        # topology_definition             
        else:
            return_result["PRINT"].append(color_txt("RED",f"No id or name selected!"))
            topo_id = None

        if topo_id is not None:
            return_result["PRINT"].append(color_txt("GREEN",f"TOPO reading Lab: {topo_id}"))
            get_topo_id_result = [client.api.read_topology(topology_definition_id=topo_id)]
            get_topo_id_result_cnt = len(get_topo_id_result)

            logger_topo.info(str(get_topo_id_result))
            return_result["RESULTS"] = get_topo_id_result

    # UPDATE
    if arg_values.action_command == 'update':
        #define args:
        topo_id_val = None
        topo_found = False
        get_topo_id_result_cnt = 0
        return_result["PRINT"].append(color_txt("GREEN",f"TOPO update"))
        
        if "topo_id" in arg_values and arg_values.topo_id is not None:
            logger_topo.info(f"TOPO Read topo_id")
            get_topo_id_result = [client.api.read_topology(topology_definition_id=arg_values.topo_id)]
            get_topo_id_result_cnt = len(get_topo_id_result)
            topo_found = True

        elif "topo_name" in arg_values and arg_values.topo_name is not None:
            return_result["PRINT"].append(color_txt("GREEN",f"Starting search for topo name: {arg_values.topo_name}"))
            get_topo_id_result = client.api.read_topologies(name=arg_values.topo_name)
            get_topo_id_result_cnt = len(get_topo_id_result)
            topo_found = True
        else:
            return_result["PRINT"].append(color_txt("RED",f"No id or name selected!"))
            topo_id_val = None
        item_selected = False
        if topo_found == True:
            return_result["PRINT"].append(color_txt("YELLOW",f"TOPO FOUND ID"))
            logger_topo.info(str(get_topo_id_result))
            if get_topo_id_result_cnt == 0:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found 0 Entries!"))
            elif get_topo_id_result_cnt == 1:
                return_result["PRINT"].append(color_txt("GREEN",f"Search found 1 Entry!"))
                topo_id_val = get_topo_id_result[0]
                item_selected = True
            elif topo_id_val > 1:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found {get_topo_id_result_cnt} Entries! Query should only return 1"))
                topo_id_val = None
            else:
                topo_id_val = None

        if item_selected:
            topo_description = topo_id_val["description"]
            topo_name = topo_id_val["name"]
            topo_topology_pathname = topo_id_val["topology_pathname"]
            topo_diagram_pathname = topo_id_val["diagram_pathname"]
            topo_created_by = topo_id_val["created_by"]
            return_result["PRINT"].append(color_txt("OKBLUE",f"\nPRE UPDATE:\nTopo name: {topo_name}\nTopology file name: {topo_topology_pathname}\nDescription: {topo_description}\nImage File: {topo_diagram_pathname}\n\nCreated By: {topo_created_by}"))
            run_command = True
            # Description
            if arg_values.topo_description is not None: 
                topo_description = arg_values.topo_description
            else:
                topo_description = topo_id_val["description"]
            # New name
            if arg_values.new_topo_name is not None: 
                topo_name = arg_values.new_topo_name
            else:
                topo_name = topo_id_val["name"]
            #  Updated Topo Def file
            if arg_values.topo_def is not None: 
                # files must be same name
                base_filename = os.path.basename(arg_values.topo_def)
                if base_filename == topo_id_val["topology_pathname"]:
                    topo_def = arg_values.topo_def
                else:
                    logger_topo.critical("File names must be the same on update!")
                    return_result["PRINT"].append(color_txt("RED",f"File names must be the same on update!"))
                    run_command = False
            else:
                topo_def = None
            #  topo_image
            if arg_values.topo_image is not None: 
                topo_image = arg_values.topo_image
            else:
                topo_image = None

            if run_command:
                return_result["PRINT"].append(color_txt("CYAN",f"\nPOST UPDATE:\nTopo name: {topo_name}\nTopology file name: {topo_def}\nDescription: {topo_description}\nImage File: {topo_image}"))
                

            result = client.api.update_topology(
                topo_id=topo_id_val["id"],
                name=topo_name,
                topo_def_file_path=topo_def,
                description=topo_description,
                diagram_file_path=topo_image
            )
            return_result["RESULTS"] = [client.api.poll_operation(result,poll_iterations=10)]
    
    # DELETE
    if arg_values.action_command == 'delete':
        
        topo_id = None
        return_result["PRINT"].append(color_txt("GREEN",f"TOPO Read"))
        if "topo_id" in arg_values and arg_values.topo_id is not None:
            logger_topo.info(f"LAB Read topo_id")
            get_topo_id_result = [client.api.read_topology(topology_definition_id=arg_values.topo_id)]
            get_topo_id_result_cnt = len(get_topo_id_result)
            topo_found = True

        elif "topo_name" in arg_values and arg_values.topo_name is not None:
            return_result["PRINT"].append(color_txt("GREEN",f"Starting search for topo name: {arg_values.topo_name}"))
            get_topo_id_result = client.api.read_topologies(name=arg_values.topo_name)
            get_topo_id_result_cnt = len(get_topo_id_result)
            topo_found = True
        else:
            return_result["PRINT"].append(color_txt("RED",f"No id or name selected!"))
            topo_id_val = None
        item_selected = False
        if topo_found == True:
            return_result["PRINT"].append(color_txt("YELLOW",f"LAB FOUND ID"))
            logger_topo.info(str(get_topo_id_result))
            if get_topo_id_result_cnt == 0:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found 0 Entries!"))
            elif get_topo_id_result_cnt == 1:
                return_result["PRINT"].append(color_txt("GREEN",f"Search found 1 Entry!"))
                topo_id_val = get_topo_id_result[0]
                item_selected = True
            elif topo_id_val > 1:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found {get_topo_id_result_cnt} Entries! Query should only return 1"))
                topo_id_val = None
            else:
                topo_id_val = None

        if item_selected:
            run_command_check = False
            if output_type == 'print':
                response = pyip.inputYesNo("This will destory any data on the VMs. Do you want to continue?")
                if response == 'yes':
                    run_command_check = True
                    print("Continuing...")
                else:
                    run_command_check = False
                    print("Exiting...")
            if run_command_check:
                return_result["PRINT"].append(color_txt("GREEN",f"TOPO deleting Lab: {topo_id_val}"))
                get_topo_id_result = client.api.delete_topology(topology_definition_id=topo_id_val["id"])
                get_topo_id_result_cnt = len(get_topo_id_result)

                logger_topo.info(str(get_topo_id_result))
                return_result["RESULTS"] = [client.api.poll_operation(get_topo_id_result)]

    #  Disconnect Client
    client_disconnect(client)

    return return_result
