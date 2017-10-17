# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from .views import channels as channels_views


channels_urls = [
    #url(
    #    r'^(?P<channel>\w+)$',
    #    channels_views.Channel.as_view(),
    #    name='channel'),
    url(
        r'^(?P<channel>\w+)/embed$',
        channels_views.ChannelEmbed.as_view(),
        name='channel'),
]

urlpatterns = [
    url(r'^channels/', include(channels_urls, namespace='channels')),
]

