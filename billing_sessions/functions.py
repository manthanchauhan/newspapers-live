from datetime import datetime
from calendars.models import Calendar


def create_calendars(start_date, session):
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
    first_calendar.save()

    if len(calendars) > 1:
        for calendar in calendars[1:]:
            start = datetime.strptime('01-' + str(calendar[0]) + '-' + str(calendar[1]), '%d-%m-%Y')
            Calendar(session=session, start=start).save()


class Counter:
    def __init__(self):
        self._count = 1

    def increment(self):
        self._count += 1

    def count(self):
        return self._count

    def reset(self):
        self._count = 0
