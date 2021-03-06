# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Labels(models.Model):
    id = models.BigIntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    node_id = models.CharField(max_length=255, blank=True)

class Assignee(models.Model):
    id = models.BigIntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    url = models.SlugField()


class Issues(models.Model):
    id = models.BigIntegerField(primary_key=True, editable=False)
    title = models.CharField(max_length=500, blank=True)
    number = models.IntegerField(blank=False, null=True)
    # username = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()
    issues_html_url = models.CharField(max_length=500, blank=True)
    # issue_reference_id = models.IntegerField()
    # user_html_url = models.CharField(max_length=500, blank=True)
    labels = models.ManyToManyField(Labels, blank=True)
    assignee = models.ManyToManyField(Assignee, blank=True)
