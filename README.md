# Daily Event Bot

Every day, [Daily Event Bot](https://twitter.com/DailyEventBot1) posts an event that happened on that day of the year.

This repo is deployed to Heroku. The Heroku Scheduler addon is used to run bot.py every day at 9am BST. The script gets a random event from the Wikipedia page of the current day of the year, for example see the page for [May 1](https://en.wikipedia.org/wiki/May_1).
