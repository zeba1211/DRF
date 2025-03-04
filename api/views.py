from silk.profiling.profiler import silk_profile
from django.shortcuts import render
from rest_framework import viewsets
from api.models import Company,Employee
from api.serializers import CompanySerializer,EmployeeCreateSerializer, EmployeeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from django.http import JsonResponse
from rest_framework import serializers

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
#for mudule throttling
from api.throttling import empRateThrottle
import logging




#Model_view_set
class CompanyViewSet(viewsets.ModelViewSet):
    queryset= Company.objects.all()
    serializer_class=CompanySerializer

        
    @action(detail=True,methods=['get'])
    def employees(self,request,pk=None):
        try: 
            company=Company.objects.get(pk=pk)
            emps=Employee.objects.filter(company=company)
            emps_serializer=EmployeeSerializer(emps,many=True,context={'request':request})

            logger.info(f"Employees for company {company.name} from IP: {request.META.get('REMOTE_ADDR')}")
            return Response(emps_serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'message':'Company might not exists !! Error'
            })

# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer


#Generic_view_set
#logger initiate
logger = logging.getLogger(__name__)


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeCreateSerializer
    #apply throttling to employee model for listing and creating employee 3/day
    throttle_classes=[AnonRateThrottle,UserRateThrottle]

    def get_serializer_class(self):
        if self.request.method=='POST':
            return EmployeeCreateSerializer
        return EmployeeSerializer
    @silk_profile(name="fetching employee")
    def get(self, request, *args, **kwargs):
        #with silk_profile(name=f"fetching employee"):
        # Log GET requests
        logger.info(f"Employee list viewed by{request.user} from IP: {request.META.get('REMOTE_ADDR')}")
        return super().get(request, *args, **kwargs)
    @silk_profile(name="creating employee")
    def post(self, serializers):
            #with silk_profile(name=f"creating employee "):
            # Log POST requests
            logger.info(f"Employee created with data: {serializers}")
            return super().post(serializers)



class EmployeeUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    #lookup_field='id'
    #module throttling 100/hour for update and delete emp
    throttle_classes=[AnonRateThrottle,empRateThrottle]
    

    @silk_profile(name="fetching employee")
    def get(self, request, *args, **kwargs):
        #with silk_profile(name=f"fetching employee"):
        # Log GET requests
        logger.info(f"Employee retrived (ID:{kwargs['pk']})by {request.user}from IP {request.META.get('REMOTE_ADDR')}")

        return super().retrieve(request, *args, **kwargs)
    
    

    @silk_profile(name="updating employee")
    def put(self, request, *args, **kwargs):
        #with silk_profile(name=f"updating employee"):
        # Log PUT requests (update)
        logger.info(f"Employee updated (ID:{kwargs['pk']})with data:{request.data} by{request.user}from IP {request.META.get('REMOTE_ADDR')}")

        return super().update(request, *args, **kwargs)
    

    @silk_profile(name="updating employee")
    def patch(self, request, *args, **kwargs):
        #with silk_profile(name=f"updating employee"):
        # Log PATCH requests (partial update)
        logger.info(f"Employee partially updated (ID:{kwargs['pk']})with data:{request.data} by{request.user}from IP {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)
    

    @silk_profile(name="deleting employee")
    def delete(self, request, *args, **kwargs):
        #with silk_profile(name=f"deleting employee"):
        # Log DELETE requests
        logger.info(f"Employee deleted (ID:{kwargs['pk']}) by {request.user} from IP: {request.META.get('REMOTE_ADDR')}")
        return super().destroy(request, *args, **kwargs)






