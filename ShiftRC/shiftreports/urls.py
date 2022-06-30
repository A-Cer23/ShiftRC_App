from django.urls import path
from . import views

app_name = 'shiftreports'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.addsr, name='addsr'),
    path('delete/<int:shiftreport_id>', views.deletesr, name='deletesr'),
    path('update/<int:shiftreport_id>', views.updatesr, name='updatesr'),
    path('payperiod/', views.payperiod, name='payperiod'),
    #path('report/',)
]