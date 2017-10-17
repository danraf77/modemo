
import json

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers

from channels.models import Channel


class ChannelEmbedSerializer(serializers.ModelSerializer):

    playlist    = serializers.SerializerMethodField()
    logo        = serializers.SerializerMethodField()
    sharing     = serializers.SerializerMethodField()
    stretching  = serializers.SerializerMethodField()
    primary     = serializers.SerializerMethodField()
    width       = serializers.SerializerMethodField()
    height      = serializers.SerializerMethodField()
    aspectratio = serializers.SerializerMethodField()
    aboutlink   = serializers.SerializerMethodField()
    abouttext   = serializers.SerializerMethodField()
    autostart   = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ('playlist', 'logo', 'sharing', 'stretching',
            'primary', 'width', 'height', 'aspectratio', 'aboutlink',
            'abouttext', 'autostart',)

    def get_primary(self, channel):
        return 'flash'

    def get_width(self, channel):
        return '100%'

    def get_height(self, channel):
        return '100%'

    def get_aspectratio(self, channel):
        return '' if channel.only_audio == 'Y' else '16:9'

    def get_aboutlink(self, channel):
        return 'https://iblups.com'

    def get_abouttext(self, channel):
        return 'iblups.com'

    def get_autostart(self, channel):
        return True

    def get_stretching(self, channel):
        return channel.player_stretching

    def get_playlist(self, channel):

        sources = []

        sources.append({ 
                'file': 'rtmp://%s/%s%s' % (channel.nserver, channel.nserverapp, channel.codstream)
              })

        sources.append({
                'file': 'https://cdnh8.iblups.com/hls/%s.m3u8' % channel.codstream,
                'label': '0',
                'type': 'hls',
                'preload': 'none'
            })

        return [{
                'sources': sources
            }]

    def get_logo(self, channel):

        hide = False
        file = 'logoredlive.png'
        link = 'https://iblups.com/%s' % channel.channel

        if channel.logp == 'P':
            file = 'imglogo/%s/.png?id=1.1' % channel.user
        elif channel.logp == 'Y':
            file = 'logo.png'
            link = '#'
            hide = True

        return {
            'file': file,
            'link': link,
            'position': 'top-left',
            'hide': hide
          }

    def get_sharing(self, channel):

        return {
              'code': "<iframe src='https://iblups.com/e_%s' allowfullscreen width=498 height=310 scrolling='no' frameborder='0'></iframe>" % channel.channel,
              'link': 'https://iblups.com/%s' % channel.channel,
              'heading': 'Compartir'
           },


class OfflineChannelEmbedSerializer(ChannelEmbedSerializer):

    class Meta:
        model = Channel
        fields = ChannelEmbedSerializer.Meta.fields + ()

    def to_representation(self, channel):
        ret = super(OfflineChannelEmbedSerializer, self).to_representation(channel)
        ret['type'] = 'mp4'
        ret['skin'] = 'skin/bekle.xml'

        if channel.autoplay != 'Y':
            ret['autostart'] = False

        del ret['aspectratio']
        del ret['stretching']

        if self.device == 'mobile':
            del ret['sharing'] 
            del ret['logo'] 

        return ret

    def get_primary(self, channel):
        return 'html5'

    def get_playlist(self, channel):
        return '%s?channel=%s' % (settings.IBLUPS_RSS_URL, 
                    channel.user,)

    def set_device(self, device):
        self.device = device 
