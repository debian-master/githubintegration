from dataclasses import fields
from tkinter import Label
from rest_framework import serializers
from issues.models import Issues, Labels, Assignee

class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = '__all__'

class AssigneeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Assignee
        fields = '__all__'

class IssuesSerializer(serializers.ModelSerializer):
    labels = LabelsSerializer(many=True, read_only=True)
    assignee = AssigneeSerializers(many=True, read_only=True)
    class Meta:
        model = Issues
        fields = '__all__'