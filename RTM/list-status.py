#!/usr/bin/env python
# simple app

from rtm import createRTM
search = 'list:work-subs and status:incomplete'

#removes non-ascii characters
def ascii(text):
    return ''.join(i for i in text if ord(i)<128)

def createApp(rtm):
    rspTasks = rtm.tasks.getList(filter=search)
    # print search
    tasks = []
    if hasattr(rspTasks.tasks, "list") and \
       hasattr(rspTasks.tasks.list, "__getitem__"):
        for l in rspTasks.tasks.list:
            # XXX: taskseries *may* be a list
            if isinstance(l.taskseries, (list, tuple)):
                for t in l.taskseries:
                    tasks.append(t.name)
            else:
                tasks.append(l.taskseries.name)

    if not tasks:
        print False
    else:
        print True

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
