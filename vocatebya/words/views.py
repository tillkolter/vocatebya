from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny

from words.models import Word


class WordViewSet(viewsets.GenericViewSet):

    queryset = Word.objects.all()

    @list_route(
        methods=['get'],
        url_path='types',
        permission_classes=[AllowAny, ]
    )
    def types(self, request):
        return JsonResponse(
            {name: type_id for type_id, name in Word.Type.CHOICES}
        )
