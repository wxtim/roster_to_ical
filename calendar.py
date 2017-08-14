'''
This script was written by Tim Pillinger\r\n
It's designed to take Leeming shifts\r\n
and return an ICS diary.\r\n
'''
import hashlib
import datetime as dt
import csv

shift_insts = [{'name': 'Development',
                'label': 'Dv',
                'start': '0830',
                'end': '1700'},
               {'name': 'Early Morning',
                'label': 'M',
                'start': '0515',
                'end': '1400'},
               {'name': 'Afternoon',
                'label': 'E',
                'start': '1200',
                'end': '1800'},
               {'name': 'Long Met-shift Day',
                'label': 'D',
                'start': '0515',
                'end': '1700'},
               {'name': 'Support Shift',
                'label': 'd\'',
                'start': '0630',
                'end': '1600'},
              ]


def create_ical_event(name, start, end, label, day, year='2019', month='12'):
    '''
    creates a ical even with all the key details
    '''
    uid = 'UID:{}'.format(hashlib.md5(str(dt.datetime.now())).hexdigest())
    dtstamp = 'DTSTAMP:{}{}{}T{}00Z'.format(year, month, day, '0001')
    dtstart = 'DTSTART:{}{}{}T{}00Z'.format(year, month, day, start)
    dtend = 'DTEND:{}{}{}T{}00Z'.format(year, month, day, end)
    summary = 'SUMMARY:{}'.format(name)
    msg = '\r\nBEGIN:VEVENT\r\n{}\r\n{}\r\n{}\r\n{}\r\n{}\r\nEND:VEVENT\r\n'
    return msg.format(uid, dtstamp, dtstart, dtend, summary)


def create_ical(calendar, shift_types):
    '''
    creates a large string which acts as the ical file
    '''
    outstring = """BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//hacksw/handcal//NONSGML v1.0//EN\r\n"""
    for date, shift in calendar['diary'].iteritems():

        for shift_type in shift_types:
            shift_type['day'] = date
            if shift_type['label'] == shift:
                shift_type['year'] = calendar['year']
                shift_type['month'] = calendar['month']
                outstring = outstring + create_ical_event(**shift_type)

    outstring = outstring + 'END:VCALENDAR\r\n'
    return outstring


def get_csv_data(fpath):
    '''
    Opened specified file
    and returns the data
    from that file
    '''
    with open(fpath, 'r') as fyle:
        reader = csv.reader(fyle)
        data = {}
        for row in reader:
            if len(row[1:]) == 1:
                data[row[0]], = row[1:]
            else:
                data[row[0]] = row[1:]
        data['diary'] = dict(zip(data['day'], data['shift']))
        return data


def check_data():
    '''
    Check the data in a data array for errors
    implement this
    '''


def main():
    '''
    see module
    '''
    fpath = 'input.csv'
    calendar = get_csv_data(fpath)

    outstring = create_ical(calendar, shift_insts)
    fhandle = open('calendar.ics', 'w')
    fhandle.write(outstring)


if __name__ == "__main__":
    main()
