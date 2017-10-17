# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response

from channels.models import Channel

from ..mixins import APIView
from ..serializers.channels import (ChannelEmbedSerializer, 
    OfflineChannelEmbedSerializer,)


class ChannelEmbed(APIView):

    authentication_classes = []

    def get_channel(self, channel_name):
        return get_object_or_404(Channel, channel=channel_name)

    def get(self, request, *args, **kwargs):
        id = kwargs.get('channel')
        channel = self.get_channel(id)

        device = request.GET.get('device', 'mobile')

        if channel.statair == 'Y':
            serializer = ChannelEmbedSerializer(channel)
        else:
            serializer = OfflineChannelEmbedSerializer(channel)
            serializer.set_device(device)
        return Response(serializer.data)
        
