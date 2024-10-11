from rest_framework import serializers
from imagetotext.models import OcrAws, LANGUAGE_CHOICES, STYLE_CHOICES

class OcrAwsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcrAws
        fields = ['id', 'image', 'text']