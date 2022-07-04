from django.urls import path
from . import views

app_name = 'shiftreports'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('shiftreports/', views.Shiftreports.as_view(), name='shiftreports'),
    # path('shiftreports/', views.shiftreports, name='shiftreports'),
    path('shiftreports/add/', views.addsr, name='addsr'),
    path('shiftreports/delete/<int:shiftreport_id>', views.deletesr, name='deletesr'),
    path('shiftreports/update/<int:shiftreport_id>', views.updatesr, name='updatesr'),
    path('shiftreports/payperiod/', views.payperiod, name='payperiod'),
    #path('report/',)
]