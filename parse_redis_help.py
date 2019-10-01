#
# parse the redis command help to show it for the cli
# 
# main link: https://redis.io/commands
# details for every command: example append below
#
#  <li data-group='string' data-name='append'>
#     <a href='/commands/append'>
#     <span class='command'>
#         APPEND
#         <span class='args'>
#         key
#         value
#         </span>
#     </span>
#     <span class='summary'>Append a value to a key</span>
#     </a>
# </li>
 

from bs4 import BeautifulSoup
import requests
import re
import sys
from redmonty.models.tinydb.rediscommand import Rediscommand 
import datetime

r = requests.get("https://redis.io/commands")
soup = BeautifulSoup(r.text, 'html.parser')
#print(soup)
regex = re.compile('.*')
content_lis = soup.find_all('li', attrs={'data-group': regex})
all_commands = {}

for x,li in enumerate(content_lis):
    command_txt_span = li.findChild("span", attrs={"class" : "command"})
    command_txt = str.strip(command_txt_span.find(text=True, recursive=False))
    command_link = li.a.get('href')
    command_args_span = li.findChild("span", attrs={"class" : "args"})
    command_args = command_args_span.find(text=True, recursive=False)
    command_args_list =  [str.strip(x) for x in command_args.split("\n")]
    command_args_list.pop(0)    # remove the first blank.
    command_summary_span = li.findChild("span", attrs={"class" : "summary"})
    command_summary = command_summary_span.find(text=True, recursive=False)
    command_category = li.attrs["data-group"]
    #print(f"{x}: {li.a.get('href')}")
    # print()
    # print(f"{x}: command: {str.strip(command_txt)}")
    # print(f"{x}: command category: {command_category}")
    # print(f"{x}: command link: {command_link}")
    # print(f"{x}: command args: {str.strip(command_args)} ")
    # print(f"{x}: command args(list): {command_args_list} ")
    # print(f"{x}: command summary: {str.strip(command_summary)} ")
    try:
        
        all_commands[command_txt] = {
            "category"  : command_category,
            "help_link" : command_link,
            "args"      : command_args_list,
            "summary"   : command_summary,
            "name"      : command_txt
        }

    except Exception as e:
        print(str(e))
        raise e

for elem in all_commands:
    print(40*"=")
    print(f"Inserting {elem}")
    r = Rediscommand()
    r.init_from_dict(all_commands[elem])
    print(r)
    r.upsert()
    sys.exit()



