from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('upload-dem/', views.upload_file, name="form-upload"),
]
