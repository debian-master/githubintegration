# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
import requests
import json

class IssuesView(View):
    def get(self,request,*args,**kwargs):
        req = requests.get("https://api.github.com/repos/pallets/click/issues")
        json_req = req.json()
        return JsonResponse(json_req, safe=False)