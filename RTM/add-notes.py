#!/usr/bin/env python
# simple app

from rtm import createRTM
import csv

file_name = "list-taskSeries-taskID.csv"
notes = raw_input("What note do you want to add? ")

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
    with open(file_name) as csvfile:
        tasks = csv.reader(csvfile, delimiter=',')
        for i in tasks:
            rspSetName = rtm.tasksNotes.add(timeline= timelineNum, list_id= i[0], taskseries_id= i[1],
            task_id= i[2], note_title= 'API_note', note_text= notes)

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
