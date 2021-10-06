"""
Tasks to download and process recordings
"""
import os
import subprocess as sp
import time

import requests
from asgiref.sync import async_to_sync
from lassarAPI.celery import app
from lassarAPI.settings import (MEDIA_ROOT, RECORDS_PATH,
                                    VIDEO_PROCESSOR_PATH,
                                    VIDEO_PROCESSOR_THREADS)
from celery import shared_task
from channels.layers import get_channel_layer
from django.http import JsonResponse

from record.models import Record
from record.serializers import RecordSocketSerializer


@shared_task
def download_video(url,dir_path):
    """download video from url

    :url: url from download video
    :dir_path: base dir which will placed video
    :returns: filesystem path to video

    """
    response = requests.get(url)


    name = os.path.join(dir_path,"{}.webm".format(time.time()))
    with open(name,"wb") as _fb:
        _fb.write(response.content)

    return name

@app.task
def process_video(processor_path,meeting_path,video_output):
    """
    process a video
    """
    output_video_path = os.path.join(video_output,"{}.mp4".format(time.time()))
    cmd = "node {} -i {} -t {} -o {}".format(processor_path,VIDEO_PROCESSOR_THREADS, meeting_path,output_video_path)
    with sp.Popen(cmd.split()) as process:
        process.wait()


    return output_video_path
@app.task
def end_process_record(record_path, record_id):
    """callback function to update status and video path of model Record

    :record_path: TODO
    :record_id: TODO
    :returns: TODO

    """
    record = Record.objects.get(meeting_id=record_id)
    record.status = record.status_choices.Completed
    record.video = record_path
    record.save()

    data = {"status":Record.status_choices.Completed,
            "status_message":"",
            "meeting_id":record_id
            }
    serializer = RecordSocketSerializer(data=data)
    serializer.is_valid()
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(record_id,{
            "type": "record.message",
            "meeting_id": record_id,
        })


def start_process_record(record_id):
    """TODO: Docstring for handle_new_record.

    :meeting_path: TODO
    :returns: TODO

    """
    meeting_path = os.path.join(RECORDS_PATH,record_id)
    # check if meeting exists

    if not os.path.exists(meeting_path):
        record = Record.objects.get(meeting_id=record);
        record.status = record.status_choices.NotFound
        record.save()
    else:
        async_result = process_video.apply_async(
                (VIDEO_PROCESSOR_PATH,meeting_path,MEDIA_ROOT),
                link=end_process_record.s(record_id)
                )

    return async_result
