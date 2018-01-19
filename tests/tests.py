import unittest

import datetime as dt

from morriscal import (
    ical_dt_constructor,
    create_ical_event,
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
        result = create_ical_event(EVENT)
        expected = ('\r\nBEGIN:VEVENT\r\n'
                    'UID:fakdshfakdshf\r\n'
                    'DTSTAMP:20180114T0001Z\r\n'
                    'DTSTART:20180106T1800Z\r\n'
                    'DTEND:20180106T2100Z\r\n'
                    'SUMMARY:folk festival\r\n'
                    'DESCRIPTION:sometown\r\n'
                    'LOCATION:sometown\r\n'
                    'END:VEVENT\r\n')
        self.assertEqual(result, expected)

