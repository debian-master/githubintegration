from django.conf.urls import url
from django.contrib import admin
from issues.views import IssuesView
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'issues/', IssuesView.as_view(), name = 'issues'),
]
