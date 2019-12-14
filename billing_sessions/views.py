from django.shortcuts import render, redirect
from django.views import View
from billing_sessions.forms import SessionCreationForm
from billing_sessions.models import BillingSession
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from calendar import monthrange
from plans.models import Plan
from billing_sessions.functions import create_calendars, calculate_bill

# Create your views here.


class Home(LoginRequiredMixin, View):
    template = 'billing_sessions/home.html'

    def get(self, request):
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
            calendars = list(current_session.calendars.all())
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
            calendar.amount = monthly_amount
            start_date = calendar.start
            empty_days = (start_date.replace(day=1).weekday()+1) % 7
            total_days = monthrange(start_date.year, start_date.month)[1]
            days = list()

            for day in range(0, empty_days):
                days.append({'date': 0, 'status': 'disabled'})

            today = datetime.now().day
            for day in range(1, total_days+1):
                if day < start_date.day:
                    days.append({'date': day, 'status': 'not-included'})
                elif day <= today:
                    days.append({'date': day, 'status': 'active'})
                else:
                    days.append({'date': day, 'status': 'future'})

            days = [days[0:7], days[7:14], days[14:21], days[21:28], days[28:]]
            return render(request, self.template, {'current_session': current_session,
                                                   'days': days,
                                                   'date': calendars[0].start.strftime('%d/%m/%y'),
                                                   'amount': amount,
                                                   'monthly_amount': monthly_amount,
                                                   })

        form = SessionCreationForm(user=request.user)
        return render(request, self.template, {'current_session': current_session,
                                               'form': form})

    def post(self, request):
        form = SessionCreationForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('/sessions/home')
        else:
            return render(request, self.template, {'form': form})



