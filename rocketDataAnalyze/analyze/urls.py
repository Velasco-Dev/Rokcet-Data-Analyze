from django.urls import path
from . import views

app_name = 'analyze'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload'),
    path('file/<int:file_id>/', views.file_analyze, name='file_analyze'),
    path('file/<int:file_id>/delete/', views.delete_file, name='delete_file'),
    path('api/file/<int:file_id>/stats/', views.api_file_stats, name='api_stats'),
]