from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format=r'%Y-%m-%d')
    class Meta:
        model = File
        fields = ('id', 'name', 'size', 'path', 'date_created', 'is_folder')


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('id', 'name', 'total_size', 'path', 'is_folder')


class DupeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = DupeGroup
        fields = ('checksum', 'files', 'file_size', 'file_count')


class FileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileType
        fields = ('id', 'extension', 'total_size')


class FileSummarySerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format=r'%Y-%m-%d %H:%M')
    class Meta:
        model = FileSummary
        fields = ('id', 'timestamp', 'folder_count', 'file_count', 
            'duplicate_count', 'total_size', 'size_timeline_data', 'type_chart_data')
