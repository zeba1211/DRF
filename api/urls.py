from django.contrib import admin
from django.urls import path,include
from api.views import CompanyViewSet#,EmployeeViewSet
from rest_framework.routers import DefaultRouter
from .views import EmployeeListCreateView, EmployeeUpdateDestroyView
from . import views

router= DefaultRouter()
router.register('companies',CompanyViewSet)
#router.register(r'employees',EmployeeViewSet)

urlpatterns = [
    path('',include(router.urls)),
      # This is the view for the home page

    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeUpdateDestroyView.as_view(),name='employee-details'),
  #custome chart.js URL

]