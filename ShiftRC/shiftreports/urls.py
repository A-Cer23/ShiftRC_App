from django.urls import path
from . import views

app_name = 'shiftreports'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('shiftreports/', views.Shiftreports.as_view(), name='shiftreports'),
    path('shiftreports/add/', views.Addsr.as_view(), name='addsr'),
    path('shiftreports/update/<int:shiftreport_id>', views.Updatesr.as_view(), name='updatesr'),
    path('shiftreports/delete/<int:shiftreport_id>', views.Deletesr.as_view(), name='deletesr'),
    path('shiftreports/payperiod/', views.Payperiod.as_view(), name='payperiod'),
]