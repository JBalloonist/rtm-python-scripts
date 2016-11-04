from bs4 import BeautifulSoup
import rtm_addtasks, time
html_doc = open('Tableau 10 Essential Training.html', 'r')
soup = BeautifulSoup(html_doc, 'html.parser')

# conversion dictionary
minutes_per_unit = {"m": 1, "h": 60, "d": 1440, "w": 10080}

def convert_to_minutes(m):
    return int(m[:-1]) * minutes_per_unit[m[-1]]

titles = list()
contents = list()
duration = list()
rtm_time = list()
all_text = list()
full_list = list()

# get the header with the section name
for i in soup.find_all('h4', class_='ga'):
    # print i.get_text()
    titles.append(i.get_text().strip())

# get the video title
for i in soup.find_all('a', class_='item-name video-name ga'):
    # print i.get_text()
    contents.append(i.get_text().strip())

print len(titles)

# get the time of the video
for i in soup.find_all('span', class_='video-duration'):
    # print i.get_text().strip()
    duration.append((i.get_text().strip()).replace('s', ''))

# get all text and match it up with the lists created above
for i in soup.find_all(['h4', 'a']):
    if i.get_text() in titles:
        # print i.get_text().strip()
        all_text.append(i.get_text().strip())
    if i.get_text().strip() in contents:
        # print i.get_text().strip()
        all_text.append(i.get_text().strip())

for i in duration:
    minutes = 0
    if len(i) == 2:
        rtm_time.append('1m')
    # check if the seconds are greater than 30 and add a minute
    if len(i) == 5:
        if int(i[3:5]) > 29:
            rtm_time.append(str(int(i[0])+1) + 'm')
        else:
            rtm_time.append(i[0:2])
    if len(i) == 4:
        rtm_time.append(i[0:2])

combined = zip(contents, rtm_time)

for i in combined:
    pass
    # print i[0], i[1]

print 'Break ------------------'

num_string = ['1','2','3','4','5','6','7','8','9']
count = 0
# loop through all_text and check if it is a heading; if not it has a time
for g,i in enumerate(all_text):
    if i[0] in num_string:
        count = count - 1
        # print i
        full_list.append(i)
    elif i == 'Introduction':
        count = count - 1
        # print i
        full_list.append(i)
    elif i == 'Conclusion':
        count = count - 1
        # print i
    else:
        # print g, i, rtm_time[g + count]
        full_list.append(i + ' =' + rtm_time[g + count])

for i in full_list:
    print i

"""
with open('lynda.txt', 'w') as f:
    for i in full_list:
        rtm_addtasks.main(i)
        f.write(i)
        f.write('\n')
        time.sleep(9.5)
"""