from django.urls import path
from .views import DepartmentListCreateView, DepartmentRetrieveUpdateDestroyView, ProjectListCreateView, ProjectRetrieveUpdateDestroyView
from . import views

urlpatterns = [
    # Department URLs
    path('department/', DepartmentListCreateView.as_view(), name='department_list_create'),
    path('department/<int:pk>/', DepartmentRetrieveUpdateDestroyView.as_view(), name='department_detail'),

    # Project URLs
    path('project/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('project/<int:pk>/', ProjectRetrieveUpdateDestroyView.as_view(), name='project_detail'),
    
    # Additional views
    path('chart/', views.chart_page2, name='chart_page2'),
]
