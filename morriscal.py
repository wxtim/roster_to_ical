'''
This script was written by Tim Pillinger\r\n
It's designed to take shifts\r\n
and return an ICS diary.\r\n
'''
import hashlib
import datetime as dt
import csv

from dateutil.parser import parse


def ical_dt_constructor(event_time, label, tzone='Z'):
    """
    args
        event_time (datetime):
            A datetime object
        label (str)
            string defining ICAL event label
            Options:
                DTSTAMP
                DTSTART
                DTEND

    kwargs
        tzone (str)
            timezone for ical construction
            defaults to 'Z'

    returns
        ical_dt (str):
            string in ical dt format
    """
    ical_dt = '{}:{:04d}{:02d}{:02d}T{:02d}{:02d}{}'
    ical_dt = ical_dt.format(label,
                             event_time.year,
                             event_time.month,
                             event_time.day,
                             event_time.hour,
                             event_time.minute,
                             tzone)
    return ical_dt


def create_ical_event(event):
    """create ical event string
    args
        event (dict)
            event dictionary
    returns
        event (str)
            string describing event in ICAL format"""
    uid = 'UID:{}'.format(event['uid'])
    today = dt.datetime.today().replace(hour=0, minute=1)
    start, finish = event['dt_start'], event['dt_finish']
    dtstamp = ical_dt_constructor(today, 'DTSTAMP')
    dtstart = ical_dt_constructor(start, 'DTSTART')
    dtend = ical_dt_constructor(finish, 'DTEND')
    summary = 'SUMMARY:{}'.format(event['event_name'])
    desc = 'DESCRIPTION:{}'.format(event['location'])
    loc = 'LOCATION:{}'.format(event['location'])
    msg = ('\r\nBEGIN:VEVENT\r\n{}\r\n{}\r\n{}\r\n{}'
           '\r\n{}\r\n{}\r\n{}\r\nEND:VEVENT\r\n')
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
    dt_finish = parse(finish)
    dt_start = parse(start)
    if dt_finish == dt_start:
        dt_finish = dt_start + dt.timedelta(hours=standard_duration)
    event.update({'dt_start': dt_start,
                  'dt_finish': dt_finish})
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
    """Script designed to take a csv file with a list of key event details and
    return a csv file importable into an ical compatible calendar programme"""
    events = get_csv(r'tests/at_data/example.csv')
    for i in range(0, len(events)):
        events[i].update({'uid': hashlib.md5(
            str(dt.datetime.today())).digest()})
    events = [parse_times(event) for event in events]
    events = [create_ical_event(event) for event in events]

    with open('tests/at_data/file.ics', 'w') as fhandle:
        fhandle.write(create_ical(events))
        fhandle.close()


if __name__ == "__main__":
    main()
