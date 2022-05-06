from dataclasses import fields
from rest_framework import serializers
from issues.models import Issues

class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'