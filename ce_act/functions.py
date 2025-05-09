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


import os
import json
import pprint
pp = pprint.PrettyPrinter(indent=2)

from ce_act.config import *

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import Terminal256Formatter

from actrac.client import ACTClient

bcolors = {
    'RED'       : '\033[0;31m',
    'HEADER'    : '\033[95m',
    'OKBLUE'    : '\033[94m',
    'YELLOW'    : '\033[0;33m',
    'BLACK'     : '0',
    'CYAN'      : '\033[96m',
    'GREEN'     : '\033[92m',
    'WARNING'   : '\033[93m',
    'FAIL'      : '\033[91m',
    'NC'        : '\033[0m',
    'BOLD'      : '\033[1m',
    'UNDERLINE' : '\033[4m'
}

def color_txt(color,text):
    return f"{bcolors[color]}{text}{bcolors['NC']}"


app__file__ = __file__
app_basename = os.path.basename(app__file__).split(".")[0]

def color_json(json_str):
    parsed = json.loads(json_str)
    formatted = json.dumps(parsed, indent=2)
    return highlight(formatted, JsonLexer(), Terminal256Formatter())



def client_connect(api_key, base_url, debug=False, log_stdout=True):


    try:
        client = ACTClient(api_key=api_key, base_url=base_url, log_stdout=log_stdout)
    except ACTClient.RequestError as e:
        print(f"An error occurred while requesting: {e}")
    except ACTClient.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    
    root_logger.info("INSTANTIATE CLIENT")
    client.connect()
    root_logger.info("CONNECTED")

    return client

def client_disconnect(conn,debug=False):
    root_logger.info("DISCONNECT CLIENT")
    conn.disconnect()
    root_logger.info("LOGGED OUT")

def print_found(count,text=None):
    print_string = color_txt("GREEN",f"Found ")
    print_string += color_txt("YELLOW",f"{count} ")
    if text is not None:
        print_string += color_txt("GREEN",f"{text}")
    return print_string
