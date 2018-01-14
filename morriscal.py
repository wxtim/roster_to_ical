'''
This script was written by Tim Pillinger\r\n
It's designed to take shifts\r\n
and return an ICS diary.\r\n
'''
import hashlib
import datetime as dt
import csv
import sys
import re

from dateutil.parser import parse


def ical_dt_constructor(dt, label, tz='Z'):
    """
    args
        dt (datetime):
            A datetime object
        label (str)
            string defining ICAL event label
            Options:
                DTSTAMP
                DTSTART
                DTEND

    kwargs
        tz (str)
            timezone for ical construction
            defaults to 'Z'

    returns
        ical_dt (str):
            string in ical dt format
    """
    ical_dt = '{}:{:04d}{:02d}{:02d}T{:02d}{:02d}{}'
    ical_dt = ical_dt.format(label,
                             dt.year,
                             dt.month,
                             dt.day,
                             dt.hour,
                             dt.minute,
                             tz)
    return ical_dt


def create_ical_event(event):
    '''
    creates a ical even with all the key details
    '''
    uid = 'UID:{}'.format(event['uid'])
    today = dt.datetime.today().replace(hour=0, minute=1)
    start, finish = event['dt_start'], event['dt_finish']
    dtstamp = ical_dt_constructor(today, 'DTSTAMP')
    dtstart = ical_dt_constructor(start, 'DTSTART')
    dtend = ical_dt_constructor(finish, 'DTEND')
    summary = 'SUMMARY:{}'.format(event['event_name'])
    desc = 'DESCRIPTION:{}'.format(event['location'])
    loc = 'LOCATION:{}'.format(event['location'])
    msg = '\r\nBEGIN:VEVENT\r\n{}\r\n{}\r\n{}\r\n{}\r\n{}\r\n{}\r\n{}\r\nEND:VEVENT\r\n'
    return msg.format(uid, dtstamp, dtstart, dtend, summary, desc, loc)


def create_ical(events):
    """
    args
        events (list):
            a list of events in string format

    returns
        calendar (string):
            a string making a valid ical file"""
    outstring = ("""BEGIN:VCALENDAR\r\nVERSION:2.0
                 \r\nPRODID:-//morris_calendar/
                 NONSGML v1.0//EN\r\n""")
    for event in events:
        outstring += event
    outstring = outstring + '\n\nEND:VCALENDAR\r\n'
    return outstring


def parse_times(event, standard_duration=3.):
    """Take an event dictionary and return the same dictionary with
    additional keypairs containing the parsed datetime objects of the
    start and end times of the event:

    args
        event (dict):
            dictionary describing a calendar event

    kwargs
        standard_duration (float or int):
            length in hours of default duration of an event.
            Set as 3 for the sake of argument"""
    start = ' '.join([event['start_date'], event['time']])
    if len(event['end_date']) == 0 and len(event['end_time']) == 0:
        finish = ' '.join([event['start_date'], event['end_time']])
    if len(event['end_date']) == 0:
        finish = ' '.join([event['start_date'], event['end_time']])
    else:
        finish = ' '.join([event['start_date'], event['time']])
    finish = parse(finish)
    start = parse(start)
    if finish == start:
        finish = start + dt.timedelta(hours=standard_duration)
    event.update({'dt_start': start,
                  'dt_finish': finish})
    return event


def get_csv(fpath):
    """Open a csv file and parse it into something useful

    Args
        fpath (str):
            filepath of the input data

    Returns
        events (list)
            a list of dictionaries containing details
            of individual events"""
    print fpath
    fyle = open(fpath, 'r')
    list_of_events = [i for i in csv.DictReader(fyle)]
    list_of_events = [parse_times(i) for i in list_of_events]
    return list_of_events


def main():
    events = get_csv(r'tests/at_data/example.csv')
    for i in range(0,len(events)):
        events[i].update({'uid': hashlib.md5(str(dt.datetime.today())).digest()})
    events = [parse_times(event) for event in events]
    events = [create_ical_event(event) for event in events]
    with open('tests/at_data/file.ics', 'w') as fh:
        fh.write(create_ical(events))
        fh.close()





if __name__ == "__main__":
    main()