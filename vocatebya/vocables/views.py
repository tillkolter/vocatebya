import random

from attrdict import AttrDict
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vocables.models import Vocable, VocableStats, VocableTest
from vocables.serializers import VocableSerializer, VocableTestSerializer

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

        l = min(30, queryset.count())
        rdm = random.randrange(l)

        if queryset:
            pk = queryset[rdm].pk
            VocableStats.objects.get(vocable__pk=pk).increment_seen()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'], url_path='solve')
    def solve(self, request, pk):
        vocable = self.get_object()

        data = request.data
        result_dict = {}
        if data:
            serializer = self.get_serializer(vocable)
            solved = True
            vocable_data = AttrDict(serializer.data)
            for k, v in data.items():
                if getattr(vocable_data, k) != v:
                    solved = False
                    break

            vocable.vocablestats.increment_tries()
            if solved:
                vocable.vocablestats.increment_solved()
                result_dict['status'] = 'solved'
                result_dict['vocable'] = vocable_data
            else:
                result_dict['status'] = 'failed'
        else:
            raise ValidationError('Payload must not be empty')

        return Response(result_dict)


class VocableTestViewSet(viewsets.ModelViewSet):

    queryset = VocableTest.objects.all()

    serializer_class = VocableTestSerializer
    permission_classes = (IsAuthenticated, )

    @list_route(methods=['post'], url_path='next')
    def next(self, request):
        VocableTest.objects.filter(finished_at=False)


