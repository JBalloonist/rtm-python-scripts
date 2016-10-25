#!/usr/bin/env python
# simple app

from rtm import createRTM
import csv, time

file_name = 'work.csv'

def timer(run):
    # run = raw_input("Start? > ")
    mins = 0
    total_mins = int(raw_input("How many minutes have you already worked on this task? "))
    # Only run if the user types in "start"
    if run == "start":
        # Loop until we reach 25 minutes running
        while mins != 25:
            print ">>>>>>>>>>>>>>>>>>>>>", mins
            # Sleep for a minute
            time.sleep(60)
            # Increment the minute total
            mins += 1
            # Bring up the dialog box here
    return str(mins + total_mins) + 'm'

def user_select():
    with open(file_name) as csvfile:
        tasks = csv.reader(csvfile, delimiter=',')
        for n, i in enumerate(tasks, start=1):
            print (n,': ' + i[3])
        index = int(raw_input("Choose which task you want to work on "))
        return index

def createApp(rtm):
    task_num = user_select()
    rspTimeline = rtm.timelines.create()
    if hasattr(rspTimeline, 'timeline'):
        timelineNum = rspTimeline.timeline
    with open(file_name) as csvfile:
        tasks = csv.reader(csvfile, delimiter=',')
        for n, i in enumerate(tasks, start=1):
            if task_num == n:
                rtm.tasks.setEstimate(timeline= timelineNum, list_id= i[0], taskseries_id= i[1],
                task_id= i[2], estimate= timer('start'))

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