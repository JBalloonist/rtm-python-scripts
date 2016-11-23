#!/usr/bin/env python

# from rtm_json import createRTM
from rtm_json import createRTM
import json, csv
file_name = 'evernote'
search = 'source:evernote and NOT priority:1'

def ascii_only(text):
    return ''.join(i for i in text if ord(i)<128)

def parseJson(file):
    data = open(file + '.json', 'r')
    parsed_json = json.load(data)
    print type(parsed_json['rsp']['tasks'])
    tasks = parsed_json['rsp']['tasks']['list']
    ids_list = list()
    for i in tasks:
        if isinstance(i['taskseries'], list):
            for n in i['taskseries']:
                add = list() # recreates the list each time
                # if not repeating, will be a dict
                if isinstance(n['task'], dict):
                    add.append(i['id']) # list ID
                    add.append(n['id']) # taskseries ID
                    add.append(n['task']['id']) # task ID
                    add.append(ascii_only(n['name'])) # task name
                    add.append(n['task']['added']) # created date and time
                    add.append(n['task']['completed'])
                    add.append(n['task']['estimate'])
                    add.append(n['task']['due']) # due date
                    ids_list.append(add)
                else:
                    for g in n['task']:
                        add = list() # recreates the list each time
                        add.append('In a list: ')
                        add.append(i['id']) # list ID
                        add.append(n['id']) # taskseries ID
                        add.append(g['id']) # task id for repeating tasks
                        add.append(ascii_only(n['name'])) # task name
                        add.append(g['added'])
                        add.append(g['completed'])
                        add.append(g['estimate'])
                        add.append(g['due'])
                        ids_list.append(add)
        if isinstance(i['taskseries'], dict):
            add = list() # recreates the list each time
            add.append(i['id']) # list ID
            add.append(i['taskseries']['id']) # taskseries ID
            add.append(i['taskseries']['task']['id']) # task ID
            add.append(ascii_only(i['taskseries']['name'])) # task name
            add.append(i['taskseries']['task']['added']) # created date and time
            add.append(i['taskseries']['task']['completed']) # created date and time
            add.append(i['taskseries']['task']['estimate'])
            add.append(i['taskseries']['task']['due'])
            ids_list.append(add)

    with open(file_name + '.csv', 'wb') as f:
        writer = csv.writer(f)
        for i in ids_list:
            print i
            writer.writerow(i)

def createApp(rtm):
    rspTasks = rtm.tasks.getList(filter=search)
    with open(file_name + '.json', 'wb') as out:
        for i in rspTasks:
            out.write(i)

    parseJson(file_name)

    with open(file_name + '.csv', 'r') as csvfile:
        tasks = csv.reader(csvfile, delimiter = ',')
        for i in tasks:
            rtm.tasks.setPriority(timeline = '1053897822', list_id = i[0],
            taskseries_id = i[1], task_id = i[2], priority = '1')

# creates RTM (the API keys and token)
def test(apiKey, secret, token=None):
    rtm = createRTM(apiKey, secret, token)
    createApp(rtm)

def main():
    import sys
    from ConfigParser import SafeConfigParser
    parser = SafeConfigParser()
    parser.read('simple.ini')
    api_key = parser.get('API', 'api_key')
    secret = parser.get('API', 'secret')
    token = parser.get('API', 'token')
    try:
        api_key, secret
    except ValueError:
        sys.stderr.write('Usage: rtm_appsample APIKEY SECRET [TOKEN]\n')
    else:
        try:
            token
        except IndexError:
            token = None
        test(api_key, secret, token)

if __name__ == '__main__':
    main()

