from rest_framework import serializers

from record.models import Record


class RecordSerializer(serializers.ModelSerializer):

    class Meta:

        model = Record
        fields = ["meeting_id","status"]
class RecordDownloadSerializer(serializers.ModelSerializer):

    """Docstring for RecordDownloadSerializer. """

    class Meta:

        model = Record
        fields = ["meeting_id","video"]



class RecordSocketSerializer(serializers.Serializer):
    meeting_id = serializers.CharField(max_length=128)
    status = serializers.IntegerField()
    status_message = serializers.CharField(max_length=128)

class RecordPostSerializer(serializers.Serializer):
    url = serializers.URLField()
class RecordRequestSerializer(serializers.Serializer):
    meeting_id = serializers.CharField(max_length=128)
