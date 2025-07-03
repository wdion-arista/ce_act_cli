
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

from ce_act.config import *
from ce_act.functions import *

from actrac.client import ACTClient

''' Labs '''
def labs_commands(api_key, arg_values=None, output_type = "print", debug = False ):
    logger_lab = setup_logger(__name__, f"log_{__name__}.log")
    logger_lab.info(f"LABS: This is logged in {__name__}.log")
    logger_lab.propagate = False
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
        logger_lab.setLevel(arg_values.log)
        logger_lab.info(f"LABS:LABS List")
        # Search
        if arg_values.labs_list_command == "search":
            return_result["PRINT"].append(color_txt("GREEN",f"READ LABS List Search"))
            
            if "user_name" in arg_values and arg_values.user_name is not None:
                logger_lab.info(f"User_name arg found")
                
                result = client.api.read_labs(user=arg_values.user_name)
            elif "lab_name" in arg_values and arg_values.lab_name is not None:
                logger_lab.info(f"Lab_name arg found")
                result = client.api.read_labs(name=arg_values.lab_name)
            else:
                logger_lab.critical(f"Need a username or lab name to search")
                return_result["ERROR"].append("Need a username or lab name to search")
        elif arg_values.labs_list_command == "all":
            result = client.api.read_labs()
        else:
            result = client.api.read_labs()
        
    
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
        # Is user_name defined
            # Search for user name
            #result = [item for item in labs if user_name in item["user"]]

        pp_data=pp.pformat(result_render)
        
        #return_result["PRINT"].append(color_txt("GREEN",f"{pp_data}"))
        
            
        return_result["RESULTS"] = result_render
            

    # ACTION (START / STOP / DEPLOY / UNDEPLOY)

    if arg_values.action_command == 'action':
        #define args:
        lab_id = None

        logger_lab.info(f"LABS action")
        if "lab_id" in arg_values and arg_values.lab_id is not None:
            lab_id = arg_values.lab_id
        elif "lab_name" in arg_values and arg_values.lab_name is not None:
            return_result["PRINT"].append(color_txt("GREEN",f"Starting search for lab name: {arg_values.lab_name}"))
            get_lab_id_result = client.api.read_labs(name=arg_values.lab_name)
            get_lab_id_result_cnt = len(get_lab_id_result)
            logger_lab.info(str(get_lab_id_result))
            if get_lab_id_result_cnt == 0:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found 0 Entries!"))
            elif get_lab_id_result_cnt == 1:
                return_result["PRINT"].append(color_txt("GREEN",f"Search found 1 Entry!"))
                lab_id = get_lab_id_result[0]['id']
            elif get_lab_id_result_cnt > 1:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found {get_lab_id_result_cnt} Entries! Query should only return 1"))
            else:
                lab_id = None
        else:
            return_result["PRINT"].append(color_txt("RED",f"No id or name selected!"))
            lab_id = None

        if lab_id is not None:
            # ACTION START
            if arg_values.lab_action_command == "start":
                
                return_result["PRINT"].append(color_txt("GREEN",f"LABS action start\nStarting Lab: {lab_id}"))
                get_lab_id_result = client.api.start_lab(lab_id=lab_id)
                get_lab_id_result_cnt = len(get_lab_id_result)
                return_result["RESULTS"] = [client.api.poll_operation(get_lab_id_result)]

            # ACTION STOP
            elif arg_values.lab_action_command == "stop":
                run_command_check = False
                if output_type == 'print':
                    response = pyip.inputYesNo("Do you want to continue? ")
                    if response == 'yes':
                        run_command_check = True
                        print("Continuing...")
                    else:
                        run_command_check = False
                        print("Exiting...")
                if run_command_check == True:
                    
                    return_result["PRINT"].append(color_txt("YELLOW",f"LABS action stop\nStoping Lab: {lab_id}"))
                    get_lab_id_result = client.api.stop_lab(lab_id=lab_id)
                    get_lab_id_result_cnt = len(get_lab_id_result)
                    return_result["RESULTS"] = [client.api.poll_operation(get_lab_id_result)]
            # ACTION DEPLOY
            elif arg_values.lab_action_command == "deploy":
                
                return_result["PRINT"].append(color_txt("GREEN",f"LABS action deploy\nDeploying Lab: {lab_id}"))
                get_lab_id_result = client.api.deploy_lab(lab_id=lab_id)
                get_lab_id_result_cnt = len(get_lab_id_result)
                
                logger_lab.info(str(get_lab_id_result))
                return_result["RESULTS"] = [client.api.poll_operation(get_lab_id_result)]

            # ACTION UNDEPLOY
            elif arg_values.lab_action_command == "undeploy":
                run_command_check = False
                if output_type == 'print':
                    response = pyip.inputYesNo("This will destory any data on the VMs. Do you want to continue?")
                    if response == 'yes':
                        run_command_check = True
                        print("Continuing...")
                    else:
                        run_command_check = False
                        print("Exiting...")
                if run_command_check == True:
                    return_result["PRINT"].append(color_txt("YELLOW",f"LABS action undeploy\nUndeploying Lab: {lab_id}"))
                    get_lab_id_result = client.api.undeploy_lab(lab_id=lab_id)
                    get_lab_id_result_cnt = len(get_lab_id_result)
                    return_result["RESULTS"] = [client.api.poll_operation(get_lab_id_result)]
                
            else:
                return_result["PRINT"].append(color_txt("RED",f"No action selected!"))

    # CREATE

    if arg_values.action_command == 'create':
        logger_lab.info(f"LABS Create")
        
        if arg_values.topo_def is not None and arg_values.lab_name is not None:
            topo_def = arg_values.topo_def
            lab_name = arg_values.lab_name
            if arg_values.lab_description is not None:
                lab_description = arg_values.lab_description
            else:
                lab_description = f"LAB {lab_name}"
            
            return_result["PRINT"].append(color_txt("GREEN",f"Lab name:{lab_name}\nTopology name:{topo_def}\nDescription:{lab_description}"))

            result = client.api.create_lab(
                name=lab_name,
                description=lab_description,
                topo_def=topo_def,
            )
            return_result["RESULTS"] = [client.api.poll_operation(result)]

    # READ
    if arg_values.action_command == 'read':
        #define args:
        lab_id = None
        logger_lab.info(f"LABS Read")
        if "lab_id" in arg_values and arg_values.lab_id is not None:
            lab_id = arg_values.lab_id
        elif "lab_name" in arg_values and arg_values.lab_name is not None:
            return_result["PRINT"].append(color_txt("GREEN",f"Starting search for lab name: {arg_values.lab_name}"))
            get_lab_id_result = client.api.read_labs(name=arg_values.lab_name)
            get_lab_id_result_cnt = len(get_lab_id_result)
            logger_lab.info(str(get_lab_id_result))
            if get_lab_id_result_cnt == 0:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found 0 Entries!"))
            elif get_lab_id_result_cnt == 1:
                return_result["PRINT"].append(color_txt("GREEN",f"Search found 1 Entry!"))
                lab_id = get_lab_id_result[0]['id']
            elif get_lab_id_result_cnt > 1:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found {get_lab_id_result_cnt} Entries! Query should only return 1"))
            else:
                lab_id = None
        else:
            return_result["PRINT"].append(color_txt("RED",f"No id or name selected!"))
            lab_id = None

        if lab_id is not None:
            return_result["PRINT"].append(color_txt("GREEN",f"LABS reading Lab: {lab_id}"))
            get_lab_id_result = [client.api.read_lab(lab_id=lab_id)]
            get_lab_id_result_cnt = len(get_lab_id_result)

            logger_lab.info(str(get_lab_id_result))
            return_result["RESULTS"] = get_lab_id_result

    # UPDATE
    if arg_values.action_command == 'update':
        #define args:
        lab_id_val = None
        lab_found = False
        get_lab_id_result_cnt = 0
        logger_lab.info(f"LABS update")
        
        if "lab_id" in arg_values and arg_values.lab_id is not None:
            logger_lab.info(f"LAB Read lab_id")
            get_lab_id_result = [client.api.read_lab(lab_id=arg_values.lab_id)]
            get_lab_id_result_cnt = len(get_lab_id_result)
            lab_found = True

        elif "lab_name" in arg_values and arg_values.lab_name is not None:
            return_result["PRINT"].append(color_txt("GREEN",f"Starting search for lab name: {arg_values.lab_name}"))
            get_lab_id_result = client.api.read_labs(name=arg_values.lab_name)
            get_lab_id_result_cnt = len(get_lab_id_result)
            lab_found = True
        else:
            return_result["PRINT"].append(color_txt("RED",f"No id or name selected!"))
            lab_id_val = None
        item_selected = False
        if lab_found == True:
            return_result["PRINT"].append(color_txt("YELLOW",f"LAB FOUND ID"))
            logger_lab.info(str(get_lab_id_result))
            if get_lab_id_result_cnt == 0:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found 0 Entries!"))
            elif get_lab_id_result_cnt == 1:
                return_result["PRINT"].append(color_txt("GREEN",f"Search found 1 Entry!"))
                lab_id_val = get_lab_id_result[0]
                item_selected = True
            elif lab_id_val > 1:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found {get_lab_id_result_cnt} Entries! Query should only return 1"))
                lab_id_val = None
            else:
                lab_id_val = None

        if item_selected:
            lab_topology_definition = lab_id_val["topology_definition"]
            lab_description = lab_id_val["description"]
            lab_name = lab_id_val["name"]         
            return_result["PRINT"].append(color_txt("OKBLUE",f"\nPRE UPDATE:\nLab name:{lab_name}\nTopology name:{lab_topology_definition}\nDescription:{lab_description}"))
            
            if arg_values.lab_description is not None: 
                lab_description = arg_values.lab_description
            
            if arg_values.new_lab_name is not None: 
                lab_name = arg_values.new_lab_name
            
            return_result["PRINT"].append(color_txt("CYAN",f"\nPOST UPDATE:\nLab name:{lab_name}\nTopology name:{lab_topology_definition}\nDescription:{lab_description}"))
            result = client.api.update_lab(
                lab_id=lab_id_val["id"],
                name=lab_name,
                description=lab_description
            )
            return_result["RESULTS"] = [client.api.poll_operation(result)]
    
    # DELETE
    if arg_values.action_command == 'delete':
        #define args:
        lab_id = None
        return_result["PRINT"].append(color_txt("GREEN",f"LABS Read"))
        if "lab_id" in arg_values and arg_values.lab_id is not None:
            logger_lab.info(f"LAB Read lab_id")
            get_lab_id_result = [client.api.read_lab(lab_id=arg_values.lab_id)]
            get_lab_id_result_cnt = len(get_lab_id_result)
            lab_found = True

        elif "lab_name" in arg_values and arg_values.lab_name is not None:
            return_result["PRINT"].append(color_txt("GREEN",f"Starting search for lab name: {arg_values.lab_name}"))
            get_lab_id_result = client.api.read_labs(name=arg_values.lab_name)
            get_lab_id_result_cnt = len(get_lab_id_result)
            lab_found = True
        else:
            return_result["PRINT"].append(color_txt("RED",f"No id or name selected!"))
            lab_id_val = None
        item_selected = False
        if lab_found == True:
            return_result["PRINT"].append(color_txt("YELLOW",f"LAB FOUND ID"))
            logger_lab.info(str(get_lab_id_result))
            if get_lab_id_result_cnt == 0:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found 0 Entries!"))
            elif get_lab_id_result_cnt == 1:
                return_result["PRINT"].append(color_txt("GREEN",f"Search found 1 Entry!"))
                lab_id_val = get_lab_id_result[0]
                item_selected = True
            elif lab_id_val > 1:
                return_result["PRINT"].append(color_txt("YELLOW",f"Search found {get_lab_id_result_cnt} Entries! Query should only return 1"))
                lab_id_val = None
            else:
                lab_id_val = None

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
                return_result["PRINT"].append(color_txt("GREEN",f"LABS deleting Lab: {lab_id_val}"))
                get_lab_id_result = client.api.delete_lab(lab_id=lab_id_val["id"])
                get_lab_id_result_cnt = len(get_lab_id_result)
                
                logger_lab.info(str(get_lab_id_result))
                return_result["RESULTS"] = [client.api.poll_operation(get_lab_id_result)]



    #  Disconnect Client
    client_disconnect(client)
    logger_lab.info("Client Disconnect")

    return return_result
