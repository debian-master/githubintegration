from __future__ import unicode_literals
from ast import Assign
from pydoc import describe
from re import template
from urllib import response
from django.shortcuts import render, redirect
from django.views import View
# from django.views.generic.list import ListView
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
import requests
import json
from django.db.models import Q
from rest_framework.response import Response
from .models import Labels, Issues, Assignee
from .serializers import IssuesSerializer
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required

class IssuesFetchView(View):
    '''This View will fetch the data from GitHub-Apis and will store it into database'''
    def get(self,request,*args,**kwargs):
        try:
            iterations = 1
            tmp = 'issues/issues-list.jinja'
            social_user = UserSocialAuth.objects.all().values('extra_data')
            social_user_auth = social_user[0]['extra_data']['access_token']
            headers = {
            'Authorization': f'Bearer {social_user_auth}'
            }
            page_no = 1
            state = 'open'
            while iterations > 0:
                url = f"https://api.github.com/repos/pallets/click/issues?state={state}&per_page=100\
                        &page={page_no}"
                page_no += 1
                req = requests.request("GET", url, headers=headers)
                json_req = req.json()
                if state=='closed' and not json_req:
                    break
                if not json_req:
                    state = 'closed'
                    page_no=1
                print(url)
                for issue in json_req:
                    issues = Issues.objects.filter(id=issue['id']).exists()
                    if not issues:
                        create_issues = Issues.objects.create(
                                        id=issue['id'], number= issue['number'],title=issue['title'],
                                        state=issue['state'],created_at=issue['created_at'],update_at=issue['updated_at'],
                                        issues_html_url=issue['html_url']
                        )
                    else:
                        create_issues = Issues.objects.get(id=issue['id'])
                    if issue['labels']:
                        for label in issue['labels']:     
                            # create_issues = Issues.objects.get(id=issue['id'])
                            labels_add = Labels.objects.get(id=label['id'])
                            create_issues.labels.add(labels_add)
                            create_issues.save()
                    # print(issue['assignees'])
                    if issue['assignees']:
                        for assignee in issue['assignees']:      
                            # create_issues = Issues.objects.get(id=issue['id'])
                            assignee_add = Assignee.objects.filter(id=assignee['id']).exists()
                            if not assignee_add:
                                self.assignees_save()
                                assignee_add = Assignee.objects.filter(id=assignee['id'])
                            create_issues.assignee.add(assignee_add)
                            create_issues.save()
            self.assignees_save()
            self.label_save()
        except Exception as e:
            print(e)
        return render(request, tmp)
        

    def label_save(*args):
        social_user = UserSocialAuth.objects.all().values('extra_data')
        social_user_auth = social_user[0]['extra_data']['access_token']
        headers = {
            'Authorization': f'Bearer {social_user_auth}'
        }
        url = "https://api.github.com/repos/pallets/click/labels"
        req_labels = requests.request("GET", url, headers=headers)
        json_labels = req_labels.json()
        for label in json_labels:
            labels = Labels.objects.filter(node_id=label['node_id']).exists()
            if not labels:
                Labels.objects.create(
                        id=label['id'], name=label['name'], node_id=label['node_id'],
                        description=label['description']
                )
        return 0

    def assignees_save(*args):
        social_user = UserSocialAuth.objects.all().values('extra_data')
        social_user_auth = social_user[0]['extra_data']['access_token']
        headers = {
            'Authorization': f'Bearer {social_user_auth}'
        }
        page_no = 2
        url = f"https://api.github.com/repos/pallets/click/issues?state=closed&per_page=100&page={page_no}"
        req_assignees = requests.request("GET", url, headers=headers)
        json_assignee = req_assignees.json()
        for issue in json_assignee:
            for assignee in issue['assignees']:
                assignees = Assignee.objects.filter(id=assignee['id']).exists()
                if not assignees:
                    Assignee.objects.create(
                            id=assignee['id'],name=assignee['login'],html_url=assignee['html_url']
                    )
        return 0


class Login(View):
    def get(self, request, *args, **kwargs):
        tmp = 'issues/login.jinja'
        return redirect('/oauth/login/github')

class RateLimit(View):
    def get(self, request, *args, **kwargs):
        social_user = UserSocialAuth.objects.all().values('extra_data')
        social_user_auth = social_user[0]['extra_data']['access_token']
        headers = {
                'Authorization': f'Bearer {social_user_auth}'
        }
        ctx = {}
        tmp = 'issues/rate-limit.jinja'
        url_ratelimit = "https://api.github.com/rate_limit"
        req_rate_limit = requests.request("GET", url_ratelimit, headers=headers)
        json_req_rate_limit = req_rate_limit.json()
        ctx['rate_limit'] = json_req_rate_limit
        return render(request, tmp, context=ctx)


class IssuesView(APIView):
    def get(self, request, *args, **kwargs):
        context = {}
        issues = Issues.objects.all().order_by('-created_at')
        serializer = IssuesSerializer(issues, many=True)
        context['issues'] = serializer.data
        context['labels'] = Labels.objects.all()
        context['assignees'] = Assignee.objects.all()
        return render(request, 'issues/issues-list.jinja', context=context)

class AjaxIssues(APIView):
    def get(self,request,*args, **kwargs):
        issues = Issues.objects.all().order_by('-created_at')
        data = request.GET
        print(data)
        if data:
            if data.get('state'):
                issues = issues.filter(state=data.get('state'))
            if data.get('state')=='all':
                issues = Issues.objects.all().order_by('-created_at')
            if data.get('labels'):
                issues = issues.filter(labels=data.get('labels'))
            if data.get('assignee'):
                issues = issues.filter(assignee=data.get('assignee'))
        serializer = IssuesSerializer(issues, many=True)
        return Response(serializer.data)
    