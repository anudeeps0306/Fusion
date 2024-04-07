from django.contrib import admin

from .models import Employee,EmpConfidentialDetails,ForeignService,EmpDependents,EmpAppraisalForm,WorkAssignemnt, LTCform, Appraisalform, CPDAAdvanceform, CPDAReimbursementform, Leaveform

# Register your models here.

admin.site.register(Employee)
admin.site.register(EmpConfidentialDetails)
admin.site.register(EmpDependents)
admin.site.register(ForeignService)
admin.site.register(EmpAppraisalForm)
admin.site.register(WorkAssignemnt)
admin.site.register(LTCform)
admin.site.register(Appraisalform)
admin.site.register(CPDAAdvanceform)
admin.site.register(CPDAReimbursementform)
admin.site.register(Leaveform)