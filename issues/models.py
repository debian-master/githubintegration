# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Issues(models.Model):
    label = models.CharField(max_length=500)
    user = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()