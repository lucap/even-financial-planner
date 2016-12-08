from datetime import datetime, date, timedelta
import json
import sys

START_DATE = '2016-01-01'
END_DATE = '2017-01-01'


def run():
    input_data = read_input()
    # validate(input_data)

    #print input_data

    # create data structures to hold every day of the year
    days = []
    date_map = {}

    for i, d in daterange(START_DATE, END_DATE):
        days.append({
            'date': d,
            'expenses': [],
            'incomes': [],
        })
        date_map[d] = i

    #print date_map

    for income in input_data['incomes']:
        dates = dates_from_sechedule(income)
        for d in dates:
            days[date_map[d]]['incomes'].append(income)

    for expense in input_data['expenses']:
        dates = dates_from_sechedule(expense)
        for d in dates:
            days[date_map[d]]['expenses'].append(expense)

    for d in days:
        if d['expenses'] or d['incomes']:
            print d


def dates_from_sechedule(event):
    dates = []
    schedule = event['schedule']
    start = schedule.get('start', START_DATE)

    if schedule['type'] == 'onTime':
        dates.append(start)
    if schedule['type'] == 'monthly':
        for i, d in daterange(start, END_DATE):
            if string_to_date(d).day in schedule['days']:
                dates.append(d)

    if schedule['type'] == 'interval':
        for i, d in daterange(start, END_DATE):
            if i % schedule['period'] == 0:
                dates.append(d)
    else:
        pass  # throw error?

    return dates

def date_to_string(d):
    return d.strftime('%Y-%m-%d')

def string_to_date(s):
    return datetime.strptime(s, '%Y-%m-%d')

# http://stackoverflow.com/a/1060330 (inclusive)
def daterange(start, end):
    start_date = string_to_date(start)
    end_date = string_to_date(end)
    for i in range(int((end_date - start_date).days)+1):
        yield i, date_to_string(start_date + timedelta(i))

def read_input():
    return json.load(sys.stdin)

if __name__ == '__main__':
    run()
