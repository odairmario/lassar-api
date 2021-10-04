import hashlib
import shutil
import time
import unittest
from os import makedirs, path
from unittest import mock

import requests
import responses
from bbbrecord_api.settings import VIDEO_PROCESSOR_PATH
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from record.models import Record
from record.tasks import (end_process_record, process_video,
                          start_process_record)
from record.views import search

# Create your tests here.

def calc_checksum(file_path):
    """calc checksum from file

    :file_path: TODO
    :returns: TODO

    """
    with open(file_path,"rb") as _file:
        checksum = hashlib.md5(_file.read()).hexdigest()

    return checksum

class RecordTasksTestCase(TestCase):

    """Record test case class"""

    def setUp(self):
        """setup record class
        :returns: TODO

        """
        self.input_record_direcotry = "record/test_data/record"
        self.output_directory = "/tmp/test_download"
        self.final_video_processed = "record/test_data/processed.mp4"
        self.meeting_id = "bf0a5dbc0b893bebc8d7c76ce2a6dad2617916bf-1630953904626"
        self.url = "http://bbbserver.test/playback/presentation/2.3/{}".format(self.meeting_id)

        makedirs(self.output_directory, exist_ok=True)

    def tearDown(self):
        """TODO: Docstring for setDown.
        :returns: TODO

        """
        shutil.rmtree(self.output_directory, ignore_errors=False, onerror=None)

    def test_process_video(self):
        """test process video
        :returns: TODO

        """
        # calculate checksum from processed video to compare with checksum of video from processed_funtiu
        correct_video_checksum = calc_checksum(self.final_video_processed)

        video_path = process_video(VIDEO_PROCESSOR_PATH,self.input_record_direcotry,self.output_directory)

        video_checksum = calc_checksum(video_path)

        self.assertEqual(correct_video_checksum,video_checksum)


    def test_end_process_record(self):
        Record.objects.create(pk=self.meeting_id)
        end_process_record(self.final_video_processed,self.meeting_id)

        record_final = Record.objects.get(pk=self.meeting_id)
        self.assertTrue(record_final.status == record_final.status_choices.Completed)
        self.assertTrue(record_final.video == self.final_video_processed)

class RecordViewsTestCase(APITestCase):

    """Docstring for RecordViewsTestCase. """
    def setUp(self):
        """TODO: Docstring for setUp.
        :returns: TODO

        """
        self.meeting_id = "bf0a5dbc0b893bebc8d7c76ce2a6dad2617916bf-1630953904626"
        self.url = "http://bbbserver.test/playback/presentation/2.3/{}".format(self.meeting_id)
    def test_search(self):
        """TODO: Docstring for test_search.
        :returns: TODO

        """
        search_url = reverse("search")
        data = {"url":self.url}
        print(self.url)
        response_correct = {"meeting_id":self.meeting_id, "status":"Pending"}

        response = self.client.post(search_url,data,format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK )
        self.assertEqual(Record.objects.count(),1)

        #self.assertJSONEqual(response,response_correct)
