from django.urls import path
from django.contrib import admin
from issues.views import IssuesView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('issues/', IssuesView.as_view(), name = 'issues'),
]
