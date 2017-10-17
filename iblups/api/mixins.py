# -*- coding: utf-8 -*-

import re
import json
import jwt
import requests

from datetime import datetime
from collections import namedtuple

from dateutil.parser import parse
from dateutil.tz import tzutc

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser

from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView as rest_APIView


token_pattern = re.compile(r'^Token ([a-z-A-Z-0-9\_\.]*)$')


AUTHORIZATION_HEADER_REQUIRED = 'Authorization Header Required'
MALFORMED_AUTHORIZATION_HEADER = 'Malformed Authorization Header'


class TokenAuthentication(BasicAuthentication):

    def authenticate(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION', None)

        if authorization_header is None:
            raise exceptions.AuthenticationFailed(
                AUTHORIZATION_HEADER_REQUIRED)
        _match = token_pattern.match(authorization_header)

        if not _match:
            raise exceptions.AuthenticationFailed(
                MALFORMED_AUTHORIZATION_HEADER)

        access_token = _match.groups()[0]

        if access_token == settings.IBLUPS_ACCESS_TOKEN:
            return None, None
        else:
            raise exceptions.AuthenticationFailed('Invalid Token')

    def authenticate_header(self, request):
        return 'Token'


class APIView(rest_APIView):

    authentication_classes = [TokenAuthentication]

    def get_referer(self, request):
        return request.META.get('HTTP_REFERER')

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def handle_exception(self, exc):
        response = super(APIView, self).handle_exception(exc)
        if 'detail' in response.data and \
                str(response.status_code).startswith('4'):
            response.data['message'] = response.data['detail']
            del response.data['detail']
        return response

