# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
import requests
import json

class IssuesView(View):
    def get(self,request,*args,**kwargs):
        ctx = {}
        tmp = 'issues/issues-list.jinja'
        req = requests.get("https://api.github.com/repos/pallets/click/issues?page=1")
        json_req = req.json()
        ctx['issues'] = json_req
        ctx['num'] = 2
        return render(request, tmp, context=ctx)