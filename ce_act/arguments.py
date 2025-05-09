
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
import argparse
import argcomplete
from ce_act.constants import *

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description=setup_text,
        formatter_class=argparse.RawDescriptionHelpFormatter ,
    )
    # Main Menu
    parser.add_argument("--debug", help="Start Debugging",action="store",default=None, 
                        choices=['CRITICAL', 'DEBUG','INFO','WARNING','DEBUG_APP','DEBUG_REMOTE','NONE'])
    parser.add_argument(
        "--api_key", 
        required=False, 
        action="store",
        help="CE ACT APIKEY to Use", 
        default="None"
    )
    parser.add_argument(
        "--base_url", 
        dest="base_url", 
        required=False, 
        action="store", 
        help="Tenant base URL",
        default="https://ce.act.arista.com"
    )
    parser.add_argument(
        "--logging", 
        action="store_true", 
        help="Enable logging",
        default=False,
        
    )
    parser.add_argument('--log', default='WARNING', 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level')
    parser.add_argument(
        "-o",
        "--output", 
        default="print", 
        help='Output format',
        choices=['json','yaml','print']
        
    )

    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument('-o','--output', required=False,
                        type=str,  help='Output Format',choices=['json','yaml','print'])   
    output_parser.add_argument('-l','--limit', required=False,
                        type=int,  help='Output Limit results')
    output_parser.add_argument('--sort_desc', required=False,action="store_true",
                        help='Output sorted type Descending results', default=False)   


    # Root Services
    service_subparsers = parser.add_subparsers(title="service",dest="service_command")

    # LABS Service Commands
    list_output_parser = argparse.ArgumentParser(add_help=False)
    list_output_parser.add_argument('-s','--sort_type', required=False,
                        type=str,  help='Output sorted type results', default='name',choices=['name','user','description','created_at','updated_at','schema_version','state','stage','topology_definition'])   

    labs_parser = service_subparsers.add_parser("labs", help="CE ACT Labs Configuration API")
    labs_action_subparser = labs_parser.add_subparsers(title="action", dest="action_command")
    # Filtered parser for command:
    lab_id_parser = argparse.ArgumentParser(add_help=False)
    lab_id_parser.add_argument('-n','--lab_name',type=str, help='Lab Name')   
    lab_id_parser.add_argument('-i','--lab_id',type=str, help='Lab id')   

    labs_list_parser = argparse.ArgumentParser(add_help=False)
    labs_list_parser.add_argument('-n','--lab_name',type=str, help='Lab Name',)   
    labs_list_parser.add_argument('-u','--user_name',type=str, help='User Name')   

    lab_create_parser = argparse.ArgumentParser(add_help=False)
    lab_create_parser.add_argument('-n','--lab_name',type=str, help='Lab Name',required=True)   
    lab_create_parser.add_argument('-t','--topo_def',type=str, help='Lab Topology definition ',required=True)   
    lab_create_parser.add_argument('-d','--lab_description',type=str, help='Lab Description')   

    lab_update_parser = argparse.ArgumentParser(add_help=False)
    lab_update_parser.add_argument('-i','--lab_id',type=str, help='Lab id')   
    lab_update_parser.add_argument('-n','--lab_name',type=str, help='Lab Name')      
    lab_update_parser.add_argument('--new_lab_name',type=str, help='New Lab Name')      
    lab_update_parser.add_argument('-d','--lab_description',type=str, help='Lab Description')   

    # sub commands for LABS
    labs_action_subparser.add_parser("create", help="Create Lab",parents=[lab_create_parser])
    labs_action_subparser.add_parser("read",   help="Read Lab",parents=[lab_id_parser,output_parser,list_output_parser])
    labs_action_subparser.add_parser("update", help="Update Lab",parents=[lab_update_parser])
    labs_action_subparser.add_parser("delete", help="Delete Lab",parents=[lab_id_parser,output_parser,list_output_parser])
    #labs_action_subparser.add_parser("list", help="list Labs")
    
    # sub sub action command for lab
    labs_action_action_parser = labs_action_subparser.add_parser("action", help="CE ACT Labs Action")
    labs_action_action_subparser = labs_action_action_parser.add_subparsers(title="action",
                    dest="lab_action_command")
    labs_action_action_subparser.add_parser("start", help="Start Lab",parents=[lab_id_parser,output_parser,list_output_parser])
    labs_action_action_subparser.add_parser("stop", help="Stop Lab",parents=[lab_id_parser,output_parser,list_output_parser])
    labs_action_action_subparser.add_parser("deploy", help="Deploy Lab",parents=[lab_id_parser,output_parser,list_output_parser])
    labs_action_action_subparser.add_parser("undeploy", help="Undeploy Lab",parents=[lab_id_parser,output_parser,list_output_parser])

    # sub sub action command for topo list
    labs_action_list_parser = labs_action_subparser.add_parser("list", help="CE ACT Topology list")
    labs_action_list_subparser = labs_action_list_parser.add_subparsers(title="action",
                    dest="labs_list_command")
    labs_action_list_subparser.add_parser("search", help="Search Labs",parents=[labs_list_parser,output_parser,list_output_parser])
    labs_action_list_subparser.add_parser("all", help="All Labs",parents=[labs_list_parser,output_parser,list_output_parser])


    # Topology Service Commands

    topo_output_parser = argparse.ArgumentParser(add_help=False)
    topo_output_parser.add_argument('-s','--sort_type', required=False,
                        type=str,  help='Output sorted type results', default='name',choices=['name','created_by','modified_by','description','topology_pathname','diagram_pathname','device_count','ref_count','version'])   
    topo_parser = service_subparsers.add_parser("topology", help="CE ACT Topology Configuration API")
    topo_action_subparser = topo_parser.add_subparsers(title="action", dest="action_command")
    # Filtered parser for command:
    topo_id_parser = argparse.ArgumentParser(add_help=False)
    topo_id_parser.add_argument('-i','--topo_id',type=str, help='Topo id')
    topo_id_parser.add_argument('-n','--topo_name',type=str, help='Topo Name')
    topo_id_parser.add_argument('-t','--topo_def',type=str, help='Topology Definition') 
    #topo_id_parser.add_argument('-u','--user_name',type=str, help='User Name')   

    topo_list_parser = argparse.ArgumentParser(add_help=False)
    #topo_id_parser.add_argument('-c','--search ',type=str, help='Lab id')
    topo_list_parser.add_argument('-n','--topo_name',type=str, help='Topo Name')   
    topo_list_parser.add_argument('-u','--user_name',type=str, help='User Name') 

    topo_create_parser = argparse.ArgumentParser(add_help=False)
    topo_create_parser.add_argument('-n','--topo_name',type=str, help='Topo Name')   
    topo_create_parser.add_argument('-t','--topo_def',type=str, help='Topology definition ')   
    topo_create_parser.add_argument('-d','--topo_description',type=str, help='Topo Description')
    topo_create_parser.add_argument('-g','--topo_image',type=str, help='Topo image')   

    topo_update_parser = argparse.ArgumentParser(add_help=False)
    topo_update_parser.add_argument('-i','--topo_id',type=str, help='Topo id')
    topo_update_parser.add_argument('-n','--topo_name',type=str, help='Topo Name')
    topo_update_parser.add_argument('--new_topo_name',type=str, help='New Topo Name')       
    topo_update_parser.add_argument('-t','--topo_def',type=str, help='Topology definition ')   
    topo_update_parser.add_argument('-d','--topo_description',type=str, help='Topo Description')
    topo_update_parser.add_argument('-g','--topo_image',type=str, help='Topo image')   


    # sub commands for LABS
    topo_action_subparser.add_parser("create", help="Create Topology",parents=[topo_create_parser])
    topo_action_subparser.add_parser("read",   help="Read Topology",parents=[topo_id_parser,output_parser,topo_output_parser])
    topo_action_subparser.add_parser("update", help="Update Topology",parents=[topo_update_parser])
    topo_action_subparser.add_parser("delete", help="Delete Topology",parents=[topo_id_parser,output_parser,topo_output_parser])
    #topo_action_subparser.add_parser("list", help="list Topology")
    
    # sub sub action command for topo get
    topo_action_get_parser = topo_action_subparser.add_parser("get", help="CE ACT Topology models")
    topo_action_get_subparser = topo_action_get_parser.add_subparsers(title="action",dest="topo_get_command")
    topo_action_get_subparser.add_parser("nodes", help="Get Nodes")
    #topo_action_get_subparser.add_parser("device_models", help="Get Device Models")
    # sub sub action command for topo list
    topo_action_list_parser = topo_action_subparser.add_parser("list", help="CE ACT Topology list")
    topo_action_list_subparser = topo_action_list_parser.add_subparsers(title="action",
                    dest="topo_list_command")
    topo_action_list_subparser.add_parser("search", help="Search for Topologies",parents=[topo_list_parser,output_parser,topo_output_parser])
    topo_action_list_subparser.add_parser("all", help="All Topologies",parents=[topo_list_parser,output_parser,topo_output_parser])

    argcomplete.autocomplete(parser)
    #return parser.parse_args()
    return parser
