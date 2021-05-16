from datetime import date
import os
import random
from sys import platform

from dotenv import load_dotenv
import tweepy
import wikipediaapi

# Load API keys and tokens.
# Load .env if not running on Heroku.
if 'HEROKU' not in os.environ:
    load_dotenv()
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

# Set up the connection to the API.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Initialize the Wikipedia object.
wiki_wiki = wikipediaapi.Wikipedia('en')

# Get the current day in a format such as 'May 1'.
# Platform specific functionality to remove leading zeroes.
# Only support removal for Windows and Linux so far.
if platform == 'win32':
    current_date = date.today().strftime('%B %#d')
elif platform == 'linux':
    current_date = date.today().strftime('%B %-d')
else:
    current_date = date.today().strftime('%B %d')

# Get the Wikipedia page for the current day.
page_py = wiki_wiki.page(current_date.replace(' ', '_'))

# Get all events on the current day.
events = []

# The page will have an events section, possibly with subsections for year ranges.
events_section = page_py.sections[0]
events_subsections = page_py.sections[0].sections

# If the events section is not split into subsections, get the events directly from the events section.
if not events_subsections:
    for event in events_section.text.split('\n'):
        events.append(event)

# If there are subsections, get events from all subsections.
else:
    for subsection in events_subsections:
        for event in subsection.text.split('\n'):
            events.append(event)

# Get a random event.
# Sometimes the year will have a leading 0 e.g. 0946 - this is removed.
event = random.choice(events).lstrip('0')

# Tweet the event.
tweet = f'{current_date}, {event}'
api.update_status(tweet)
