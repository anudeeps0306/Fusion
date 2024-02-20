from django.shortcuts import render, get_object_or_404
from .models import *
from applications.globals.models import ExtraInfo
from applications.globals.models import *
from django.db.models import Q
from django.http import Http404
from .forms import EditDetailsForm, EditConfidentialDetailsForm, EditServiceBookForm, NewUserForm, AddExtraInfo
from django.contrib import messages
from applications.eis.models import *
from django.http import HttpResponse, HttpResponseRedirect
from applications.establishment.models import *
from applications.establishment.views import *
from applications.eis.models import *
from applications.globals.models import ExtraInfo, HoldsDesignation, DepartmentInfo, Designation
from html import escape
from io import BytesIO
import re
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import (get_object_or_404, redirect, render,
                              render)
from django.http import JsonResponse
from applications.filetracking.sdk.methods import *


def edit_employee_details(request, id):
    """ Views for edit details"""
    template = 'hr2Module/editDetails.html'

    try:
        employee = ExtraInfo.objects.get(user__id=id)
    except:
        raise Http404("Post does not exist")

    if request.method == "POST":
        for e in request.POST:
            print(e)
        print('--------------')
        form = EditDetailsForm(request.POST)
        conf_form = EditConfidentialDetailsForm(request.POST, request.FILES)
        print("f1", form.is_valid())
        print("f2", conf_form.is_valid())
        if form.is_valid() and conf_form.is_valid():
            form.save()
            conf_form.save()
            try:
                ee = ExtraInfo.objects.get(pk=id)
                ee.user_status = "PRESENT"
                ee.save()

            except:
                pass
            messages.success(request, "Employee details edited successfully")
        else:
            messages.warning(request, "Error in submitting form")
            pass
    else:
        print("Failed")

    form = EditDetailsForm(initial={'extra_info': employee.id})
    conf_form = EditConfidentialDetailsForm(initial={'extra_info': employee})
    context = {'form': form, 'confForm': conf_form, 'employee': employee}

    return render(request, template, context)


def hr_admin(request):
    """ Views for HR2 Admin page """

    user = request.user
    # extra_info = ExtraInfo.objects.select_related().get(user=user)
    designat = HoldsDesignation.objects.select_related().get(user=user)
    print(designat)
    if designat.designation.name == 'hradmin':
        template = 'hr2Module/hradmin.html'
        # searched employee
        query = request.GET.get('search')
        if(request.method == "GET"):
            if(query != None):
                emp = ExtraInfo.objects.filter(
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(id__icontains=query)
                ).distinct()
                emp = emp.filter(user_type="faculty")
            else:
                emp = ExtraInfo.objects.all()
                emp = emp.filter(user_type="faculty")
        else:
            emp = ExtraInfo.objects.all()
            emp = emp.filter(user_type="faculty")
        empPresent = emp.filter(user_status="PRESENT")
        empNew = emp.filter(user_status="NEW")
        context = {'emps': emp, "empPresent": empPresent, "empNew": empNew}
        print(context)
        return render(request, template, context)
    else:
        return HttpResponse('Unauthorized', status=401)


def service_book(request):
    """
    Views for service book page
    """
    user = request.user
    extra_info = ExtraInfo.objects.select_related().get(user=user)

    lien_service_book = ForeignService.objects.filter(
        extra_info=extra_info).filter(service_type="LIEN").order_by('-start_date')
    deputation_service_book = ForeignService.objects.filter(
        extra_info=extra_info).filter(service_type="DEPUTATION").order_by('-start_date')
    other_service_book = ForeignService.objects.filter(
        extra_info=extra_info).filter(service_type="OTHER").order_by('-start_date')
    appraisal_form = EmpAppraisalForm.objects.filter(
        extra_info=extra_info).order_by('-year')
    pf = extra_info.id
    workAssignemnt = WorkAssignemnt.objects.filter(
        extra_info_id=pf).order_by('-start_date')

    empprojects = emp_research_projects.objects.filter(
        pf_no=pf).order_by('-start_date')
    visits = emp_visits.objects.filter(pf_no=pf).order_by('-entry_date')
    conferences = emp_confrence_organised.objects.filter(
        pf_no=pf).order_by('-date_entry')
    template = 'hr2Module/servicebook.html'
    awards = emp_achievement.objects.filter(pf_no=pf).order_by('-date_entry')
    thesis = emp_mtechphd_thesis.objects.filter(
        pf_no=pf).order_by('-date_entry')
    context = {'lienServiceBooks': lien_service_book, 'deputationServiceBooks': deputation_service_book, 'otherServiceBooks': other_service_book,
               'appraisalForm': appraisal_form,
               'empproject': empprojects,
               'visits': visits,
               'conferences': conferences,
               'awards': awards,
               'thesis': thesis,
               'extrainfo': extra_info,
               'workAssignment': workAssignemnt,
               'awards': awards
               }

    return HttpResponseRedirect("/eis/profile/")
    # return render(request, template, context)


def view_employee_details(request, id):
    """ Views for edit details"""
    extra_info = ExtraInfo.objects.get(user__id=id)
    context = {}
    try:
        emp = Employee.objects.get(extra_info=extra_info)
        context['emp'] = emp
    except:
        print("Personal details not found")
    # try:
        
    # except:
    #     extra_info = ExtraInfo.objects.get(pk=id)
        # print("caught error")
        # return
    lien_service_book = ForeignService.objects.filter(
        extra_info=extra_info).filter(service_type="LIEN").order_by('-start_date')
    deputation_service_book = ForeignService.objects.filter(
        extra_info=extra_info).filter(service_type="DEPUTATION").order_by('-start_date')
    other_service_book = ForeignService.objects.filter(
        extra_info=extra_info).filter(service_type="OTHER").order_by('-start_date')
    appraisal_form = EmpAppraisalForm.objects.filter(
        extra_info=extra_info).order_by('-year')
    pf = extra_info.user.id
    print(pf)
    workAssignemnt = WorkAssignemnt.objects.filter(
        extra_info_id=pf).order_by('-start_date')

    empprojects = emp_research_projects.objects.filter(
        pf_no=pf).order_by('-start_date')
    visits = emp_visits.objects.filter(pf_no=pf).order_by('-entry_date')
    conferences = emp_confrence_organised.objects.filter(
        pf_no=pf).order_by('-date_entry')
    awards = emp_achievement.objects.filter(pf_no=pf).order_by('-date_entry')
    thesis = emp_mtechphd_thesis.objects.filter(
        pf_no=pf).order_by('-date_entry')

    response = {}
    # Check if establishment variables exist, if not create some fields or ask for them
    response.update(initial_checks(request))
    if is_eligible(request) and request.method == "POST":
        handle_appraisal(request)

    if is_eligible(request):
        response.update(generate_appraisal_lists(request))

    # If user has designation "HOD"
    if is_hod(request):
        response.update(generate_appraisal_lists_hod(request))

    # If user has designation "Director"
    if is_director(request):
        response.update(generate_appraisal_lists_director(request))

    response.update({'cpda': False, 'ltc': False,
                     'appraisal': True, 'leave': False})
    # designat = HoldsDesignation.objects.get(user=request.user).designation
    template = 'hr2Module/viewdetails.html'
    context.update({'lienServiceBooks': lien_service_book, 'deputationServiceBooks': deputation_service_book, 'otherServiceBooks': other_service_book, 'user': extra_info.user, 'extrainfo': extra_info,
               'appraisalForm': appraisal_form,
               'empproject': empprojects,
               'visits': visits,
               'conferences': conferences,
               'awards': awards,
               'thesis': thesis,
               'workAssignment': workAssignemnt,
            #    'designat':designat,
                
               })
    context.update(response)

    return render(request, template, context)


def edit_employee_servicebook(request, id):
    """ Views for edit Service Book details"""
    template = 'hr2Module/editServiceBook.html'

    try:
        employee = ExtraInfo.objects.get(user__id=id)
    except:
        raise Http404("Post does not exist")

    if request.method == "POST":
        form = EditServiceBookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Employee Service Book details edited successfully")
        else:
            messages.warning(request, "Error in submitting form")
            pass

    form = EditServiceBookForm(initial={'extra_info': employee.id})
    context = {'form': form, 'employee': employee
               }

    return render(request, template, context)


def administrative_profile(request, username=None):
    user = get_object_or_404(
        User, username=username) if username else request.user
    extra_info = get_object_or_404(ExtraInfo, user=user)
    if extra_info.user_type != 'faculty' and extra_info.user_type != 'staff':
        return redirect('/')
    pf = extra_info.id

    lien_service_book = ForeignService.objects.filter(
        extra_info=extra_info).filter(service_type="LIEN").order_by('-start_date')
    deputation_service_book = ForeignService.objects.filter(
        extra_info=extra_info).filter(service_type="DEPUTATION").order_by('-start_date')
    other_service_book = ForeignService.objects.filter(
        extra_info=extra_info).filter(service_type="OTHER").order_by('-start_date')

    response = {}

    response.update(initial_checks(request))
    if is_eligible(request) and request.method == "POST":
        handle_appraisal(request)

    if is_eligible(request):
        response.update(generate_appraisal_lists(request))

    # If user has designation "HOD"
    if is_hod(request):
        response.update(generate_appraisal_lists_hod(request))

    # If user has designation "Director"
    if is_director(request):
        response.update(generate_appraisal_lists_director(request))

    response.update({'cpda': False, 'ltc': False,
                     'appraisal': True, 'leave': False})
    workAssignemnt = WorkAssignemnt.objects.filter(
        extra_info_id=pf).order_by('-start_date')

    context = {'user': user,
               'pf': pf,
               'lienServiceBooks': lien_service_book, 'deputationServiceBooks': deputation_service_book, 'otherServiceBooks': other_service_book,
               'extrainfo': extra_info,
               'workAssignment': workAssignemnt
               }

    context.update(response)
    template = 'hr2Module/dashboard_hr.html'
    return render(request, template, context)

def chkValidity(password):
    flag = 0
    while True:  
        if (len(password)<8):
            flag = -1
            break
        elif not re.search("[a-z]", password):
            flag = -1
            break
        elif not re.search("[0-9]", password):
            flag = -1
            break
        elif not re.search("[_@$]", password):
            flag = -1
            break
        elif re.search("\s", password):
            flag = -1
            break
        else:
            return True
            break
    
    if flag ==-1:
        return False

def add_new_user(request):
    """ Views for edit Service Book details"""
    template = 'hr2Module/add_new_employee.html'

    if request.method == "POST":
        form = NewUserForm(request.POST)
        eform = AddExtraInfo(request.POST)
        # t_pass = request.POST['password1']
        # t_user = request.POST['username']

        if form.is_valid():
            user = form.save()
            messages.success(request, "New User added Successfully")
        else:
            print(form.errors)
            # print(request.POST['password1'])
            t_pass = '0000'
            if 'password1' in request.POST:
                t_pass = request.POST['password1']
            # messages.error(request,str(type(t_pass)))
            if chkValidity(t_pass):
                messages.error(request,"User already exists")
            elif not t_pass == '0000':
                messages.error(request,"Use Stronger Password")
            else:
                messages.error(request,"User already exists")
                

        if eform.is_valid():
            eform.save()
            messages.success(request, "Extra info of user saved successfully")
        elif not eform.is_valid:
            print(eform.errors)
            messages.error(request,"Some error occured")

    form = NewUserForm
    eform = AddExtraInfo

    try:
        employee = ExtraInfo.objects.all().first()
    except:
        raise Http404("Post does not exist")

    # if request.method == "POST":
    #     form = EditServiceBookForm(request.POST, request.FILES)

    #     if form.is_valid():
    #         form.save()
    #         messages.success(
    #             request, "Employee Service Book details edited successfully")
    #     else:
    #         messages.warning(request, "Error in submitting form")
    #         pass

    # form = EditServiceBookForm(initial={'extra_info': employee.id})
    context = {'employee': employee, "register_form": form, "eform": eform
               }

    return render(request, template, context)

def ltc_form(request, id):
    """ Views for edit details"""
    try:
        employee = ExtraInfo.objects.get(user__id=id)
    except:
        raise Http404("Post does not exist! id doesnt exist")

    print(employee.user_type)

    
    if(employee.user_type == 'faculty'):
        template = 'hr2Module/ltc_form.html'

        if request.method == "POST":
            family_mem_a = request.POST.get('id_family_mem_a', '')
            family_mem_b = request.POST.get('id_family_mem_b', '')
            family_mem_c = request.POST.get('id_family_mem_c', '')

        
            details_of_family_members = ', '.join(filter(None, [family_mem_a, family_mem_b, family_mem_c]))

        
            request.POST = request.POST.copy()
            request.POST['details_of_family_members_already_done'] = details_of_family_members

    
            family_members = []
            for i in range(1, 7):  # Loop through input fields for each family member
                name = request.POST.get(f'info_{i}_2', '')  # Get the name
                age = request.POST.get(f'info_{i}_3', '')   # Get the age
                if name and age:  # Check if both name and age are provided
                    family_members.append(f"{name} ({age} years)")  # Concatenate name and age

            family_members_str = ', '.join(family_members)

            # Populate the form with concatenated family member details
            request.POST['family_members_about_to_avail'] = family_members_str

            dependents = []
            for i in range(1, 7):  # Loop through input fields for each dependent
                name = request.POST.get(f'd_info_{i}_2', '')  # Get the name
                age = request.POST.get(f'd_info_{i}_3', '')   # Get the age
                why_dependent = request.POST.get(f'd_info_{i}_4', '')  # Get the reason for dependency
                if name and age:  # Check if both name and age are provided
                    dependents.append(f"{name} ({age} years), {why_dependent}")  # Concatenate name, age, and reason
            

            # Concatenate all dependent strings into a single string
            dependents_str = ', '.join(dependents)

            # Populate the form with concatenated dependent details
            request.POST['details_of_dependents'] = dependents_str

            # print("first",request.POST['family_members_about_to_avail'])
            pf_no = int(request.POST.get('pf_no')) if request.POST.get('pf_no') else None
            basic_pay_salary = int(request.POST.get('basic_pay_salary')) if request.POST.get('basic_pay_salary') else None
            amount_of_advance_required = int(request.POST.get('amount_of_advance_required')) if request.POST.get('amount_of_advance_required') else None
            phone_number_for_contact = int(request.POST.get('phone_number_for_contact')) if request.POST.get('phone_number_for_contact') else None


            try:
                ltc_request = LTCform.objects.create(
                    employee_id = id,
                    details_of_family_members_already_done=request.POST.get('details_of_family_members_already_done', ''),
                    family_members_about_to_avail=request.POST.get('family_members_about_to_avail', ''),
                    details_of_dependents=request.POST.get('details_of_dependents', ''),
                    name=request.POST.get('name', ''),
                    block_year=request.POST.get('block_year', ''),
                    pf_no=request.POST.get('pf_no', ''),
                    basic_pay_salary=request.POST.get('basic_pay_salary', ''),
                    designation=request.POST.get('designation', ''),
                    department_info=request.POST.get('department_info', ''),
                    leave_availability=request.POST.get('leave_availability', ''),
                    leave_start_date=request.POST.get('leave_start_date', ''),
                    leave_end_date=request.POST.get('leave_end_date', ''),
                    date_of_leave_for_family=request.POST.get('date_of_leave_for_family', ''),
                    nature_of_leave=request.POST.get('nature_of_leave', ''),
                    purpose_of_leave=request.POST.get('purpose_of_leave', ''),
                    hometown_or_not=request.POST.get('hometown_or_not', ''),
                    place_of_visit=request.POST.get('place_of_visit', ''),
                    address_during_leave=request.POST.get('address_during_leave', ''),
                    mode_for_vacation=request.POST.get('mode_for_vacation', ''),
                    details_of_family_members=request.POST.get('details_of_family_members', ''),
                    amount_of_advance_required=request.POST.get('amount_of_advance_required', ''),
                    certified_family_dependents=request.POST.get('certified_family_dependents', ''),
                    certified_advance=request.POST.get('certified_advance', ''),
                    adjusted_month=request.POST.get('adjusted_month', ''),
                    date=request.POST.get('date', ''),
                    phone_number_for_contact=request.POST.get('phone_number_for_contact', '')
                )
                print("done")
                messages.success(request, "Ltc form filled successfully")
            except Exception as e:
                print("error" , e)
                messages.warning(request, "Fill not correctly")
                context = {'employee': employee}
                return render(request, template, context)

            
         # Query all LTC requests
        ltc_requests = LTCform.objects.filter(employee_id=id)

        context = {'employee': employee, 'ltc_requests': ltc_requests}

        return render(request, template, context)
    else:
        return render(request, 'hr2Module/edit.html')

def view_ltc_form(request, id):
    ltc_form = get_object_or_404(LTCform, id=id)

    # Preprocessing data
    family_mem_a = ltc_form.family_members_about_to_avail.split(',')[0].strip() if ltc_form.family_members_about_to_avail else ''
    family_mem_b = ltc_form.family_members_about_to_avail.split(',')[1].strip() if ltc_form.family_members_about_to_avail else ''
    family_mem_c = ltc_form.family_members_about_to_avail.split(',')[2].strip() if ltc_form.family_members_about_to_avail else ''
    ltc_form.details_of_family_members_already_done = ', '.join(filter(None, [family_mem_a, family_mem_b, family_mem_c]))

    family_members = []
    for i in range(1, 7):  
        name = getattr(ltc_form, f'info_{i}_2', '')  
        age = getattr(ltc_form, f'info_{i}_3', '')   
        if name and age:
            family_members.append(f"{name} ({age} years)")
    ltc_form.family_members_about_to_avail = ', '.join(family_members)

    dependents = []
    for i in range(1, 7): 
        name = getattr(ltc_form, f'd_info_{i}_2', '')  
        age = getattr(ltc_form, f'd_info_{i}_3', '')   
        why_dependent = getattr(ltc_form, f'd_info_{i}_4', '')  
        if name and age:
            dependents.append(f"{name} ({age} years), {why_dependent}")
    ltc_form.details_of_dependents = ', '.join(dependents)

    context = {
        'ltc_form': ltc_form
    }
    print(ltc_form.block_year)

    return render(request, 'hr2Module/view_ltc_form.html', context)

def get_user_object_from_username(username: str) -> User:
    user = User.objects.get(username=username)
    return user

def get_designation_name(username):
    try:
        # Get the user object
        user = User.objects.get(username=username)

        print("User" , user)
        
        # Get the HoldsDesignation object associated with the user
        holds_designation = HoldsDesignation.objects.get(user=user)\

        print("Hole De", holds_designation)
        
        # Retrieve the designation name
        designation_name = holds_designation.designation.name
        
        return designation_name
    except User.DoesNotExist:
        return "User does not exist"
    except HoldsDesignation.DoesNotExist:
        return "Designation not found for user"

def forward_request(request, id):
    try:
        # Retrieve the LTC form object
        ltc_form = get_object_or_404(LTCform, id=id)

        # print(get_user_object_from_username("atul"))

        getting_d = get_designation_name("21BCS185")

        # print("2",getting_d)

        # Logic to handle the LTC form and prepare necessary data
        # For example:
        uploader = "21BCS183" # Assuming this is the username of the uploader
        uploader_designation = "student" # Assuming the uploader is a student
        receiver = "vkjain"  # Assuming this is the username of the HR admin
        receiver_designation = "CSE HOD"  # Assuming this is the designation of HR admin
        src_module = "hr2"  # Assuming the source module is the LTC module
        src_object_id = str(ltc_form.id)  # Assuming the LTC form object ID is used as src_object_id
        file_extra_JSON = {"key": "value"}  # Any additional data related to the file

        # Create a file representing the LTC form and send it to HR admin
        file_id = create_file(
            uploader=uploader,
            uploader_designation=uploader_designation,
            receiver=receiver,
            receiver_designation=receiver_designation,
            src_module=src_module,
            src_object_id=src_object_id,
            file_extra_JSON=file_extra_JSON,
            attached_file=None  # Attach any file if necessary
        )

        # file_id = create_file(uploader="21BCS078", 
        #     uploader_designation="student", 
        #     receiver="Shyam",
        #     receiver_designation="h1caretaker", 
        #     src_module="complaint", 
        #     src_object_id= src_object_id, 
        #     file_extra_JSON= {"value": 2}, 
        #     attached_file = None)

        # print("new1")


        # Add success message
        messages.success(request, "LTC form forwarded successfully")
        print(view_inbox(
            username="vkjain",
            designation="CSE HOD",
            src_module="hr2"
        ))
        # Return a success response
        # console.log("file_id", file_id)
        response_data = {'message': 'LTC form forwarded successfully', 'file_id': file_id}
        return JsonResponse(response_data)
    except Exception as e:
        # Log error
        print("Error:", e)
        
        # Add warning message
        messages.warning(request, "LTC form forwarding failed")

        # Return an error response if any exception occurs
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=500)
