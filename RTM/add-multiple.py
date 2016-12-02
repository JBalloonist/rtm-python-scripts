#!/usr/bin/env python
# script to add multiple tasks to RTM
# can add as a parent task or as a subtask

from rtm import createRTM
import time, csv

# Get input from the user on the settings of the import
file_name = raw_input("What is the name of the file with the list of tasks? ")
parent = raw_input("Are these tasks being assigned to a parent task? Type yes or no: ")
parse_status = raw_input("Should RTM Smart Add be used? Type YES or NO. ")

if parse_status == "yes":
    parse_id = str(1)
else:
    parse_id = str(0)

parent_ids = []
with open('work.csv') as csvfile:
    ids = csv.reader(csvfile, delimiter= ',')
    for i in ids:
        print i[2]
        parent_ids.append(str(i[2]))

# parent_ids = [x.strip('\n') for x in parent_ids]

print parent_ids

def createApp(rtm):
    global parent
    global parent_ids
    # used to get a new timelime if necessary
    # timelines never expire so not really necessary to keep getting a new one
    rspTimeline = rtm.timelines.create()
        #print rspTimeline
        #print type(rspTimeline)
    if hasattr(rspTimeline, 'timeline'):
        timelineNum = rspTimeline.timeline
    if parent == "yes":
        with open(file_name) as tasks:
            for f in tasks:
                print f
                for i in parent_ids:
                    print i
                    rtm.tasks.add(timeline= timelineNum, name= f, parse= parse_id, parent_task_id= i)
                    time.sleep(9.7)
    else:
        with open(file_name) as tasks:
            for f in tasks:
                print f
                rtm.tasks.add(timeline= timelineNum, name= f,
                    parse= parse_id)
                time.sleep(9.5)

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
