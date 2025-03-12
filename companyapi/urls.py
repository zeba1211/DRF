"""
URL configuration for companyapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
#silk authentication
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Custom decorator to check if the user is a superuser or staff (admin)
def is_superuser_or_admin(user):
    return user.is_superuser or user.is_staff


# Custom view for Silk access control
@user_passes_test(is_superuser_or_admin, login_url='/admin/login/')
def silk_view(request):
    return redirect('silk:index')  # This assumes the 'silk:index' URL is correct

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('api.urls')),
    # Silk profiling URL with restricted access
    path('silk/', include('silk.urls', namespace='silk')),  # Use the custom view to control access
]
