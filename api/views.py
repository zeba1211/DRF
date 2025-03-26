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
# import logging




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

            #logger.info(f"Employees for company {company.name} from IP: {request.META.get('REMOTE_ADDR')}")
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
# logger = logging.getLogger(__name__)


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
        
        # Log GET requests
        # logger.info(f"Employee list viewed by{request.user} from IP: {request.META.get('REMOTE_ADDR')}")
        return super().get(request, *args, **kwargs)
    

    @silk_profile(name="creating employee")
    def post(self, serializers):
            # Log POST requests
            # logger.info(f"Employee created with data: {serializers}")
            return super().post(serializers)



class EmployeeUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    #module throttling 100/hour for update and delete emp
    throttle_classes=[AnonRateThrottle,empRateThrottle]
    

    @silk_profile(name="fetching employee")
    def get(self, request, *args, **kwargs):
        # Log GET requests
        # logger.info(f"Employee retrived (ID:{kwargs['pk']})by {request.user}from IP {request.META.get('REMOTE_ADDR')}")

        return super().retrieve(request, *args, **kwargs)
    
    

    @silk_profile(name="updating employee")
    def put(self, request, *args, **kwargs):
        # Log PUT requests (update)
        # logger.info(f"Employee updated (ID:{kwargs['pk']})with data:{request.data} by{request.user}from IP {request.META.get('REMOTE_ADDR')}")

        return super().update(request, *args, **kwargs)
    

    @silk_profile(name="updating employee")
    def patch(self, request, *args, **kwargs):
        # Log PATCH requests (partial update)
        # logger.info(f"Employee partially updated (ID:{kwargs['pk']})with data:{request.data} by{request.user}from IP {request.META.get('REMOTE_ADDR')}")
        return super().partial_update(request, *args, **kwargs)
    

    @silk_profile(name="deleting employee")
    def delete(self, request, *args, **kwargs):
        # Log DELETE requests
        # logger.info(f"Employee deleted (ID:{kwargs['pk']}) by {request.user} from IP: {request.META.get('REMOTE_ADDR')}")
        return super().destroy(request, *args, **kwargs)





# from django.shortcuts import render
# from .models import Request  # Assuming you have a Request model to track request data
# from silk.profiling.profiler import silk_profile

# # View function to render the summary page and pass data
# def summary_view(request):
#     # Fetch data for the chart
#     # Assuming you have a model or data source from which you fetch the request counts, durations, or other data
#     # For example, let's use sample data for the chart

#     # Sample data for the chart (replace with actual logic to fetch data from your database)
#     chart_labels = ['Request 1', 'Request 2', 'Request 3', 'Request 4']
#     chart_data = [100, 200, 300, 400]  # Example data for the chart
    
#     # Get the necessary statistics from the database
#     num_requests = Request.objects.count()  # Example: Total number of requests
#     num_profiles = 50  # Example: Total number of profiles
#     avg_overall_time = 120.5  # Example: Average overall time
#     avg_num_queries = 12.4  # Example: Average number of queries
#     avg_time_spent_on_queries = 35.2  # Example: Average time spent on queries

#     # Fetch some data for the views like 'longest_queries_by_view' and 'most_time_spent_in_db'
#     longest_queries_by_view = Request.objects.order_by('-duration')[:5]  # Example: Longest 5 queries
#     most_time_spent_in_db = Request.objects.order_by('-db_time')[:5]  # Example: Most time spent in DB
#     most_queries = Request.objects.order_by('-num_queries')[:5]  # Example: Most queries

#     # Pass all the data to the template
#     context = {
#         'chart_labels': chart_labels,
#         'chart_data': chart_data,
#         'num_requests': num_requests,
#         'num_profiles': num_profiles,
#         'avg_overall_time': avg_overall_time,
#         'avg_num_queries': avg_num_queries,
#         'avg_time_spent_on_queries': avg_time_spent_on_queries,
#         'longest_queries_by_view': longest_queries_by_view,
#         'most_time_spent_in_db': most_time_spent_in_db,
#         'most_queries': most_queries,
#     }

#     return render(request, 'summary.html', context)

# views.py
from django.shortcuts import render
from django.db.models import Avg
from silk.models import Request , Profile# Adjust import based on your project structure

def chart_page(request):
    total_requests = Request.objects.count()
    total_profiles = Profile.objects.count()

    total_response_time=0
    total_query_time=0
    total_query_count=0

    profiles=Profile.objects.all()

    for profile in profiles:
        total_response_time+=profile.time_taken or 0

        queries=profile.queries.all()
        total_query_count+=queries.count()

        total_query_time+=sum(q.time_taken for q in queries)

    avg_response_time=total_response_time / total_profiles if total_profiles else 0
    avg_query_time=total_query_time / total_profiles if total_profiles else 0
    avg_num_queries=total_query_count / total_profiles if total_profiles else 0

    data = {
    'chart_data': {
        'requests': total_requests,
        'profiles': total_profiles,
        'avg_overall_time': round(avg_response_time * 1000, 2),
        'avg_num_queries': round(avg_num_queries, 2),
        'avg_time_spent_on_queries': round(avg_query_time * 1000, 2),
    }
}
    return render(request, 'chart_page.html', data)


    # # Assuming you are gathering data from Silk's request logs
    # num_requests = Request.objects.count()
    # num_profiles = Request.objects.count()
    
    # # Example of gathering time statistics from Silk logs
    # avg_overall_time = Request.objects.aggregate(Avg('duration'))['duration__avg']
    # avg_num_queries = Request.objects.aggregate(Avg('num_queries'))['num_queries__avg']
    # avg_time_spent_on_queries = Request.objects.aggregate(Avg('db_duration'))['db_duration__avg']
    
    # # Prepare data for Chart.js (request, response, avg db time, etc.)
    # chart_data = {
    #     'requests': [num_requests],  # Example data, can be customized
    #     'response_time': [avg_overall_time],
    #     'avg_db_time': [avg_time_spent_on_queries],
    #     'api': [num_profiles]  # API count can be based on profiles, for example
    # }

    # return render(request, 'chart_page.html', {
    #     'num_requests': num_requests,
    #     'num_profiles': num_profiles,
    #     'avg_overall_time': avg_overall_time,
    #     'avg_num_queries': avg_num_queries,
    #     'avg_time_spent_on_queries': avg_time_spent_on_queries,
    #     'chart_data': chart_data
    # })





# def chart_page(request):
#     # Example data, replace with actual dynamic data as needed
#     chart_data = {
#         'requests': 20,
#         'profiles': 50,
#         'avg_overall_time': 120,
#         'avg_num_queries': 8,
#         'avg_time_spent_on_queries': 60,
#     }
#     return render(request, 'chart_page.html', {'chart_data': chart_data})