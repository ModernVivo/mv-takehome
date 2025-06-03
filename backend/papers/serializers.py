from rest_framework import serializers
from .models import Paper

class PaperListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ['id', 'title', 'authors']

class PaperDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = '__all__'
