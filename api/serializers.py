from rest_framework import serializers
from .models import Company,Employee



class CompanySerializer(serializers.HyperlinkedModelSerializer):
    company_id=serializers.ReadOnlyField()
    class Meta:
        model = Company
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    id=serializers.ReadOnlyField()
    class Meta:
        model = Employee
        fields = "__all__"

class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"