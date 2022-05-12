from django.urls import path, include
from django.contrib import admin

from issues.views import IssuesFetchView, Login, RateLimit, IssuesView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('issues-fetch/', IssuesFetchView.as_view(), name = 'issues'),
    path('login/', Login.as_view(), name="login"),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('rate-limit/', RateLimit.as_view(), name= 'rate-limit'),
    path('issues/', IssuesView.as_view(), name = 'issues'),
]
