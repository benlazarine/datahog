import datetime
import csv

from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework import views, pagination, generics, filters

from .models import *
from .serializers import *
from .helpers import create_size_timeline_data, create_type_chart_data, filter_files, EchoBuffer


class GetBiggestFiles(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('size',)
    ordering = ('-size',)


class GetBiggestFolders(generics.ListAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('total_size',)
    ordering = ('-total_size',)


class GetBiggestFileTypes(generics.ListAPIView):
    queryset = FileType.objects.all()
    serializer_class = FileTypeSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('total_size',)
    ordering = ('-total_size',)


class GetBiggestDupeGroups(generics.ListAPIView):
    queryset = DupeGroup.objects.all()
    serializer_class = DupeGroupSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('file_size',)
    ordering = ('-file_size',)


class GetMostDuped(generics.ListAPIView):
    queryset = DupeGroup.objects.all()
    serializer_class = DupeGroupSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('file_count',)
    ordering = ('-file_count',)


class GetChildrenOfFolder(views.APIView):
    def get(self, request, folder_id):
        try:
            parent_folder = Folder.objects.get(pk=folder_id)
        except Folder.DoesNotExist:
            return Response('That folder does not exist!', status=404)
        
        child_folders = Folder.objects.filter(parent=parent_folder)
        child_files   = File.objects.filter(parent=parent_folder)

        folder_serializer = FolderSerializer(child_folders.all(), many=True)
        file_serializer   = FileSerializer(child_files.all(), many=True)

        return Response(folder_serializer.data + file_serializer.data)


class GetTopLevelFiles(views.APIView):
    def get(self, request):
        
        top_folders = Folder.objects.filter(parent=None)
        top_files   = File.objects.filter(parent=None)

        folder_serializer = FolderSerializer(top_folders.all(), many=True)
        file_serializer   = FileSerializer(top_files.all(), many=True)

        return Response(folder_serializer.data + file_serializer.data)


class SearchFiles(views.APIView):
    def get(self, request):
        matching_files = filter_files(File.objects, request.GET)

        if 'offset' in request.GET:
            offset = int(request.GET['offset'])
            matching_files = matching_files.all()[offset:offset+100]
        else:
            matching_files = matching_files.all()[:100]
        
        files_serialized = FileSerializer(matching_files, many=True)
        return Response(files_serialized.data)


class GetSearchCSV(views.APIView):
    def get(self, request):
        matching_files = filter_files(File.objects, request.GET)
        writer = csv.writer(EchoBuffer())

        def get_csv_rows():
            for file in matching_files.all():
                yield writer.writerow([
                    file.path,
                    str(file.date_created),
                    str(file.size)
                ])

        response = StreamingHttpResponse(get_csv_rows(), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        return response


class GetFileSummary(views.APIView):
    def get(self, request):
        try:
            summary = FileSummary.objects.latest('timestamp')
        except FileSummary.DoesNotExist:
            summary = FileSummary.objects.create()
        
        if not summary.size_timeline_data:
            summary.size_timeline_data = create_size_timeline_data()
        if not summary.type_chart_data:
            summary.type_chart_data = create_type_chart_data()
        summary.save()
        
        summary_serialized = FileSummarySerializer(summary)
        return Response(summary_serialized.data)
