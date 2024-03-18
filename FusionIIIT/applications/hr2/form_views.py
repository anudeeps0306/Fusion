from .serializers import LTC_serializer, CPDAAdvance_serializer, Appraisal_serializer, CPDAReimbursement_serializer, Leave_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import LTCform, CPDAAdvanceform, CPDAReimbursementform, Leaveform, Appraisalform
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from applications.filetracking.sdk.methods import *
from applications.globals.models import Designation, HoldsDesignation

class LTC(APIView):
    serializer_class = LTC_serializer
    permission_classes = (AllowAny, )
    def post(self, request):
        user_info = request.data[0]
        receiver_value = User.objects.get(username=user_info['receiver_name'])
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        serializer = self.serializer_class(data = request.data[1])
        if serializer.is_valid():
            serializer.save()
            file_id = create_file(uploader = user_info['uploader_name'], uploader_designation = user_info['uploader_designation'], receiver = user_info['receiver_name'], receiver_designation=obj.name, src_module="HR", src_object_id= str(serializer.data['id']), file_extra_JSON= {"type": "LTC"}, attached_file= None)
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        pk = request.query_params.get("name")
        print(pk)
        try: 
            forms = LTCform.objects.get(created_by =  pk)           
            serializer = self.serializer_class(forms, many = False)
        except MultipleObjectsReturned:
            forms = LTCform.objects.filter(created_by =  pk)
            serializer = self.serializer_class(forms, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        pk = request.query_params.get("id")
        receiver = request.data[0]
        send_to = receiver['receiver']
        receiver_value = User.objects.get(username=send_to)
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        form = LTCform.objects.get(id = pk)
        serializer = self.serializer_class(form, data = request.data[1])
        if serializer.is_valid():
            serializer.save()
            forward_file(file_id = receiver['file_id'], receiver = receiver['receiver'], receiver_designation = obj.name, remarks = receiver['remarks'], file_extra_JSON = receiver['file_extra_JSON'])
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request,*args, **kwargs):
        id = request.query_params.get("id")
        is_archived = archive_file(file_id= id)
        return Response(status = status.HTTP_200_OK)

class FormManagement(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        designation = request.query_params.get("designation")
        inbox = view_inbox(username = username, designation = designation, src_module = "HR")
        return Response(inbox, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        username = request.data['receiver']
        receiver_value = User.objects.get(username=username)
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        forward_file(file_id = request.data['file_id'], receiver = request.data['receiver'], receiver_designation = obj.name, remarks = request.data['remarks'], file_extra_JSON = request.data['file_extra_JSON'])
        return Response(status = status.HTTP_200_OK)  


class CPDAAdvance(APIView):
    serializer_class = CPDAAdvance_serializer
    permission_classes = (AllowAny, )
    def post(self, request):
        user_info = request.data[0]
        receiver_value = User.objects.get(username=user_info['receiver_name'])
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        serializer = self.serializer_class(data = request.data[1])
        if serializer.is_valid():
            serializer.save()
            file_id = create_file(uploader = user_info['uploader_name'], uploader_designation = user_info['uploader_designation'], receiver = user_info['receiver_name'], receiver_designation=obj.name, src_module="HR", src_object_id= str(serializer.data['id']), file_extra_JSON= {"type": "LTC"}, attached_file= None)
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        pk = request.query_params.get("name")
        try: 
            forms = CPDAAdvanceform.objects.get(created_by =  pk)           
            serializer = self.serializer_class(forms, many = False)
        except MultipleObjectsReturned:
            forms = CPDAAdvanceform.objects.filter(created_by =  pk)
            serializer = self.serializer_class(forms, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        pk = request.query_params.get("id")
        receiver = request.data[0]
        send_to = receiver['receiver']
        receiver_value = User.objects.get(username=send_to)
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        form = CPDAAdvanceform.objects.get(id = pk)
        serializer = self.serializer_class(form, data = request.data[1])
        if serializer.is_valid():
            serializer.save()
            forward_file(file_id = receiver['file_id'], receiver = receiver['receiver'], receiver_designation = obj.name, remarks = receiver['remarks'], file_extra_JSON = receiver['file_extra_JSON'])
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,*args, **kwargs):
        id = request.query_params.get("id")
        is_archived = archive_file(file_id= id)
        return Response(status = status.HTTP_200_OK)

class CPDAReimbursement(APIView):
    serializer_class = CPDAReimbursement_serializer
    permission_classes = (AllowAny, )
    def post(self, request):
        user_info = request.data[0]
        receiver_value = User.objects.get(username=user_info['receiver_name'])
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        serializer = self.serializer_class(data = request.data[1])
        if serializer.is_valid():
            serializer.save()
            file_id = create_file(uploader = user_info['uploader_name'], uploader_designation = user_info['uploader_designation'], receiver = user_info['receiver_name'], receiver_designation=obj.name, src_module="HR", src_object_id= str(serializer.data['id']), file_extra_JSON= {"type": "LTC"}, attached_file= None)
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        pk = request.query_params.get("name")
        print(pk)
        try: 
            forms = CPDAReimbursementform.objects.get(created_by =  pk)           
            serializer = self.serializer_class(forms, many = False)
        except MultipleObjectsReturned:
            forms = CPDAReimbursementform.objects.filter(created_by =  pk)
            serializer = self.serializer_class(forms, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        pk = request.query_params.get("id")
        receiver = request.data[0]
        send_to = receiver['receiver']
        receiver_value = User.objects.get(username=send_to)
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        form = CPDAReimbursementform.objects.get(id = pk)
        serializer = self.serializer_class(form, data = request.data[1])
        if serializer.is_valid():
            serializer.save()
            forward_file(file_id = receiver['file_id'], receiver = receiver['receiver'], receiver_designation = obj.name, remarks = receiver['remarks'], file_extra_JSON = receiver['file_extra_JSON'])
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,*args, **kwargs):
        id = request.query_params.get("id")
        is_archived = archive_file(file_id= id)
        return Response(status = status.HTTP_200_OK)

class Leave(APIView):
    serializer_class = Leave_serializer
    permission_classes = (AllowAny, )
    def post(self, request):
        user_info = request.data[0]
        receiver_value = User.objects.get(username=user_info['receiver_name'])
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        serializer = self.serializer_class(data = request.data[1])
        if serializer.is_valid():
            serializer.save()
            file_id = create_file(uploader = user_info['uploader_name'], uploader_designation = user_info['uploader_designation'], receiver = user_info['receiver_name'], receiver_designation=obj.name, src_module="HR", src_object_id= str(serializer.data['id']), file_extra_JSON= {"type": "LTC"}, attached_file= None)
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        pk = request.query_params.get("name")
        try: 
            forms = Leaveform.objects.get(created_by =  pk)           
            serializer = self.serializer_class(forms, many = False)
        except MultipleObjectsReturned:
            forms = Leaveform.objects.filter(created_by =  pk)
            serializer = self.serializer_class(forms, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        pk = request.query_params.get("id")
        receiver = request.data[0]
        send_to = receiver['receiver']
        receiver_value = User.objects.get(username=send_to)
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        form = Leaveform.objects.get(id = pk)
        serializer = self.serializer_class(form, data = request.data[1])
        if serializer.is_valid():
            serializer.save()
            forward_file(file_id = receiver['file_id'], receiver = receiver['receiver'], receiver_designation = obj.name, remarks = receiver['remarks'], file_extra_JSON = receiver['file_extra_JSON'])
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,*args, **kwargs):
        id = request.query_params.get("id")
        is_archived = archive_file(file_id= id)
        return Response(status = status.HTTP_200_OK)

class Appraisal(APIView):
    serializer_class = Appraisal_serializer
    permission_classes = (AllowAny, )
    def post(self, request):
        user_info = request.data[0]
        receiver_value = User.objects.get(username=user_info['receiver_name'])
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        serializer = self.serializer_class(data = request.data[1])
        if serializer.is_valid():
            serializer.save()
            file_id = create_file(uploader = user_info['uploader_name'], uploader_designation = user_info['uploader_designation'], receiver = user_info['receiver_name'], receiver_designation=obj.name, src_module="HR", src_object_id= str(serializer.data['id']), file_extra_JSON= {"type": "LTC"}, attached_file= None)
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        pk = request.query_params.get("name")
        print(pk)
        try: 
            forms = Appraisalform.objects.get(created_by =  pk)           
            serializer = self.serializer_class(forms, many = False)
        except MultipleObjectsReturned:
            forms = Appraisalform.objects.filter(created_by =  pk)
            serializer = self.serializer_class(forms, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        pk = request.query_params.get("id")
        form = Appraisalform.objects.get(id = pk)
        send_to = request.query_params.get("send_to")
        receiver_value = User.objects.get(username=send_to)
        receiver_value_designation= HoldsDesignation.objects.filter(user=receiver_value)
        lis = list(receiver_value_designation)
        obj=lis[0].designation
        serializer = self.serializer_class(form, data = request.data)
        if serializer.is_valid():
            serializer.save()
            forward_file(file_id = id, receiver = send_to, receiver_designation = obj.name, remarks = request.data['remarks'], file_extra_JSON = request.data['file_extra_JSON'])
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,*args, **kwargs):
        id = request.query_params.get("id")
        is_archived = archive_file(file_id= id)
        return Response(status = status.HTTP_200_OK)
        
# class Forward(APIView):
#     def post(self, request, *args, **kwargs):
#         forward_file(file_id = request.data['file_id'], receiver = request.data['receiver'], receiver_designation = 'hradmin', remarks = request.data['remarks'], file_extra_JSON = request.data['file_extra_JSON'])
#         return Response(status = status.HTTP_200_OK)

class GetForms(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, *args, **kwargs):
        form_type = request.query_params.get("type")
        id = request.query_params.get("id")
        if form_type == "LTC":
            try: 
                forms = LTCform.objects.get(created_by =  id)           
                serializer = LTC_serializer(forms, many = False)
            except MultipleObjectsReturned:
                forms = Leaveform.objects.filter(created_by =  id)
                serializer = LTC_serializer(forms, many = True)
        elif form_type == "CPDAReimbursement":
            try: 
                forms = CPDAReimbursementform.objects.get(created_by =  id)           
                serializer = CPDAReimbursement_serializer(forms, many = False)
            except MultipleObjectsReturned:
                forms = CPDAReimbursementform.objects.filter(created_by =  id)
                serializer = CPDAReimbursement_serializer(forms, many = True)
        elif form_type == "CPDAAdvance":
            try: 
                forms = CPDAAdvanceform.objects.get(created_by =  id)           
                serializer = CPDAAdvance_serializer(forms, many = False)
            except MultipleObjectsReturned:
                forms = CPDAAdvanceform.objects.filter(created_by =  id)
                serializer = CPDAAdvance_serializer(forms, many = True)
        elif form_type == "Appraisal":
            try: 
                forms = Appraisalform.objects.get(created_by =  id)           
                serializer = Appraisal_serializer(forms, many = False)
            except MultipleObjectsReturned:
                forms = Appraisalform.objects.filter(created_by =  id)
                serializer = Appraisal_serializer(forms, many = True)
        elif form_type == "Leave":
            try: 
                forms = Leaveform.objects.get(created_by =  id)           
                serializer = Leave_serializer(forms, many = False)
            except MultipleObjectsReturned:
                forms = Leaveform.objects.filter(created_by =  id)
                serializer = Leave_serializer(forms, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
# class TrackProgress(APIView):
#     permission_classes = (AllowAny, )
#     def get(self, request, *args, **kwargs):
#         file_id = request.query_params.get("id")
#         progress = view_history(file_id)
#         print(progress)
#         return Response(status = status.HTTP_200_OK)