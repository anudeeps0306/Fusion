from django.conf.urls import url
from django.urls import path
from . import views
from . import form_views


app_name = 'hr2'

urlpatterns = [
    url('ltc/', form_views.LTC.as_view(), name = 'LTC_form'),
    url('formManagement/', form_views.FormManagement.as_view(), name = 'formManagement'),
    url('tracking/', form_views.TrackProgress.as_view(), name = 'tracking'),
    url('formFetch/', form_views.FormFetch.as_view(), name = "fetch_form"),
    # url(r'^$', views.service_book, name='hr2'),
    # url(r'^hradmin/$', views.hr_admin, name='hradmin'),
    # url(r'^edit/(?P<id>\d+)/$', views.edit_employee_details,
    #     name='editEmployeeDetails'),
    # url(r'^viewdetails/(?P<id>\d+)/$',
    #     views.view_employee_details, name='viewEmployeeDetails'),
    # url(r'^editServiceBook/(?P<id>\d+)/$',
    #     views.edit_employee_servicebook, name='editServiceBook'),
    # url(r'^administrativeProfile/$', views.administrative_profile,
    #     name='administrativeProfile'),
    # url(r'^addnew/$', views.add_new_user, name='addnew'),
]
