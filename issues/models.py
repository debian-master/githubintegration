# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Labels(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Assignee(models.Model):
    name = models.CharField(max_length=255)
    html_url = models.CharField(max_length=255)
    reference_id = models.IntegerField()

class Issues(models.Model):
    title = models.CharField(max_length=500, blank=True)

    # username = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()
    issues_html_url = models.CharField(max_length=500, blank=True)
    # issue_reference_id = models.IntegerField()
    # user_html_url = models.CharField(max_length=500, blank=True)
    labels = models.ManyToManyField(Labels)
    assignee = models.ManyToManyField(Assignee)
