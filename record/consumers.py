import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.renderers import JSONRenderer

from record.models import Record
from record.serializers import RecordRequestSerializer, RecordSocketSerializer


class RecordConsumer(JsonWebsocketConsumer):
    def connect(self):
        #self.meeting_id = self.scope['url_route']['kwargs']['meeting_id']

        ## check if record is already process
        #record = Record.objects.get(pk=self.meeting_id)

        #if record.is_processed():
        #    self.close()
        #else:
        #    # Join room group
        #    async_to_sync(self.channel_layer.group_add)(
        #        self.meeting_id,
        #        self.channel_name
        #    )

        self.accept()

    def receive(self, text_data):
        """TODO: Docstring for receive.

        :content: TODO
        :returns: TODO

        """
        content = json.loads(text_data)
        serializer =  RecordRequestSerializer(data=content)

        if not serializer.is_valid():
            return;
        data = serializer.validated_data
        meeting_id = data.get("meeting_id")
        print(content,data,meeting_id)
        # check if meeting_id exists
        response = { "meeting_id":meeting_id,
                     "status_message":"",
                     "status": Record.status_choices.Pending
                     }
        try:
            record = Record.objects.get(pk=meeting_id)
        except:
            print("nao deveria entrar aqui")
            response["status"] = Record.status_choices.Error
            response["status_message"]= "Recording {} not found".format(meeting_id)
            serializer_response = RecordSocketSerializer(data=response)
            serializer_response.is_valid()
            self.send_json(response)
            #self.send("{'meeting_id':1,'status':2}")

            #self.send("")

            return

        if not record.is_processed():
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                meeting_id,
                self.channel_name
            )

        response["status"] = record.status
        serializer_response = RecordSocketSerializer(data=response)
        serializer_response.is_valid()
        #self.send("{'meeting_id':1,'status':2}")
        print(response)
        self.send_json(response)




    def record_message(self,  event):
        """TODO: Docstring for send_end.

        :meeting_id: TODO
        :returns: TODO

        """
        meeting_id = event["meeting_id"]
        data = {"status":Record.status_choices.Completed,
                "status_message":"",
                "meeting_id":meeting_id
                }
        self.send_json(data)

    def disconnect(self, close_code):
        # Leave room group
        #async_to_sync(self.channel_layer.group_discard)(
        #    self.meeting_id,
        #    self.channel_name
        #)
        pass
