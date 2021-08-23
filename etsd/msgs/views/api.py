from .. import models, serializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, authentication, permissions
from . import ParticipantQuerysetMixin


class MessageViewSet(ParticipantQuerysetMixin, viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ParticipantSerializer
    queryset = models.Participant.objects.all()
