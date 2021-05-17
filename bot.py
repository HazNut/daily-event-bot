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


# Get the connection to the API.
def get_api_connection():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)


# Get the current day in a format such as 'May 1'.
# Platform specific functionality to remove leading zeroes.
# Only support removal for Windows and Linux so far.
def get_current_day():
    if platform == 'win32':
        return date.today().strftime('%B %#d')
    elif platform == 'linux':
        return date.today().strftime('%B %-d')
    else:
        return date.today().strftime('%B %d')


# Get all events that occurred on a given day of the year.
def get_events_on_day(day):
    # Initialize the Wikipedia object.
    wiki_wiki = wikipediaapi.Wikipedia('en')

    # Get the Wikipedia page for the current day.
    page_py = wiki_wiki.page(day.replace(' ', '_'))

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

    return events


# Choose a random event and tweet it.
def tweet_random_event(day, events, api):
    # Sometimes the year will have a leading 0 e.g. 0946 - this is removed.
    event = random.choice(events).lstrip('0')

    # Tweet the event.
    tweet = f'{day}, {event}'
    api.update_status(tweet)


def main():
    api = get_api_connection()
    day = get_current_day()
    events = get_events_on_day(day)
    tweet_random_event(day, events, api)


if __name__ == '__main__':
    main()
