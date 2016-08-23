#!/usr/bin/env python
# simple app

from rtm import createRTM

def createApp(rtm):
    rspTasks = rtm.tasks.getList(filter='list:added')
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
        tasks.append('No tasks found')
    print(tasks)

def test(apiKey, secret, token=None):
    rtm = createRTM(apiKey, secret, token)
    createApp(rtm)

def main():
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
        test(api_key, secret, token)

if __name__ == '__main__':
    main()