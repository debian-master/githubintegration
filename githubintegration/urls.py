from django.urls import path, include
from django.contrib import admin

from issues.views import IssuesView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('issues/', IssuesView.as_view(), name = 'issues'),
    path('oauth/', include('social_django.urls', namespace='social')),
]
