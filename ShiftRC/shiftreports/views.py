from django.shortcuts import render, redirect, get_object_or_404
from .models import Shiftreport
from .forms import Pay_Period_Form, Shiftreport_Form 
from django.http import Http404
from datetime import datetime, date, timedelta

# Create your views here.
def index(request):
    shiftreport_list = Shiftreport.objects.order_by('-date')
    context = {
        'shiftreport_list': shiftreport_list,
        }
    return render(request, 'shiftreports/index.html', context)

def addsr(request):
    if request.method == "POST":
        form = Shiftreport_Form(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            sr = Shiftreport(date = date, start_time = start_time, end_time = end_time)
            sr.save()
            return redirect('/')
    else:
        form = Shiftreport_Form()
        context = {
        'add_updt': 'Add',
        'form': form,
    }
    return render(request, 'shiftreports/srform.html', context)

def updatesr(request, shiftreport_id):
    if request.method == "POST":
        form = Shiftreport_Form(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            sr = get_object_or_404(Shiftreport, pk=shiftreport_id)
            sr.date = date
            sr.start_time = start_time
            sr.end_time = end_time
            sr.save()
            return redirect('/')
    else:
        sr = get_object_or_404(Shiftreport, pk=shiftreport_id)
        form = Shiftreport_Form(initial={'date': sr.date, 'start_time': sr.start_time, 'end_time': sr.end_time})
        context = {
            'add_updt': 'Update',
            'form':form
        }
    return render(request, 'shiftreports/srform.html', context)

def deletesr(request, shiftreport_id):
    try:
        sr = Shiftreport.objects.get(pk=shiftreport_id)
        sr.delete()
    except Shiftreport.DoesNotExist:
        raise Http404("Shiftreport does not exist")
    return redirect('/')


def payperiod(request, wage=15):
    if request.method == 'POST':
        form = Pay_Period_Form(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            wage = form.cleaned_data['wage']
            report = calculate_report(start_date, end_date, wage)
            return render(request, 'shiftreports/report.html', report)

    else:
        form = Pay_Period_Form(initial={'wage': wage})
        context = {
            'form': form,
        }
        return render(request, 'shiftreports/payperiod.html', context)

def report(request):
    pass

def calculate_report(start_date, end_date, wage):
    shiftreports = Shiftreport.objects.filter(date__gte=start_date, date__lte=end_date)
    total_time = timedelta()
    total_shifts = 0
    for sr in shiftreports:
        start_time = datetime.combine(date.today(), sr.start_time)
        end_time = datetime.combine(date.today(), sr.end_time)
        total_time += end_time - start_time
        total_shifts += 1
    total_pay = (total_time.total_seconds()/60/60) * wage
    report = {
        'total_pay': total_pay,
        'total_shifts': total_shifts,
        'total_time': total_time.total_seconds()/60/60,
        'wage':wage
    }
    return report