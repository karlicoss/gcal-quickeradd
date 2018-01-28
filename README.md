Long story short: Google broke 'quick add' feature in google calendar after its design 'update' (you can nag them in [this thread](https://productforums.google.com/forum/#!msg/calendar/CIwo3Ch-aTk/5TEmUvoSAwAJ)). This script aims to work around it.

# Demo
`quickeradd.py --cal work "lunch tomorrow 12:00 with Paul for an hour"`

    lunch with Paul
    Starts   : 29 Jan 2018 Mon 12:00
    Ends     : 29 Jan 2018 Mon 13:00
    Repeats  : 
    Location : 
    Edit in browser: https://www.google.com/calendar/event?eid=cjhib2NkaG5mazJzbHU1ZnVkZ3YyaWc0NjQgbDFyM2YzZ2cwamZzajA2bzdzYnFhdTNhbThAZw

![Demo](https://media.giphy.com/media/xThta97FV4kypC8mFW/giphy.gif)

# Installation
python3 is required
    
    pip3 install -r requirements.txt

You can also bind `quickeradd.sh` on a hotkey (e.g. Win+Q) in your window manager, it will start a terminal and prompt for a calendar and quick add string interactively.

# Usage
To use the tool, just run it interactively: `quickeradd.py` or pass command line args to it: e.g. `quickeradd.py --cal work "meeting on monday 15:00 every week"`.

However, you'd need to authorise the tool to use google calendar first. You can read about it in detail [here](https://developers.google.com/api-client-library/python/start/get_started), but basically you need to:

1. Create a new project in https://console.developers.google.com/apis/
2. Go to Library and enable Google Calendar Api: https://console.developers.google.com/apis/library/calendar-json.googleapis.com/
3. Go to Credentials (e.g. https://console.developers.google.com/apis/credentials?project=gcal-quickeradd**
Create credentials -> Oauth client id -> accept the conscent if necessary -> Other
4. Download the oauth json and put in in `~/.gcal-quickeradd/client_secret.json`
5. You might need to wait for few minutes before using the API, it has to propagate throught google's servers.

First time you call the script you'd have to authorise it to use google calendar.

See `config.py` for token and oath key paths.
