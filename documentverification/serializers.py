from rest_framework import serializers
from .models import UploadedDocument, ExtractedData

class ExtractedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedData
        fields = '__all__'

class UploadedDocumentSerializer(serializers.ModelSerializer):
    extracted_data = ExtractedDataSerializer(read_only=True)

    class Meta:
        model = UploadedDocument
        fields = '__all__'
