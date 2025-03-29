from silk.profiling.profiler import silk_profile
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Department, Project
from .serializers import DepartmentSerializer, ProjectSerializer
from django.http import JsonResponse

# Department List and Create View (ListCreateAPIView)
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @silk_profile(name="Fetching department list")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @silk_profile(name="Creating department")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Department Retrieve, Update, and Destroy View (RetrieveUpdateDestroyAPIView)
class DepartmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @silk_profile(name="Fetching department")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @silk_profile(name="Updating department")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @silk_profile(name="Partially updating department")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @silk_profile(name="Deleting department")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

# Project List and Create View (ListCreateAPIView)
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @silk_profile(name="Fetching project list")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @silk_profile(name="Creating project")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Project Retrieve, Update, and Destroy View (RetrieveUpdateDestroyAPIView)
class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @silk_profile(name="Fetching project")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @silk_profile(name="Updating project")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @silk_profile(name="Partially updating project")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @silk_profile(name="Deleting project")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

# Department Performance (Dashboard)
# @silk_profile(name="Department-wise Project Performance")
# def department_performance(request):
#     departments = Department.objects.all()
#     performance_data = []

#     for department in departments:
#         projects = Project.objects.filter(department=department)
#         completed_projects = projects.filter(status="Completed").count()
#         ongoing_projects = projects.filter(status="Ongoing").count()
#         on_hold_projects = projects.filter(status="On Hold").count()

#         performance_data.append({
#             "department": department.name,
#             "completed": completed_projects,
#             "ongoing": ongoing_projects,
#             "on_hold": on_hold_projects,
#         })

#     return render(request, 'department_performance.html', {'performance_data': performance_data})

# # Budget Utilization by Department (Dashboard)
# @silk_profile(name="Budget Utilization by Department")
# def department_budget_utilization(request):
#     departments = Department.objects.all()
#     budget_data = []

#     for department in departments:
#         total_projects = Project.objects.filter(department=department)
#         total_allocated_budget = sum([project.budget_allocated for project in total_projects])
#         budget_utilized = department.budget
#         efficiency = (budget_utilized / total_allocated_budget) * 100 if total_allocated_budget else 0

#         budget_data.append({
#             "department": department.name,
#             "allocated_budget": total_allocated_budget,
#             "utilized_budget": budget_utilized,
#             "efficiency": efficiency,
#         })

#     return render(request, 'department_budget_utilization.html', {'budget_data': budget_data})


from django.shortcuts import render
from django.db.models import Avg
from silk.models import Request , Profile# Adjust import based on your project structure

def chart_page2(request):
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
    return render(request, 'chart_page2.html', data)
