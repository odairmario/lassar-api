from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from record.models import Record
from record.serializers import RecordPostSerializer, RecordSerializer
from record.tasks import start_process_record


@api_view(['get'])
@csrf_exempt
def download(request,meeting_id):
    """TODO: Docstring for download.

    :request: TODO
    :returns: TODO

    """
    try:
        record = Record.objects.get(pk=meeting_id)
    except Exception as e:
        return HttpResponse("")
    with open(record.video,"rb") as  _file:
        response = HttpResponse(_file,content_type="application/mp4")
        response["Content-Disposition"] = 'attachment; filename=record.mp4'

    return response


@api_view(['POST'])
@csrf_exempt
def search(request):
    """TODO: Docstring for search_or_create.

    :request: TODO
    :returns: TODO

    """
    serializer_post = RecordPostSerializer(data=request.data)



    serializer_post.is_valid(raise_exception=True)
    data = serializer_post.validated_data

    meeting_id = data.get("url").split("/")[-1]

    try:
        record = Record.objects.get(pk=meeting_id)
    except Exception as e:
        record = Record.objects.create(pk=meeting_id)
        start_process_record(meeting_id)

    serializer = RecordSerializer(record)

    return JsonResponse(serializer.data)
