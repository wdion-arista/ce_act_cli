#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# 
#
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
#
# Author: Westley Dion
# Date: 2025-MAR-25
# Usage:
#    ce_act -h
# Autocomplete run:
#   activate-global-python-argcomplete

import logging
import sys
import json, yaml

import pprint
pp = pprint.PrettyPrinter(indent=2)

import httpx
from ce_act.constants import *
from ce_act.config import *
from ce_act.service.labs import *
from ce_act.service.topology import *
from ce_act.arguments import *

def main():
    """Begin example of ACT REST API Client Lab Functions."""
    return_result = {
        "ERROR":[],
        "PRINT":[],
        "CODE":200,
        "RESULTS":[]
    }

    api_parser = parse_args()
    args = api_parser.parse_args()

    if len(sys.argv)==1:
        api_parser.print_help(sys.stderr)
        sys.exit(1)

    if args.debug is not None:
        print(color_txt("YELLOW",f"DEBUG ON LEVEL: {args.debug}"))
        if args.debug == "NONE":
            debug = False
        else:
            debug = True
    else:
        debug = False

    # Set output type
    if args.output is not None:
        output_type = args.output
    else:
        output_type = "print"
    
    root_logger.info(pp.pformat(args))

    # Check for api key
    if act_apikey is not None:
        api_key = act_apikey
    elif args.api_key is not None:
        api_key = args.api_key
    else:
        # do Menu again
        print(color_txt("RED",f"No ENV or API key found use -h flag to get options"))
        sys.exit(1)
    root_logger.setLevel(args.log)
    logging.basicConfig(level=args.log, format='%(levelname)s: %(message)s')
    
    
    
    root_logger.debug("This is a debug message *******")
        
    return_result["PRINT"].append(color_txt("GREEN",f"-== CE ACT CLI ==-"))
    # Main Menu Selection
    return_response = None
    try:
        if args.service_command == "labs" and args.action_command is not None:
            return_response = labs_commands(api_key,args,output_type = output_type,debug=debug)
        elif args.service_command == "topology" and args.action_command is not None:
            return_response = topology_commands(api_key,args,output_type = output_type,debug=debug)
        else:
            print({"ERROR":"Bad Mojo Command messed up."})
            exit(1)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            root_logger.critical(f"Authentication failed: {e}")
            # Handle the 401 Unauthorized error (e.g., prompt for new credentials)
        else:
            print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"An error occurred while making the request: {e}")
    except AttributeError as e:
        print(f"Attribute error occurred: {e}")
        # Handle the AttributeError (e.g., check if 'client' is properly initialized)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    if return_response is not None and "CODE" in return_response:
        return_result["ERROR"] += return_response["ERROR"]
        return_result["PRINT"] += return_response["PRINT"]
        return_result["CODE"] += return_response["CODE"]
        return_result["RESULTS"] += return_response["RESULTS"]

    if output_type == "print":
        json_str = json.dumps(return_result["RESULTS"])
        print(color_json(json_str))
        if len(return_result["ERROR"]) > 0:
            print("\n".join(return_result["ERROR"]))
        print("\n".join(return_result["PRINT"]))
        
        
    elif output_type == "json":
        
        root_logger.info(json.dumps(dict(return_result), indent=1))
        print(json.dumps(return_result["RESULTS"], indent=1))
    elif output_type == "yaml":
        root_logger.info(yaml.dump(return_result, default_flow_style=False))
        yaml_ouptut = yaml.dump(return_result["RESULTS"], default_flow_style=False)
        print(yaml_ouptut)
    
    
    root_logger.info("DONE\n")
        


if __name__ == "__main__":
    main()
