from django.db import models

# Create your models here.
class Shiftreport(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.date)