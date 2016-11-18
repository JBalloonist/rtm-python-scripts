#!/usr/bin/env python
# pomodoro timer that adds time to the RTM task I select

# from rtm import createRTM
from rtm_json import createRTM
import csv, time, json, datetime

now = datetime.datetime.now()
todays_date = str(now.month) + '-' + str(now.day) + '-' + str(now.year)

searches = ['custom search',
            'list:Work-week and status:incomplete',
            'list:work-week and priority:1 and status:incomplete',
            'list:Work-week and due:tod and status:incomplete',
            'list:work-Projects and status:incomplete',
            'list:work-Projects priority:1 and status:incomplete',]

# lists for the hardcoded
take_break = ['36712370','306248407','525099979','Take a break from working on ']
break_over = ['36712370','306248422','525100002', 'Your break is over, get back to work!']

for n, i in enumerate(searches):
    print (str(n) + ': ' + i)
print " "

ind = int(raw_input('Which search would you like to run?\nEnter zero if you would like to enter your own search: '))
for n, i in enumerate(searches):
    if ind > 0:
        if n == ind:
            search = i
            break
    else:
        search = raw_input('Enter your search: ')
        break

run_search = 'yes'
# search = 'list:work and (due:tod OR priority:1)'
file_name = 'work'

# sends detail of the task worked on to a master file for the month
def all_pom(text_one, text_two):
    tracking_list = list()
    pom_list = list()
    now = datetime.datetime.now()
    tracking_list.append(now.isoformat())
    tracking_list.append(text_one)
    tracking_list.append(text_two)
    pom_list.append(tracking_list)
    tracking_file = '/home/JBalloonist/RTM/pomodoro/' + now.strftime('%B') + '-tracking.csv'

    with open(tracking_file, 'a') as f:
        writer = csv.writer(f)
        for i in pom_list:
            writer.writerow(i)

# function to get the time already spent on a task
def add_time(time):
    time_all = list()
    for i in time:
        # print i
        if 'minutes' in i:
            if 'hour' in i:
                time_all.append(int(i[0:1])*60)
                time_all.append(int(i[8:10]))
            else:
                ending = len(i) - 8
                time_all.append(int(i[0:ending]))
        else:
            if 'H' in i:
                if len(i) == 4:
                    time_all.append(int(i[2:3])*60)
                if len(i) == 5:
                    time_all.append(int(i[2:4])*60)
                if len(i) == 6:
                    time_all.append(int(i[2:3])*60)
                    time_all.append(int(i[4:5]))
                if len(i) == 7:
                    time_all.append(int(i[2:3])*60)
                    time_all.append(int(i[4:6]))
            if i.endswith('m'):
                # print i.replace('m', "")
                time_all.append(int(i.replace('m', "")))
            if 'M' in i:
                if len(i) == 4:
                    time_all.append(int(i[2:3]))
                if len(i) == 5:
                    time_all.append(int(i[2:4]))
    return sum(time_all)

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
                add.append(n['task']['due']) # due date
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
    if run == "start":
        # Loop until we reach 25 minutes running
        while mins != 25:
            print ">>>>>>>>>>>>>>>>>>>>>", mins
            # Sleep for a minute
            time.sleep(60)
            # Increment the minute total
            mins += 1
            # Bring up the dialog box here
    print ">>>>>>>>>>>>>>>>>>>>>", mins
    return mins

def user_select():
    with open(file_name + '.csv') as csvfile:
        tasks = csv.reader(csvfile, delimiter=',')
        for n, i in enumerate(tasks, start=1):
            print (str(n) + ': ' + i[3])
        # print '\n'
        print " "
        index = int(raw_input("Choose which task you want to work on: "))
        return index

def pom_count():
    now = datetime.datetime.now()
    tracking_file = '/home/JBalloonist/RTM/pomodoro/' + now.strftime('%B') + '-tracking.csv'
    with open(tracking_file) as csvfile:
        tasks = csv.reader(csvfile, delimiter=',')
        counter = 0
        for i in tasks:
            if i[0][0:10] == now.isoformat()[0:10]:
                counter = counter + 1
        return counter

def createApp(rtm):
    global run_search
    print search
    if run_search == 'yes':
        rspTasks = rtm.tasks.getList(filter=search)
        with open(file_name + '.json', 'wb') as out:
            for i in rspTasks:
                out.write(i)
    parseJson(file_name + '.json')
    task_num = user_select()
    minutes = list()
    # timelines never expire
    #just hardcoding one instead of getting new one every time
    timelineNum = '1053897822'
    now = datetime.datetime.now()
    pom_end = (now + (datetime.timedelta(minutes=26))).isoformat()

    with open(file_name + '.csv') as csvfile:
        tasks = csv.reader(csvfile, delimiter=',')
        for n, i in enumerate(tasks, start=1):
            if task_num == n:
                # set the due date of the take a break task
                rtm.tasks.setDueDate(timeline= timelineNum, list_id= '10509737',
                taskseries_id= '306248407', task_id= '525099979', due=pom_end,
                has_due_time='1', parse='0')

                # change the name of the break task reminder
                rtm.tasks.setName(timeline= timelineNum, list_id= '10509737',
                taskseries_id= '306248407', task_id= '525099979',
                name= (take_break[3] + '- ' + i[3]))

                minutes.append(i[6])
                if add_time(minutes) == 0:
                    rtm.tasksNotes.add(timeline= timelineNum, list_id= i[0],
                    taskseries_id= i[1],task_id= i[2], note_title='Original Due Date', note_text=i[7])

                print add_time(minutes)
                print 'Existing time: ' + str(add_time(minutes) / 60) + ' hours ' + str(add_time(minutes) % 60) + ' minutes'

                total_time = timer('start') + add_time(minutes)
                print 'Total time: ' + str(total_time / 60) + ' hours ' + str(total_time % 60) + ' minutes'

                rtm.tasks.setEstimate(timeline= timelineNum, list_id= i[0], taskseries_id= i[1],
                task_id= i[2], estimate= str(total_time) + 'm')

                all_pom(i[3], 'pomodoro ' + str(total_time/25))

    break_status = pom_count()
    if break_status % 4 == 0:
        print 'Time to take a longer break!'
        break_end_time = (now + (datetime.timedelta(minutes=41))).isoformat()
    else:
        print 'Sorry, you only get a five minute break this time.'
        break_end_time = (now + (datetime.timedelta(minutes=31))).isoformat()

    rtm.tasks.setDueDate(timeline= timelineNum, list_id= '10509737',
    taskseries_id= '306248422', task_id= '525100002', due=break_end_time,
    has_due_time='1', parse='0')

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