from datetime import date, timedelta
import simplejson as json
import sys

START_DATE = date(2016, 1, 1)
END_DATE = date(2017, 1, 1)


def run():
    input_data = read_input()
    # validate(input_data)

    print input_data

    # create data structures to hold every day of the year
    delta = END_DATE - START_DATE
    days = []
    date_map = {}
    for i in range(delta.days + 1):
        date = START_DATE + timedelta(days=i)
        days.append({
            'date': date,
            'expenses': [],
            'incomes': [],
        })
        date_map[date.isoformat()] = i

    #print date_map

    for income in input_data['incomes']:
        print income


def dates_from_sechedule(event, max_date=END_DATE.isoformat()):
    dates = []
    schedule = event['schedule']
    start = schedule['start'] or START_DATE.isoformat()

    if schedule['type'] == 'onTime':
        dates.append(schedule['start'])
    if schedule['type'] == 'monthly':
        pass
    if schedule['type'] == 'interval':
        pass
    else:
        pass  # throw error?


def read_input():
    return json.load(sys.stdin)

if __name__ == '__main__':
    run()
