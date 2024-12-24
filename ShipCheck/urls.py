"""
URL configuration for ShipCheck project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('camera/', views.camera_view, name='camera'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employee/register/', views.add_employee, name='add_employee'),
    path('employee/view/', views.EmployeeHTMxTableView.as_view(), name='view_employee_list'), 
    path('employee/', views.EmployeeHTMxTableView.as_view(), name='employee_htmx'),       
    path('save_face/', views.save_face, name='save_face'),
    path('save_face_embedding/', views.save_face_embedding, name='save_face_embedding'),
    path('get_saved_face_embeddings/', views.get_saved_face_embeddings, name='get_saved_face_embeddings'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)