from django.db import models
from applications.globals.models import ExtraInfo
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Constants:
    # Class for various choices on the enumerations
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    DEPARTMENT = (
        ('CSE', 'CSE'),
        ('ME', 'Mechanical'),
        ('ECE', 'ECE'),
        ('DESIGN', 'DESIGN'),
    )
    CATEGORY = (
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('OBC', 'OBC'),
        ('GENERAL', 'GENERAL'),
        ('PWD', 'PWD'),

    )
    MARITIAL_STATUS = (
        ('MARRIED', 'MARRIED'),
        ('UN-MARRIED', 'UN-MARRIED'),
        ('WIDOW', 'WIDOW'),

    )

    BLOOD_GROUP = (
        ('AB+', 'AB+'),
        ('O+', 'O+'),
        ('AB-', 'AB-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),

    )
    FOREIGN_SERVICE = (
        ('LIEN', 'LIEN'),
        ('DEPUTATION', 'DEPUTATION'),
        ('OTHER', 'OTHER'),
    )


# Employee model
class Employee(models.Model):
    """
    table for employee details
    """
    extra_info = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=40, default='')
    mother_name = models.CharField(max_length=40, default='')
    religion = models.CharField(max_length=40, default='')
    category = models.CharField(max_length=50, null=False, choices=Constants.CATEGORY)
    cast = models.CharField(max_length=40, default='')
    home_state = models.CharField(max_length=40, default='')
    home_district = models.CharField(max_length=40, default='')
    date_of_joining = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=40, default='')
    blood_group = models.CharField(
        max_length=50, choices=Constants.BLOOD_GROUP)

    def __str__(self):
        return self.extra_info.user.first_name


# table for employee  confidential details
class EmpConfidentialDetails(models.Model):
    """
    table for employee  confidential details
    """
    extra_info = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE)
    aadhar_no = models.BigIntegerField(default=0, max_length=12, 
                              validators=[MaxValueValidator(999999999999),MinValueValidator(99999999999)])
                              
    maritial_status = models.CharField(
        max_length=50, null=False, choices=Constants.MARITIAL_STATUS)
    bank_account_no = models.IntegerField(default=0)
    salary = models.IntegerField(default=0)

    def __str__(self):
        return self.extra_info.user.first_name

# table for employee's dependent details


class EmpDependents(models.Model):
    """Table for employee's dependent details """
    extra_info = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=50, choices=Constants.GENDER_CHOICES)
    dob = models.DateField(max_length=6, null=True)
    relationship = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.extra_info.user.first_name


class ForeignService(models.Model):
    """
    This table contains details about deputation, lien 
    and other foreign services of employee
    """
    extra_info = models.ForeignKey(ExtraInfo, on_delete=models.CASCADE)
    start_date = models.DateField(max_length=6, null=True, blank=True)
    end_date = models.DateField(max_length=6, null=True, blank=True)
    job_title = models.CharField(max_length=50, default='')
    organisation = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=300, default='')
    salary_source = models.CharField(max_length=100, default='')
    designation = models.CharField(max_length=100, default='')
    # award_name = models.CharField(max_length=100, default='')
    # award_type = models.CharField(max_length=100, default='')
    # achievement_date = models.CharField(max_length=100, default='')
    service_type = models.CharField(
        max_length=100, choices=Constants.FOREIGN_SERVICE)

    def __str__(self):
        return self.extra_info.user.first_name


class EmpAppraisalForm(models.Model):
    extra_info = models.ForeignKey(ExtraInfo, on_delete=models.CASCADE)
    year = models.DateField(max_length=6, null=True, blank=True)
    appraisal_form = models.FileField(
        upload_to='Hr2/appraisal_form', null=True, default=" ")

    def __str__(self):
        return self.extra_info.user.first_name


class WorkAssignemnt(models.Model):
    extra_info = models.ForeignKey(ExtraInfo, on_delete=models.CASCADE)
    start_date = models.DateField(max_length=6, null=True, blank=True)
    end_date = models.DateField(max_length=6, null=True, blank=True)
    job_title = models.CharField(max_length=50, default='')
    orders_copy = models.FileField(blank=True, null=True)

class LTCform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    # name = models.ForeignKey(Designation)
    blockYear = models.TextField()
    pfNo = models.IntegerField(max_length=50)
    designation = models.CharField(max_length=50)
    departmentInfo= models.CharField(max_length=20)
    leaveAvailability = models.BooleanField(null = True)
    leaveStartDate = models.DateField(max_length=6, null=True, blank=True)
    leaveEndDate = models.DateField(max_length=6, null=True, blank=True)
    dateOfLeaveForFamily = models.DateField(max_length=6, null=True, blank=True)
    natureOfLeave= models.TextField()
    purposeOfLeave= models.TextField()
    hometownOrNot = models.BooleanField()
    placeOfVisit = models.CharField(max_length=20, null=True)
    addressDuringLeave= models.TextField()
    modeForVacation = models.TextField()
    detailsOfFamilyMembersAlreadyDone = models.TextField()
    familyMembersAboutToAvail = models.CharField(
        max_length=30, default='self')
    detailsOfFamilyMembers= models.TextField()
    detailsOfDependents= models.TextField()
    amountOfAdvanceRequired= models.IntegerField(null=True)
    certifiedFamilyDependents= models.TextField()
    certifiedAdvance=models.TextField()
    adjustedMonth=models.TextField()
    date= models.DateField(max_length=6)
    phoneNumberForContact = models.IntegerField(max_length=10)
    approved = models.BooleanField(null = True)
    approvedDate = models.DateField(auto_now_add=True, null = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

class CPDAAdvanceform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    pfNo= models.IntegerField(max_length=20)
    amountRequired = models.IntegerField()
    purpose = models.TextField()
    adjustedPDA= models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    balanceAvailable= models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    advanceDueAdjustment = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    advanceAmountPDA= models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    amountCheckedInPDA = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    submissionDate = models.DateField()
    approved = models.BooleanField(null = True)
    approvedDate = models.DateField(auto_now_add=True, null = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

class CPDAReimbursementform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    pfNo= models.IntegerField(max_length=20)
    advanceTaken = models.IntegerField()
    purpose = models.TextField()
    adjustmentSubmitted= models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    balanceAvailable= models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    advanceDueAdjustment = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    advanceAmountPDA= models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    amountCheckedInPDA = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    submissionDate = models.DateField(auto_now_add=True)
    approved = models.BooleanField(null = True)
    approvedDate = models.DateField(auto_now_add=True, null = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

class Appraisalform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    disciplineInfo= models.CharField(max_length=50)
    specificFieldOfKnowledge = models.TextField()
    currentResearchInterests= models.TextField()
    coursesTaught= models.JSONField()
    sponsoredReseachProjects= models.JSONField()
    performanceComments = models.TextField()
    submissionDate = models.DateField()
    approved = models.BooleanField(null = True)
    approvedDate = models.DateField(auto_now_add=True, null = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

class Leaveform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    departmentInfo= models.CharField(max_length=20)
    leaveStartDate = models.DateField(max_length=6, null=True, blank=True)
    leaveEndDate = models.DateField(max_length=6, null=True, blank=True)
    natureOfLeave= models.TextField()
    purposeOfLeave= models.TextField()
    pfNo = models.IntegerField(max_length=50)
    addressDuringLeave= models.TextField()
    rolesTransferredTo = models.TextField() #academic and administrtative responsibilities assigned to
    submissionDate= models.DateField()
    approved = models.BooleanField(null = True)
    approvedDate = models.DateField(auto_now_add=True, null = True)    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

# class LeaveBalance(models.Model):
#     employee_id = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE)
#     casual_leave = models.IntegerField(default=0)
#     medical_leave = models.IntegerField(default=0)
#     earned_leave = models.IntegerField(default=0)
#     half_pay_leave = models.IntegerField(default=0)
#     commuted_leave = models.IntegerField(default=0)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True)