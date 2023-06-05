from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owned_by', 'updated_at', 'created_date']

    def create(self, validated_data):
        validated_data['owned_by'] = self.context['request'].user
        return super(TaskSerializer, self).create(validated_data)
