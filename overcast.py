# parse Overcast.com HTML file into a list of each podcast
# inserts each podcast name and title to Remember the Milk
import datetime
import time
import copy
import rtm_addtasks

now = datetime.datetime.now()
todays_date = str(now.month) + '-' + str(now.day) + '-' + str(now.year)

html_file = todays_date + '-overcast.html'
computer = " "

txt = open(html_file)

podcast_list = []
title_list = []
time_list = []
rtm_time = []
master_list = []
full_list = []
count = []

# loop through the HTML to only find the titles and time of each podcast episode
# use enumerate so we know the line number to use in the second if statement
for i in enumerate(txt):
    # check for the podcast separator where it lists all the podcasts and stop the loop
    if i[1].startswith('            <h2 class="ocseparatorbar">Podcasts</h2>'):
        break
    # find each row with this string for the podcast name
    if i[1].startswith('                <div class="caption2 singleline">'):
        # get the length of i so we can pull out just the name of the podcast
        if len(i[1]) > 50:
            end = len(i[1]) - 7
            podcast_list.append(i[1][49:end])
    # find each row with this string for the episode title
    if i[1].startswith('                <div class="title singleline">'):
        # get the length of i so we can pull out just the title of the episode
        end = len(i[1]) - 7
        # append the name of the podcast episode
        title_list.append(i[1][46:end])
    # lines with the time start at enumerate 44 (line 48 in the file)
    if (i[0]-3) > 40:
        # find lines that are divisible by 11 (when subtracted by 3)
        # they contain the time data
        if (i[0]-3) % 11 == 0:
            # check if it has remaining in the string
            if 'remaining' in i[1]:
                begin = len(i[1]) - 41
                end_two = len(i[1]) - 33
                # append the time of the episode
            elif '&bull;' not in i[1]:
                begin = len(i[1]) - 16
                end_two = len(i[1]) - 8
            else:
                begin = len(i[1]) - 31
                # append the time of the episode
                end_two = len(i[1]) - 23
            time_list.append(i[1][begin:end_two])

# close the html file
txt.close()

# make a copy of timelist since you cannot loop through a list and edit it
time_list_two = copy.copy(time_list)

# for podcasts without a time add 26 minutes
for i in enumerate(time_list_two):
    if i[1].startswith(' '):
        # removes the original value and inserts 26 minutes
        time_list.pop(i[0])
        time_list.insert(i[0], '00:26:00')

# dictionary for the function below
minutes_per_unit = {"m": 1, "h": 60, "d": 1440, "w": 10080}

# function to convert hours to minutes using the above dict
# found on stack overflow; easy to use since it doesn't require importing a module
# can also use for seconds or any other unit of measurement
def convert_to_minutes(m):
    return int(m[:-1]) * minutes_per_unit[m[-1]]

# go through the time list and update to minutes
for i in time_list:
    minutes = 0
    # check if the hour has a value
    if int(i[1:2]) > 0:
        # convert hour to minutes
        minutes = convert_to_minutes(str(i[1:2]) + "h")
    # check if the seconds are greater than 30 and add a minute
    if int(i[6:8]) > 30:
        minutes = minutes + int(i[3:5]) + 1
    # if the second are less than 30 do not add a minute
    if int(i[6:8]) < 30:
        minutes = minutes + int(i[3:5])
    rtm_time.append(str(minutes) + " minutes")

# create a list of index numbers for today's list
count = range(1, len(podcast_list)+1)

# combine all of the lists into a tuple so each list string is grouped together properly
full_list = zip(count, podcast_list, title_list, rtm_time)

# iterate through the tuple to write each one to a single line
with open(todays_date + '.txt' , 'wb') as out:
    for i in full_list:
        if len(str(i[0])) == 1:
            out.write(str(i[0]) + "    " + i[1] + " - " + i[2] + '\r')
        if len(str(i[0])) == 2:
            out.write(str(i[0]) + "   " + i[1] + " - " + i[2] + '\r')
        if len(str(i[0])) == 3:
            out.write(str(i[0]) + "  " + i[1] + " - " + i[2] + '\r')
        if len(str(i[0])) == 4:
            out.write(str(i[0]) + " " + i[1] + " - " + i[2] + '\r')

# now that the html has been parsed compare the new file with the master file
new_only = []
master_list = []
new_list = []

# open the master-list and today's list and put contents into list
for i in open('master-list.txt', 'U'):
    master_list.append(i)

for g in open(todays_date + '.txt', 'U'):
    new_list.append(g)

# compare today's list with the master list
for i in new_list:
    # slice the first five characters of the string to exclude the number
    if i[5:] not in master_list:
        # now that there are only new podcasts put the time back in
        for l in full_list:
            if int(i[0:5]) == l[0]:
                new_only.append(i[5:] + " =" + l[3].strip('\n'))
                print (i[5:] + " " + l[3])

# add new podcast episodes to the master file
with open('master-list.txt', 'a') as myfile:
    for i in new_only:
        equal_sign = i.index(' =')
        myfile.write(i[:equal_sign])

# print the number of new podcasts that will be added to RTM
print "\n" + str(len(new_only)) + " new podcasts will be added to RTM \n"

# function to remove pound signs so no new tags are added
def remove_pound(text):
    return "".join(g for g in text if g != "#")

# use above function remove the pound sign so stuff doesn't become a tag in RTM
for i in enumerate(new_only):
    new_only.pop(i[0])
    new_only.insert(i[0], remove_pound(i[1]))

# copy the new list so I can compare it and append to it based on what I find
new_only_two = copy.copy(new_only)

for i in enumerate(new_only_two):
    if "NPR" in i[1]:
        new_only.pop(i[0])
        new_only.insert(i[0], i[1] + " #daily ")
    if "Marketplace" in i[1]:
        new_only.pop(i[0])
        new_only.insert(i[0], i[1] + " #daily ")
    if "MacBreak" in i[1]:
        new_only.pop(i[0])
        new_only.insert(i[0], i[1] + " #daily ")
    if "This Week in Tech (MP3)" in i[1]:
        new_only.pop(i[0])
        new_only.insert(i[0], i[1] + " #daily ")
    if "PTI -" in i[1]:
        new_only.pop(i[0])
        new_only.insert(i[0], i[1] + " #daily ")
    if "YNAB" in i[1]:
        new_only.pop(i[0])
        new_only.insert(i[0], i[1] + " #daily ")
    if "Steelers" in i[1]:
        new_only.pop(i[0])
        new_only.insert(i[0], i[1] + " #daily ")
    if "Robot or Not" in i[1]:
        new_only.pop(i[0])
        new_only.insert(i[0], i[1] + " #daily ")
    if "Star Wars Minute" in i[1]:
        new_only.pop(i[0])
        new_only.insert(i[0], i[1] + " #daily ")

# send the new podcasts to RTM

with open('todays-list-' + todays_date + '.txt' , 'wb') as out:
    for i in new_only:
        #out.write(i)
        rtm_addtasks.main(i + " #podcasts ^never")
        #print i
        # give RTM API time to process and update
        # if it goes too fast the same task will get added multiple times
        time.sleep(9.5)
