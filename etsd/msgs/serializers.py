from rest_framework import serializers
from . import models
from authorities.models import Authority


class AuthoritySerializer(serializers.ModelSerializer):
    kind = serializers.StringRelatedField()

    class Meta:
        model = Authority
        fields = ["id", "name", "code", "kind", "email", "is_active"]


class ParticipantMessageSerializer(serializers.ModelSerializer):
    participants = AuthoritySerializer(read_only=True, many=True)

    class Meta:
        model = models.Message
        fields = "__all__"


class ParticipantSerializer(serializers.ModelSerializer):
    message = ParticipantMessageSerializer(read_only=True)

    class Meta:
        model = models.Participant
        fields = ["id", "message_id", "status", "message"]


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Data
        fields = [
            "id", "number", "extension"
        ]


class MessageSerializer(serializers.ModelSerializer):
    participants = AuthoritySerializer(read_only=True, many=True)
    data = DataSerializer(read_only=True, source="data_set", many=True, )

    class Meta:
        model = models.Message
        fields = [
            "id",
            "participants",
            "data",
        ]
