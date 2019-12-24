from django.shortcuts import render, redirect
from django.views import View
from billing_sessions.forms import SessionCreationForm
from billing_sessions.models import BillingSession
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from calendar import monthrange
from plans.models import Plan
from calendars.models import Calendar
from billing_sessions.functions import create_calendars, calculate_bill, previous_calendar
from billing_sessions.functions import next_calendar, month_name, toggle_absent_status
from billing_sessions.functions import count_absentees

# Create your views here.


class Home(LoginRequiredMixin, View):
    template = 'billing_sessions/home.html'

    def get(self, request, id=None):
        user = request.user
        current_session = None

        if user.current_session_id is not None:
            try:
                current_session = BillingSession.objects.get(id=user.current_session_id)
            except BillingSession.DoesNotExist:
                user.current_session_id = None
                user.save()

        if user.current_session_id is not None:
            amount = current_session.amount

            try:
                previous_session = BillingSession.objects.get(id=current_session.prev_session)
            except BillingSession.DoesNotExist:
                previous_session = None
            calendars = list(current_session.calendars.all())

            if id is not None:
                recent_cal = list(current_session.calendars.all())[-1]
                calendar = Calendar.objects.get(id=id)

                if calendar == recent_cal:
                    return redirect('home')

                monthly_amount = calendar.amount
            else:
                present_date = datetime.now()
                last_month = calendars[-1].start.month
                last_year = calendars[-1].start.year

                if last_month != present_date.month or last_year != present_date.year:
                    if last_month == 12:
                        start_date = datetime.strptime('01-' + str(1) + '-' + str(last_year+1))
                    else:
                        start_date = datetime.strptime('01-' + str(last_month+1) + '-' + str(last_year))

                    create_calendars(start_date, current_session)

                calendars = list(current_session.calendars.all())
                calendar = calendars[-1]

                plan = Plan.objects.get(user=user)
                monthly_amount = calculate_bill(calendar, plan)
                difference = monthly_amount - calendar.amount
                calendar.amount = monthly_amount
                current_session.amount += difference
                current_session.save()
                calendar.save()

            calendar_id = calendar.id
            prev = previous_calendar(calendar, calendars)

            if prev is not None:
                prev_id = prev.id
            else:
                prev_id = None

            next = next_calendar(calendar, calendars)

            if next is not None:
                next_id = next.id
            else:
                next_id = None

            start_date = calendar.start
            empty_days = (start_date.replace(day=1).weekday()+1) % 7
            total_days = monthrange(start_date.year, start_date.month)[1]
            days = list()

            for day in range(0, empty_days):
                days.append({'date': 0, 'status': 'disabled'})

            today = datetime.now().day
            for day in range(1, total_days+1):
                if day < start_date.day:
                    days.append({'date': day, 'status': 'not-included', 'absent': False})
                elif day <= today:
                    days.append({'date': day, 'status': 'active', 'absent': False})
                else:
                    if calendar.end is None:
                        days.append({'date': day, 'status': 'future', 'absent': False})
                    else:
                        days.append({'date': day, 'status': 'active', 'absent': False})

            absentees = calendar.absentees
            i = 0

            while absentees:
                bit = absentees % 2
                days[empty_days+i]['absent'] = bool(bit)
                absentees >>= 1
                i += 1

            if len(days) > 35:
                days = [days[0:7], days[7:14], days[14:21], days[21:28], days[28:35], days[35:]]
            else:
                days = [days[0:7], days[7:14], days[14:21], days[21:28], days[28:]]
            return render(request, self.template, {'current_session': current_session,
                                                   'days': days,
                                                   'date': calendars[0].start.strftime('%d/%m/%y'),
                                                   'amount': amount,
                                                   'monthly_amount': monthly_amount,
                                                   'prev': prev_id,
                                                   'calendar_id': calendar_id,
                                                   'next': next_id,
                                                   'month_name': month_name(calendar.start.month),
                                                   'year_name': str(calendar.start.year)[-2:],
                                                   'previous_session': previous_session,
                                                   })

        form = SessionCreationForm(user=request.user)
        return render(request, self.template, {'current_session': current_session,
                                               'form': form})

    def post(self, request, id=None):
        if 'prev' in request.POST.keys():
            return redirect('calendar', id=request.POST['prev'])

        if 'next' in request.POST.keys():
            return redirect('calendar', id=request.POST['next'])

        if 'date' in request.POST.keys():
            date = request.POST['date']
            calendar_id = request.POST['calendar_id']
            toggle_absent_status(calendar_id, date, request.user)
            return redirect('calendar', id=calendar_id)

        if 'end_session' in request.POST.keys():
            return end_session(request)

        form = SessionCreationForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('/sessions/home')
        else:
            return render(request, self.template, {'form': form})


def try_func(request, id):
    print(id)
    return None


def end_session(request):
    user = request.user
    current_session_id = user.current_session_id
    current_session = BillingSession.objects.get(id=current_session_id)

    if current_session is None:
        messages.error(request, 'Invalid request')
        return redirect('home')

    current_session.end = datetime.now().date()
    absentees = 0
    calendars = list(current_session.calendars.all())

    for calendar in calendars:
        absentees += count_absentees(calendar)

    current_session.absentees = absentees
    current_session.save()

    if current_session.start == datetime.now().date():
        current_session.delete()

    user.current_session_id = None
    user.save()

    for calendar in calendars:
        calendar.delete()

    return redirect('home')


