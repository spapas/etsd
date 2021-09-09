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


class ParticipantSimpleSerializer(serializers.ModelSerializer):
    authority = AuthoritySerializer(read_only=True)

    class Meta:
        model = models.Participant
        fields = ["id", "authority"]


class ParticipantKeySerializer(serializers.ModelSerializer):
    participant = ParticipantSimpleSerializer(read_only=True)

    class Meta:
        model = models.ParticipantKey
        fields = ["id", "participant", "public_key"]


class CipherDataSerializer(serializers.ModelSerializer):
    participant_key = ParticipantKeySerializer(read_only=True)

    class Meta:
        model = models.CipherData
        fields = ["id", "cipher_data", "participant_key"]


class DataSerializer(serializers.ModelSerializer):
    cipher_data = CipherDataSerializer(
        read_only=True,
        source="cipherdata_set",
        many=True,
    )

    class Meta:
        model = models.Data
        fields = ["id", "number", "extension", "cipher_data"]


class MessageSerializer(serializers.ModelSerializer):
    participants = AuthoritySerializer(read_only=True, many=True)
    data = DataSerializer(
        read_only=True,
        source="data_set",
        many=True,
    )

    class Meta:
        model = models.Message
        fields = [
            "id",
            "participants",
            "data",
            "protocol",
            "protocol_year",
        ]
