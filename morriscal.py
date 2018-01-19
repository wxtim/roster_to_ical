'''
This script was written by Tim Pillinger\r\n
It's designed to take shifts\r\n
and return an ICS diary.\r\n
'''
import hashlib
import datetime as dt
import csv

from dateutil.parser import parse


from ical_utils import (
    ical_dt_constructor,
    create_ical_event,
    parse_times,
    get_csv
    )


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
