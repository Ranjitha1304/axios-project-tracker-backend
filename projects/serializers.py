# projects/serializers.py
from rest_framework import serializers
from .models import MiniProject
from django.contrib.auth.models import User

class MiniProjectSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.ReadOnlyField(source='assigned_to.username')
    assigned_by_username = serializers.ReadOnlyField(source='assigned_by.username')

    class Meta:
        model = MiniProject
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_to_username',
            'assigned_by', 'assigned_by_username', 'priority', 'status',
            'due_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['assigned_by', 'created_at', 'updated_at', 'assigned_by_username', 'assigned_to_username']
