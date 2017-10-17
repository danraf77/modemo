# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models


class Channel(models.Model):

    """
    pchanel, `user` , channel, nserverm_ams, idchn, levelchan, statair, logp, logp_m,statonline, ppbanevid,  nserverapp, ppbanevidq, autoplay, logop, redic, codstream, nserverm, nservermw, nserver, pplayer, playervalue, skinch, videosp, susp, thumb_channel, player_stretching, player_aspectratio, only_audio, channel_ga
    """

    idchn       = models.IntegerField(primary_key=True)
    channel     = models.CharField(max_length=60)
    codstream   = models.CharField(max_length=60)
    nserverapp  = models.CharField(max_length=60)
    nserver     = models.CharField(max_length=60)
    logp        = models.CharField(max_length=1)
    user        = models.CharField(max_length=60)
    only_audio  = models.CharField(max_length=1)
    player_stretching = models.CharField(max_length=60)
    statair     = models.CharField(max_length=1) 
    autoplay    = models.CharField(max_length=1) 

    class Meta:
        db_table = 'iblupstv_channels'