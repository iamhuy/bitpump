# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import traceback

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication

from common.config import default_logger
from common import exceptions


class BaseApiView(APIView):
    InvalidInputException = exceptions.InputIsInvalidException
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    http_get_serializer_class = None
    serializer_class = None

    def get_view_name(self):
        return self.__class__.__name__

    def handle_exception(self, exc):
        error_message = traceback.format_exc()
        msg = 'API error: %s. GET: %s, POST: %s -> Error: %s.'
        msg %= (self.get_view_name(),
                repr(self.request.GET).decode('utf-8'),
                repr(self.request.data).decode('utf-8'),
                error_message)
        default_logger.error(msg)
        return super(BaseApiView, self).handle_exception(exc)

    def get(self, request, *args, **kwargs):
        if self.http_get_serializer_class is None:
            return self.get_valid(None)

        serializer = self.http_get_serializer_class(data=request.GET)

        if serializer.is_valid():
            return self.get_valid(serializer)
        else:
            return self.input_invalid(serializer)

    def get_valid(self, serializer):
        return self.reply()

    def post(self, request, *args, **kwargs):
        if self.serializer_class is None:
            return self.post_valid(None)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return self.post_valid(serializer)
        else:
            return self.input_invalid(serializer)

    def post_valid(self, serializer):
        return self.reply()

    @staticmethod
    def generate_validation_error(serializer):
        try:
            non_field_errors = serializer.errors['non_field_errors']
            return non_field_errors[0]
        except KeyError:
            pass

        error_msg = []
        for k, v in serializer.errors.iteritems():
            error_msg.append('%s:%s' % (k, v[0]))

        return ', '.join(error_msg)

    def input_invalid(self, serializer):
        error_msg = self.generate_validation_error(serializer)
        raise self.InvalidInputException(error_msg)

    def reply(self, dict_data=None, log_params=True):
        """
        This method shall only be called by success replies, all failure replies shall be handled by exceptions
        :param dict_data:
        :param log_params:
        :return:
        """
        if dict_data is None:
            dict_data = {'error': 0}
        else:
            dict_data['error'] = 0

        msg = 'API: %s. GET: %s, POST: %s -> Reply: %s.'
        if log_params:
            msg %= (self.get_view_name(),
                    repr(self.request.GET).decode('utf-8'),
                    repr(self.request.data).decode('utf-8'),
                    dict_data)
        else:
            msg %= (self.get_view_name(),
                    repr(self.request.GET).decode('utf-8'),
                    repr(self.request.data).decode('utf-8'),
                    '')
        default_logger.info(msg)

        return Response(dict_data)
