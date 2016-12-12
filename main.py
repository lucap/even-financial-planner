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
    events = []
    event_map = {}

    for i, d in daterange(START_DATE, END_DATE):
        events.append({
            'index': i,
            'date': d,
            'expenses': [],
            'incomes': [],
        })
        event_map[d] = i

    #print event_map

    for income in input_data['incomes']:
        dates = dates_from_sechedule(income)
        for d in dates:
            events[event_map[d]]['incomes'].append(income)

    for expense in input_data['expenses']:
        dates = dates_from_sechedule(expense)
        for d in dates:
            events[event_map[d]]['expenses'].append(expense)

    c = 0
    for d in events:
        if d['expenses'] or d['incomes']:
            pass
            #print d
        if d['incomes']:
            c += 1

    #print c

    # this is the data structure we're going to optimize
    # each row represents a day in the year where an income occurs
    # columns: date - spendable - incomes - expenses until next income
    income_vector = []
    for i, event in enumerate(events):
        if event['incomes']:
            income_total = 0
            for income in event['incomes']:
                income_total += income['amount']

            j = i
            expense_total = 0
            while True:
                if events[j]['expenses']:
                    for expense in events[j]['expenses']:
                        expense_total += expense['amount']
                j += 1

                if j >= len(events) or events[j]['incomes']:
                    break

            income_vector.append([
                event['date'],
                0,
                income_total,
                expense_total
            ])

    for i in  income_vector:
        print i

    print is_solvent(income_vector)

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

def is_solvent(vectors):
    solvent = True
    i = 0
    income_pool = 0
    expense_pool = 0
    while solvent and i < len(vectors):
        income_pool += (vectors[i][2] - vectors[i][1])
        expense_pool += vectors[i][3]
        solvent = (income_pool - expense_pool >= 0)
        i += 1

    return solvent

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
