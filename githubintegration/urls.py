from django.urls import path, include
from django.contrib import admin

from issues.views import IssuesFetchView, Login, RateLimit, IssuesView, AjaxIssues
urlpatterns = [
    path('admin/', admin.site.urls),
    path('issues-fetch/', IssuesFetchView.as_view(), name = 'issues'),
    path('', Login.as_view(), name="login"),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('rate-limit/', RateLimit.as_view(), name= 'rate_limit'),
    path('issues/', IssuesView.as_view(), name = 'issues'),
    path('ajax_issues/', AjaxIssues.as_view(), name = 'ajax_call_issues'),
]