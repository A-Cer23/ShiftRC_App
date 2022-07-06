from django import forms

class Shiftreport_Form(forms.Form):
    date = forms.DateField(label="Date", widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(label="Start Time", widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(label="End Time", widget=forms.TimeInput(attrs={'type': 'time'}))
    wage = forms.IntegerField(label="Wage $/hr")

class Pay_Period_Form(forms.Form):
    start_date =  forms.DateField(label="Start Date", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label="End Date", widget=forms.DateInput(attrs={'type': 'date'}))