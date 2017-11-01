from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vocables.models import Vocable, VocableStats
from vocables.serializers import VocableSerializer

__author__ = 'tkolter'


class VocableViewSet(viewsets.ModelViewSet):

    queryset = Vocable.objects.all()

    serializer_class = VocableSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        result = super(VocableViewSet, self).retrieve(request, *args, **kwargs)
        pk = kwargs['pk']
        VocableStats.objects.get(vocable__pk=pk).increment_seen()
        return result

    @list_route(methods=['post'], url_path='next')
    def next(self, request):
        queryset = self.get_queryset()
        queryset = queryset.order_by('vocablestats__seen_count')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'], url_path='solve')
    def solve(self, request, pk):
        vocable = self.get_object()
        data = request.data
        if data:
            solved = True
            for k, v in data.items():
                word = vocable.word
                if getattr(word, k) != v:
                    solved = False
                    break

            vocable.vocablestats.increment_tries()
            if solved:
                vocable.vocablestats.increment_solved()
            else:
                raise ValidationError('Vocable does not match.')

        serializer = self.get_serializer(vocable)
        return Response(serializer.data)
