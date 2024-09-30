from django.contrib import admin
from django.urls import path, include
from migration_tool.views import index  # Import the index view

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface URL
    path('', index, name='index'),    # Root URL mapped to the index view
    path('api/', include('migration_tool.urls')),  # Includes the URLs from the migration_tool app
]
