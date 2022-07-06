from django.shortcuts import render, redirect, get_object_or_404
from .models import Shiftreport
from .forms import Pay_Period_Form, Shiftreport_Form 
from django.views import View
from django.views.generic.list import ListView
from datetime import timedelta


class Index(View):
    # Index view
    template_name = 'shiftreports/index.html'

    def get(self, request, *args, **kwargs):
        # return index page upon get request
        return render(request, self.template_name, {})


class Shiftreports(ListView):
    # Shiftreport listview
    # returns shitreports.html with all shiftreport data ordered by date
    model = Shiftreport
    paginate_by = 10
    template_name = 'shiftreports/shiftreports.html'
    ordering = ['-date']


class Addsr(View):
    # Add shiftreport view
    template_name = 'shiftreports/srform.html'
    form_class = Shiftreport_Form

    def get(self, request, *args, **kwargs):
        # renders shiftreport form with empty fields upon get request
        form = self.form_class()
        context = {
            'add_updt': 'Add',
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # upon post request, form data will be cleaned and turned into a shiftreport
        # updates shiftreport's total hours and total pay then saves to database
        # redirects to shiftreports list view
        form = self.form_class(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            wage = form.cleaned_data['wage']
            sr = Shiftreport(date = date, start_time = start_time, end_time = end_time, wage=wage)
            sr.update_total_hours()
            sr.update_total_pay()  
            sr.save()
            return redirect('/shiftreports')
 

class Updatesr(View):
    # Update shiftreport view
    template_name = 'shiftreports/srform.html'
    form_class = Shiftreport_Form

    def get(self, request, shiftreport_id, *args, **kwargs):
        # renders shiftreport form and fills form's fields with the shiftreport selected to update
        sr = get_object_or_404(Shiftreport, pk=shiftreport_id)
        form = self.form_class(initial={'date': sr.date, 'start_time': sr.start_time, 'end_time': sr.end_time, 'wage': sr.wage})
        context = {
            'add_updt': 'Update',
            'form':form
        }
        return render(request, self.template_name, context)

    def post(self, request, shiftreport_id, *args, **kwargs):
        # upon post request, form is cleaned and steps are repeated like the add shiftreport view post request
        form = self.form_class(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            wage = form.cleaned_data['wage']
            sr = get_object_or_404(Shiftreport, pk=shiftreport_id)
            sr.date = date
            sr.start_time = start_time
            sr.end_time = end_time
            sr.wage = wage
            sr.update_total_hours()
            sr.update_total_pay()
            sr.save()
            return redirect('/shiftreports')


class Deletesr(View):
    # deletes shiftreport based on shiftreport id
    def get(self, request, shiftreport_id, *args, **kwargs):
        sr = get_object_or_404(Shiftreport, pk=shiftreport_id)
        sr.delete()
        return redirect('/shiftreports')


class Payperiod(View):
    # payperiod view 
    form_class = Pay_Period_Form

    def get(self, request, *args, **kwargs):
        # renders an empty pay period form
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, 'shiftreports/payperiod.html', context)

    def post(self, request, *args, **kwargs):
        # upon post request, form is cleaned and gets the whole report list for all the shiftreports within the date range
        form = self.form_class(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            report = self.calculate_report(start_date, end_date)
            return render(request, 'shiftreports/report.html', report)
    
    def calculate_report(self, start_date, end_date):
        # takes start and end dates then finds the shiftreports within the date range
        # gathers all data needed for the report
        # returns a dictionary filled with report information
        shiftreports = Shiftreport.objects.filter(date__gte=start_date, date__lte=end_date)
        total_time = timedelta()
        total_shifts = 0
        total_pay = 0
        for sr in shiftreports:
            total_time += sr.total_hours
            total_shifts += 1
            total_pay += sr.total_pay
        total_hours, total_minutes = total_time_to_hours_minutes(total_time)
        report = {
            'total_pay': total_pay,
            'total_shifts': total_shifts,
            'total_time': {'total_hours': total_hours, 
                            'total_minutes': total_minutes,
                            },
        }
        return report


##### functions that are used by multiple views #####

def total_time_to_hours_minutes(total_time:timedelta):
    # returns total hours and minutes as integer type from the total time as timedelta type
    total_hours = int(total_time.total_seconds() / 3600)
    total_minutes = int(total_time.total_seconds() / 60) % 60
    return total_hours, total_minutes