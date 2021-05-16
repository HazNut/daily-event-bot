from datetime import date
import os
import random

from dotenv import load_dotenv
import tweepy
import wikipediaapi

# Load API keys and tokens.
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
# The # is a Windows-specific way of removing the leading zero from the day.
# May be able to use a hyphen for Linux.
current_date = date.today().strftime('%B %#d')

# Get the Wikipedia page for the current day.
page_py = wiki_wiki.page(current_date.replace(' ', '_'))

# Get all events on the current day.
events = []
for section in page_py.sections[0].sections:
    for event in section.text.split('\n'):
        events.append(event)

# Get a random event.
# Sometimes the year will have a leading 0 e.g. 0946 - this is removed.
event = random.choice(events).lstrip('0')

# Tweet the event.
tweet = f'{current_date}, {event}'
api.update_status(tweet)
