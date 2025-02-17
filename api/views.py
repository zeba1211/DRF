from django.shortcuts import render
from rest_framework import viewsets
from api.models import Company,Employee
from api.serializers import CompanySerializer,EmployeeCreateSerializer, EmployeeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import generics


class CompanyViewSet(viewsets.ModelViewSet):
    queryset= Company.objects.all()
    serializer_class=CompanySerializer

        
    @action(detail=True,methods=['get'])
    def employees(self,request,pk=None):
        try: 
            company=Company.objects.get(pk=pk)
            emps=Employee.objects.filter(company=company)
            emps_serializer=EmployeeSerializer(emps,many=True,context={'request':request})
            return Response(emps_serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'message':'Company might not exists !! Error'
            })

# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeCreateSerializer

    def get_serializer_class(self):
        if self.request.method=='POST':
            return EmployeeCreateSerializer
        return EmployeeSerializer
    

class EmployeeUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    lookup_field='id'
    
    