from django.urls import path
from .views import migrate_data

urlpatterns = [
    path('start-migration/', migrate_data, name='start_migration'),  # This should match the endpoint you're calling
]
