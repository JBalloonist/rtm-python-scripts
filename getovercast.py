import requests
import datetime
from const import payload # contains username and login info

LOGIN_URL = 'https://overcast.fm/login'
OVERCAST = 'https://overcast.fm/podcasts'
now = datetime.datetime.now()
todays_date = str(now.month) + '-' + str(now.day) + '-' + str(now.year)

def remove_non_ascii_1(text):
    return ''.join(i for i in text if ord(i)<128)

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post(LOGIN_URL, data=payload)
    f = open(todays_date + '-overcast.html', 'wb')
    f.write(remove_non_ascii_1(p.text))
    # the login page seems to automatically redirect to the podcasts page
    # therefore the below is not necessary

html_file = todays_date + '-overcast.html'