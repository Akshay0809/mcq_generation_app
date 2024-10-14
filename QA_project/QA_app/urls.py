

from django.urls import path
from . import views

urlpatterns = [
    path('view', views.upload_pdf, name='upload_pdf'),
    path('download', views.dowload_mcq_pdf, name='download_mcq_pdf'),
]
