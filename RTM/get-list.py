#!/usr/bin/env python
# simple app

from rtm import createRTM
search = raw_input("What is the search you want to run? ")
file_name = raw_input("What should the file name be? ")

def createApp(rtm):
    rspTasks = rtm.tasks.getList(filter=search)
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
    with open(file_name + '.txt', 'wb') as out:
        for i in tasks:
            print i
            out.write(i  + "\r")
    if not tasks:
        tasks.append('No tasks due within a week')

# creates RTM (the API keys and token)
def test(apiKey, secret, token=None):
    rtm = createRTM(apiKey, secret, token)
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
        test(api_key, secret, token)

if __name__ == '__main__':
    main()
