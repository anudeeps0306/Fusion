from django.conf.urls import url

from . import views

app_name = 'hr2'

urlpatterns = [

    url(r'^$', views.service_book, name='hr2'),
    url(r'^hradmin/$', views.hr_admin, name='hradmin'),
    url(r'^edit/(?P<id>\d+)/$', views.edit_employee_details,
        name='editEmployeeDetails'),
    url(r'^viewdetails/(?P<id>\d+)/$',
        views.view_employee_details, name='viewEmployeeDetails'),
    url(r'^editServiceBook/(?P<id>\d+)/$',
        views.edit_employee_servicebook, name='editServiceBook'),
    url(r'^administrativeProfile/$', views.administrative_profile,
        name='administrativeProfile'),
    url(r'^addnew/$', views.add_new_user, name='addnew'),
    url(r'^ltc_form/(?P<id>\d+)/$', views.ltc_form,
        name='ltcForm'),
    url(r'^cpda_form/(?P<id>\d+)/$', views.ltc_form,
        name='ltcForm'),
    url(r'^view_ltc_form/(?P<id>\d+)/$', views.view_ltc_form,
        name='view_ltc_form'),
    url(r'^form_mangement_ltc/',views.form_mangement_ltc, name='form_mangement_ltc'),
    url(r'dashboard/', views.dashboard, name='dashboard'),
    url(r'^form_mangement_ltc_hr/(?P<id>\d+)/$',views.form_mangement_ltc_hr, name='form_mangement_ltc_hr'),
     url(r'^form_mangement_ltc_hod/',views.form_mangement_ltc_hod, name='form_mangement_ltc_hod'),
]
