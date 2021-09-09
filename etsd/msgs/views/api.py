from .. import models, serializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, authentication, permissions
from . import ParticipantQuerysetMixin, MessageAccessMixin


class IsAuthenticatedAllowOptions(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        return super().has_permission(request, view)


class ParticipantViewSet(ParticipantQuerysetMixin, viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticatedAllowOptions]
    serializer_class = serializers.ParticipantSerializer
    queryset = models.Participant.objects.all()


class MessageViewSet(MessageAccessMixin, viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticatedAllowOptions]
    serializer_class = serializers.MessageSerializer
    queryset = models.Message.objects.all()
