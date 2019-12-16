from datetime import datetime
from calendars.models import Calendar
from calendar import monthrange
from plans.models import Plan


def calculate_bill(calendar, bill):
    if calendar.start > datetime.now().date():
        raise ValueError

    costs = list(bill.to_dict().values())
    start_day = calendar.start.day

    if calendar.end is not None:
        end_day = calendar.end.day
    else:
        end_day = datetime.now().day

    day = start_day
    amount = 0
    day_name = (datetime(year=calendar.start.year, month=calendar.start.month, day=day).weekday()+1) % 7
    absentees = calendar.absentees
    for i in range(0, day-1):
        absentees >>= 1

    while day <= end_day:
        bit = absentees % 2
        if not bit:
            amount += costs[day_name]

        day += 1
        day_name += 1
        day_name %= 7
        absentees >>= 1

    return amount


def toggle_absent_status(calendar_id, date, user):
    cal = Calendar.objects.get(id=calendar_id)
    absentees = cal.absentees
    date_bit = int(date)-1
    modifier = 2**date_bit
    absentees ^= modifier
    cal.absentees = absentees
    plan = Plan.objects.get(user=user)
    cal.amount = calculate_bill(cal, plan)
    cal.save()

    session = cal.session
    calendars = session.calendars.all()
    amount = 0

    for cal in calendars:
        amount += cal.amount

    session.amount = amount
    session.save()


def create_calendars(start_date, session):
    session_amount = 0
    present_date = datetime.now()
    calendars = list()

    if start_date.year < present_date.year:
        for month in range(start_date.month, 13):
            calendars.append((month, start_date.year))

        for month in range(1, present_date.month+1):
            calendars.append((month, present_date.year))

    else:
        for month in range(start_date.month, present_date.month+1):
            calendars.append((month, start_date.year))

    first_calendar = Calendar(session=session, start=start_date)

    if datetime.now().month != first_calendar.start.month or datetime.now().year != first_calendar.start.month:
        end = monthrange(first_calendar.start.year, first_calendar.start.month)[1]
        end = datetime.strptime(str(end) + '-' + str(first_calendar.start.month) + '-' + str(first_calendar.start.year), '%d-%m-%Y').date()
        first_calendar.end = end

    plan = Plan.objects.get(user=session.user)
    amount = calculate_bill(first_calendar, plan)
    session_amount += amount
    first_calendar.amount = amount
    first_calendar.save()

    if len(calendars) > 1:
        for calendar in calendars[1:]:
            start = datetime.strptime('01-' + str(calendar[0]) + '-' + str(calendar[1]), '%d-%m-%Y').date()
            cal = Calendar(session=session, start=start)

            if calendar != calendars[-1]:
                end = monthrange(calendar[1], calendar[0])[1]
                end = datetime.strptime(str(end) + '-' + str(calendar[0]) + '-' + str(calendar[1]), '%d-%m-%Y').date()
                cal.end = end

            cal.amount = calculate_bill(cal, plan)
            session_amount += cal.amount
            cal.save()

    return session_amount


def previous_calendar(calendar, calendars):
    if not len(calendars):
        return None

    if calendar == calendars[0]:
        return None

    for index, cal in enumerate(calendars):
        if cal == calendar:
            return calendars[index-1]


def next_calendar(calendar, calendars):
    if not len(calendars):
        return None

    if calendar == calendars[-1]:
        return None

    for index, cal in enumerate(calendars):
        if cal == calendar:
            return calendars[index+1]


def month_name(month):
    return {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec'
    }[month]


class Counter:
    def __init__(self):
        self._count = 1

    def increment(self):
        self._count += 1

    def count(self):
        return self._count

    def reset(self):
        self._count = 0
