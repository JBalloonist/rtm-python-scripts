#!/usr/bin/env python
# simple app

# using dotted dict in order to get the timeline
from rtm import createRTM
import csv, datetime
file_name = 'list-taskSeries-taskID.csv'

def createApp(rtm):
    rspTimeline = rtm.timelines.create()
    # print rspTimeline
    now = datetime.datetime.now()
    start_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day+3)
    if hasattr(rspTimeline, 'timeline'):
        timelineNum = rspTimeline.timeline
    date_add = 3
    with open(file_name) as csvfile:
        tasks = csv.reader(csvfile, delimiter=',')
        for i in tasks:
            rspSetStart = rtm.tasks.setStartDate(timeline= timelineNum,
            list_id= i[0],taskseries_id= i[1], task_id= i[2],start=start_date, parse= 1)
            date_add = date_add + 1
            print date_add
            start_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day+date_add)

# creates RTM (the API keys and token)
def test(apiKey, secret, token=None):
    rtm = createRTM(apiKey, secret, token)
    # call createApp and send above as arguments
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
