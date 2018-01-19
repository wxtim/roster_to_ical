import unittest

import datetime as dt

from ical_utils import (
    ical_dt_constructor,
    create_ical_event,
    parse_times,
    get_csv
    )

BIRTHDAY = dt.datetime(year=1983,
                       month=12,
                       day=13,
                       hour=14,
                       minute=55)

EVENT = {'uid': 'fakdshfakdshf',
         'end_date': '04/06/18',
         'event_name': 'folk festival',
         'dt_start': dt.datetime(2018, 1, 6, 18, 0),
         'dt_finish': dt.datetime(2018, 1, 6, 21, 0),
         'end_time': '12:00:00',
         'time': '18:00:00',
         'cancelled': '',
         'start_date': '01/06/18',
         'location': 'sometown'}


class Test_ical_dt_constructor(unittest.TestCase):
    def test_basic(self):
        result = ical_dt_constructor(BIRTHDAY,
                                     'DTSTART')
        expected = 'DTSTART:19831213T1455Z'
        self.assertEqual(result, expected)


class Test_create_ical_event(unittest.TestCase):
    def test_basic(self):
        results = create_ical_event(EVENT).split('\n')
        expecteds = ['\r','BEGIN:VEVENT\r',
                    'UID:fakdshfakdshf\r',
                    'DTSTAMP:20180119T0001Z\r',
                    'DTSTART:20180106T1800Z\r',
                    'DTEND:20180106T2100Z\r',
                    'SUMMARY:folk festival\r',
                    'DESCRIPTION:sometown\r',
                    'LOCATION:sometown\r',
                    'END:VEVENT\r']
        for result, expected in zip(results, expecteds):
            self.assertEqual(result, expected)


class Test_parse_times(unittest.TestCase):
    def test_basic(self):
        EVENT.pop('dt_start')
        EVENT.pop('dt_finish')
        result = parse_times(EVENT)
        self.assertEqual(EVENT, result)


class Test_get_csv(unittest.TestCase):
    def test_basic(self):
        result = get_csv(r'at_data/example.csv')
        self.assertEqual(type(result), list)
        self.assertEqual(type(result[0]), dict)