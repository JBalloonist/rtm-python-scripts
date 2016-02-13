#!/usr/bin/env python
# simple app

from rtm import createRTM
#from const import keys

def createApp(rtm, taskName_app):
    # timelineNum = "976642808"
    # used to get a new timelime if necessary
    # timelines never expire so not really necessary to keep getting a new one
    rspTimeline = rtm.timelines.create()
        #print rspTimeline
        #print type(rspTimeline)
    if hasattr(rspTimeline, 'timeline'):
        timelineNum = rspTimeline.timeline
    rspAddTask = rtm.tasks.add(timeline= timelineNum, name= taskName_app,
    parse= "1")

# creates RTM (the API keys and token)
def test(taskName_test, apiKey, secret, token=None):
    rtm = createRTM(apiKey, secret, token)
    # calls createApp
    createApp(rtm, taskName_test)

def main(taskName_main):
    #print taskName_main
    import sys, os
    api_key = os.environ.get('API_KEY', '')
    secret = os.environ.get('SECRET', '')
    token = os.environ.get('TOKEN', '')
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
        test(taskName_main, api_key, secret, token)

if __name__ == '__main__':
    # http://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-args
    main(sys.argv[1])
