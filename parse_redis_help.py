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
#from models.tinydb.rediscommand import Rediscommand 

BASE_URL = "https://redis.io/commands"

def get_command_help(url):
    """
        get the detailed command help from the deep link
        info is in <div class="article-main">
    """
    url = "https://redis.io" + url
    r = requests.get(url)
    print(f"opening: {url}")
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find("div", attrs={'class': "article-main"})
    return str(content)



r = requests.get(BASE_URL)
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
    del command_args_list[-1]   # remove the last blank
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
            "category"  : str(command_category),
            "help_link" : str(command_link),
            "args"      : command_args_list,
            "summary"   : str(command_summary),
            "name"      : str(command_txt),
            "help_text" : get_command_help(str(command_link))
        }

    except Exception as e:
        print(str(e))
        raise e

import json
with open('redis_help.json', 'w') as fp:
    json.dump(all_commands, fp)

#for elem in all_commands:
#    print(40*"=")
#    print(f"Inserting {elem}")
#    r = Rediscommand()
#    r.init_from_dict(all_commands[elem])
#    print(r)
#    #what = input("upsert or skip ... (u|s)")
#    #if what == "u":
#    #    r.upsert()
#    #else:
#    #    pass
#    r.upsert()


