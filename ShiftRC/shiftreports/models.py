from datetime import datetime, date, timedelta
from django.db import models

# Create your models here.
class Shiftreport(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    wage = models.IntegerField(default=15)
    total_hours:timedelta = models.DurationField(default=timedelta())
    total_pay = models.IntegerField(default=0)

    def update_total_hours(self):
        start_time = datetime.combine(date.today(), self.start_time)
        end_time = datetime.combine(date.today(), self.end_time)
        self.total_hours = end_time - start_time

    def update_total_pay(self):
        self.total_pay = (self.total_hours.total_seconds()/60/60) * self.wage

    def get_total_hours_minutes(self):
        total_hours = int(self.total_hours.total_seconds() / 3600)
        total_minutes = int(self.total_hours.total_seconds() / 60) % 60
        return f"{total_hours}:{total_minutes}"

    def __str__(self):
        return str(self.date)
