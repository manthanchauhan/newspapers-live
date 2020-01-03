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


def create_calendars(start_date, session, in_place=False):
    # decide which calendars are to be created Tuple(month, year)
    present_date = datetime.now()
    calendars = []

    if start_date.year < present_date.year:
        for month in range(start_date.month, 13):
            calendars.append((month, start_date.year))

        for month in range(1, present_date.month+1):
            calendars.append((month, present_date.year))

    else:
        for month in range(start_date.month, present_date.month+1):
            calendars.append((month, start_date.year))

    total_calendars = len(calendars)
    # calendars = List[Tuple(month:int, year:int)]
    # calendars only contains newly created calendars

    # update session amount
    additional_session_amount = 0
    plan = Plan.objects.get(user=session.user)

    for index, calendar in enumerate(calendars):
        # for each calendar
        if index == 0:
            start = start_date
        else:
            start = datetime.strptime('01-' + str(calendar[0]) + '-' + str(calendar[1]), '%d-%m-%Y').date()

        cal = Calendar(session=session, start_date=start)

        if index != total_calendars-1:
            # if calendar isn't the last calendar to be created
            # end the current calendar
            end = monthrange(calendar[1], calendar[0])[1]
            end = datetime.strptime(str(end) + '-' + str(calendar[0]) + '-' + str(calendar[1]), '%d-%m-%Y').date()
            cal.end = end

        # update session amount
        cal.amount = calculate_bill(cal, plan)
        cal.save()
        additional_session_amount += cal.amount

    return additional_session_amount


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


def count_absentees(calendar):
    absentees = calendar.absentees
    count = 0
    mask = 1

    while mask <= absentees:
        if absentees & mask:
            count += 1
        mask <<= 1

    return count


def end_calendar(calendar):
    end = monthrange(calendar.start.month, calendar.start.year)[1]
    end = datetime.strptime(str(end) + '-' + str(calendar.start.month) + '-' + str(calendar.start.year),
                            '%d-%m-%Y').date()
    calendar.end = end
    calendar.save()
