from rest_framework.exceptions import APIException

__author__ = 'tkolter'


class VocableExistsError(APIException):
    """ If the vocable to be created exists already """

    status_code = 422
    default_detail = 'Vocable exists already.'
