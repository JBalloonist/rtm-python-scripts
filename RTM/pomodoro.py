#!/usr/bin/env python
# pomodoro timer that adds time to the RTM task I select

# from rtm import createRTM
from rtm_json import createRTM
from sys import argv
import csv, time, json

script, run_search = argv
print script
print run_search
if run_search == 'yes':
    print
    search = raw_input("What is the search you want to run? ")

file_name = 'work'

def ascii_only(text):
    return ''.join(i for i in text if ord(i)<128)

def parseJson(file):
    data = open(file, 'r')
    parsed_json = json.load(data)
    tasks = parsed_json['rsp']['tasks']['list']
    ids_list = list()
    for i in tasks:
        if isinstance(i['taskseries'], list):
            for n in i['taskseries']:
                add = list() # recreates the list each time
                add.append(i['id']) # list ID
                add.append(n['id']) # taskseries ID
                add.append(n['task']['id']) # task ID
                add.append(ascii_only(n['name'])) # task name
                add.append(n['task']['added']) # created date and time
                add.append(n['task']['completed'])
                add.append(n['task']['estimate'])
                ids_list.append(add)
        if isinstance(i['taskseries'], dict):
            for n in i['taskseries']:
                add = list() # recreates the list each time
                print (i['id']) # list ID
                print (n['id']) # taskseries ID
                print (n['task']['id']) # task ID
                print (ascii_only(n['name'])) # task name
                print (n['task']['added']) # created date and time
                print (n['task']['completed'])
                print (n['task']['estimate'])
                add.append(i['id']) # list ID
                add.append(n['id']) # taskseries ID
                add.append(n['task']['id']) # task ID
                add.append(ascii_only(n['name'])) # task name
                add.append(n['task']['added']) # created date and time
                add.append(n['task']['completed'])
                add.append(n['task']['estimate'])
                ids_list.append(add)

    with open(file_name + '.csv', 'wb') as f:
        writer = csv.writer(f)
        for i in ids_list:
            writer.writerow(i)

def timer(run):
    mins = 0
    total_mins = int(raw_input("How many minutes have you already worked on this task? "))
    if run == "start":
        # Loop until we reach 25 minutes running
        while mins != 25:
            print ">>>>>>>>>>>>>>>>>>>>>", mins
            # Sleep for a minute
            time.sleep(60)
            # Increment the minute total
            mins += 1
            # Bring up the dialog box here
    return mins + total_mins

def user_select():
    with open(file_name + '.csv') as csvfile:
        tasks = csv.reader(csvfile, delimiter=',')
        for n, i in enumerate(tasks, start=1):
            print (n,': ' + i[3])
        index = int(raw_input("Choose which task you want to work on "))
        return index

def createApp(rtm):
    global run_search
    if run_search == 'yes':
        rspTasks = rtm.tasks.getList(filter=search)
        with open(file_name + '.json', 'wb') as out:
            for i in rspTasks:
                out.write(i)
    parseJson(file_name + '.json')
    task_num = user_select()
    # timelines never expire
    #just hardcoding one instead of getting new one every time
    timelineNum = '1053897822'
    with open(file_name + '.csv') as csvfile:
        tasks = csv.reader(csvfile, delimiter=',')
        for n, i in enumerate(tasks, start=1):
            if task_num == n:
                total_time = timer('start')
                rtm.tasks.setEstimate(timeline= timelineNum, list_id= i[0], taskseries_id= i[1],
                task_id= i[2], estimate= str(total_time) + 'm')
                rtm.tasksNotes.add(timeline= timelineNum, list_id= i[0], taskseries_id= i[1],
                task_id= i[2], note_title= 'API_note', note_text= 'pomodoro ' + str(total_time/25))

# creates RTM (the API keys and token)
def test(apiKey, secret, token=None):
    rtm = createRTM(apiKey, secret, token)
    # calls createApp
    createApp(rtm)

def main():
    from ConfigParser import SafeConfigParser
    import sys
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
        # calls test
        test(api_key, secret, token)

if __name__ == '__main__':
    main()