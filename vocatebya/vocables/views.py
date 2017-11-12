import json
import random

from attrdict import AttrDict
from rest_framework import viewsets, views
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vocables.models import Vocable, VocableStats, VocableTest, TestVocable, \
    VocableTestAnswer
from vocables.serializers import VocableSerializer, VocableTestSerializer, \
    TestVocableSerializer, VocableAnswerSerializer
from vocables.utils import generate_test

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
        user = request.user
        qs = self.get_queryset()
        unfinished_tests = (
            qs
            .filter(stats__user=user, stats__finished_at=None)
            .order_by('stats__started_at')
        )
        if unfinished_tests:
            next_test = unfinished_tests[0]
        elif qs:
            next_test = qs[0]
        else:
            next_test = generate_test()

        serializer = self.get_serializer(next_test)
        return Response(serializer.data)

    @detail_route(methods=['post'], url_path='next-vocable')
    def next_vocable(self, request, pk):
        qs = TestVocable.objects.filter(test__pk=pk, answers=None)
        qs = qs.order_by('position')
        if qs:
            test_vocable = qs[0]
            try:
                stats = test_vocable.vocable.stats.get(user=request.user)
            except VocableStats.DoesNotExist:
                stats = VocableStats.objects.create(
                    vocable=test_vocable.vocable,
                    user=request.user,
                )
            stats.increment_seen()
            return Response(TestVocableSerializer(test_vocable).data)


class VocableAnswerView(CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = VocableAnswerSerializer
    queryset = VocableTestAnswer.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        solution = data.pop('solution')
        vocable_id = data.get('vocable')
        test_vocable = TestVocable.objects.get(pk=vocable_id)

        result_dict = {}
        if data:
            vocable = test_vocable.vocable
            serializer = VocableSerializer(vocable)
            solved = True
            vocable_data = AttrDict(serializer.data)
            for k, v in solution.items():
                if getattr(vocable_data, k) != v:
                    solved = False
                    break

            stats = vocable.stats.filter(user=request.user)
            if not stats:
                stats = VocableStats.objects.create(
                    user=request.user,
                    vocable=vocable,
                )
            else:
                stats = stats[0]
            stats.increment_tries()
            answer, created = VocableTestAnswer.objects.get_or_create(
                user=request.user,
                vocable=test_vocable,
                defaults={
                    'is_correct': solved,
                    'solution': json.dumps(solution)
                }
            )
            if not created:
                answer.is_correct = solved
                answer.solution = json.dumps(solution)
                answer.save(update_fields=['is_correct', 'solution'])
            if solved:
                stats.increment_solved()
                result_dict['status'] = 'solved'
                result_dict['vocable'] = vocable_data
            else:
                result_dict['status'] = 'failed'
        else:
            raise ValidationError('Payload must not be empty')

        return Response(result_dict)