#!/usr/bin/env python3.6
import argparse
import datetime
import os
from pprint import pprint

from apiclient import discovery # type: ignore
import httplib2 # type: ignore
from oauth2client import client, tools # type: ignore
from oauth2client.file import Storage # type: ignore

from config import CREDENTIALS_PATH, CLIENT_SECRET_FILE

def get_credentials():
    store = Storage(CREDENTIALS_PATH)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(
            CLIENT_SECRET_FILE,
            scope="https://www.googleapis.com/auth/calendar",
            # redirect_uri='http://example.com/auth_return',
        )
        flow.user_agent = "QuickAdd"
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + CREDENTIALS_PATH) # TODO logger
    return credentials


def matches(a: str, b: str):
    return a.lower() == b.lower()

class QuickAdd:
    def __init__(self):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)

    def all_cals(self):
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                yield calendar_list_entry
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                raise StopIteration

    def get_cal_id(self, name: str):
        for c in self.all_cals():
            if matches(name, c['summary']): # TODO something fuzzier would be nice
                return c['id']
        raise RuntimeError("Coulnd't find calendar {}".format(name))

    def quick_add_to(self, cal: str, qstring: str):
        cal_id = 'primary' if cal is None else self.get_cal_id(cal)
        return self.service.events().quickAdd(
            calendarId=cal_id,
            text=qstring,
        ).execute()

def safe_get(d, *keys):
    for k in keys:
        if k in d:
            d = d[k]
        else:
            return ""
    return d

def extract_time_str(timish):
    if 'date' in timish:
        dstr = timish['date']
        return datetime.datetime.strptime(dstr, "%Y-%m-%d").strftime("%d %b %Y %a")
    elif 'dateTime' in timish:
        tzstr = timish.get('timeZone', None)
        tstr = timish['dateTime']
        res = datetime.datetime.strptime(tstr, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %b %Y %a %H:%M")
        if tzstr:
            res += " " + tzstr
        return res
    else:
        return str(timish)

def main():
    # TODO figure out if should be interactive or not

    parser = argparse.ArgumentParser(description="Google Calendar quick add tool")
    parser.add_argument("--cal", help="Calendar name", type=str, default=None)
    parser.add_argument("qstring", help="Quick add string", type=str)
    args = parser.parse_args()

    calname = args.cal
    qstring = args.qstring

    qa = QuickAdd()
    res = qa.quick_add_to(calname, qstring)

    starts = safe_get(res, 'start')
    if starts:
        starts = extract_time_str(starts)

    ends = safe_get(res, 'end')
    if ends:
        ends = extract_time_str(ends)

    print(
"""
{summary}
Starts   : {starts}
Ends     : {ends}
Repeats  : {repeats}
Location : {location}
Edit in browser: {link}
""".format(
    summary=safe_get(res, 'summary'),
    starts=starts,
    ends=ends,
    repeats=safe_get(res, 'recurrence'),
    location=safe_get(res, 'location'),
    link=safe_get(res, 'htmlLink'),
))
    # TODO advertise on google product forums
    # TODO display agenda for the day event was added
    # TODO license


if __name__ == '__main__':
    main()