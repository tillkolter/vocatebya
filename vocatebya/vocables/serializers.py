from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError

from vocables.exceptions import VocableExistsError
from vocables.models import Vocable, VocableStats, VocableTest, TestVocable, \
    VocableTestAnswer
from words.models import Word
from words.serializers import WordSerializer

__author__ = 'tkolter'


class VocableStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = VocableStats
        fields = ('seen_count', 'tries_count', 'correct_count', )


class VocableSerializer(serializers.ModelSerializer):

    word = WordSerializer()
    stats = VocableStatsSerializer(read_only=True, source='vocablestats')

    class Meta:
        model = Vocable
        fields = ('id', 'word', 'translation', 'stats', )

    def update(self, instance, validated_data):
        word_data = validated_data.pop('word', None)
        vocable_data = dict(**validated_data)
        if word_data is not None:
            word = word_data.pop('word')
            word_obj, word_created = Word.objects.get_or_create(
                word=word,
                defaults=word_data
            )
            # if the word object exists already, iterate over the data items
            # and update the object
            if not word_created:
                for key, value in word_data.items():
                    setattr(word_obj, key, value)
                word_obj.save(update_fields=word_data.keys())

            vocable, vocable_created = Vocable.objects.get_or_create(
                word=word_obj,
                defaults=vocable_data
            )
            # if the vocable exists already, iterate over the data items
            # and update the object
            if not vocable_created:
                for key, value in vocable_data.items():
                    setattr(vocable, key, value)
                vocable.save(update_fields=vocable_data.keys())
            return vocable
        else:
            raise ParseError

    def create(self, validated_data):
        word_data = validated_data.pop('word', None)
        vocable_data = dict(**validated_data)
        if word_data is not None:
            word = word_data.pop('word')
            word_obj, _ = Word.objects.get_or_create(
                word=word,
                defaults=word_data
            )
            vocable, vocable_created = Vocable.objects.get_or_create(
                word=word_obj,
                defaults=vocable_data
            )
            if not vocable_created:
                raise VocableExistsError
            return vocable
        else:
                raise ParseError


class TestVocableSerializer(serializers.ModelSerializer):

    position = serializers.IntegerField(read_only=True)
    vocable = VocableSerializer(read_only=True)

    class Meta:
        model = TestVocable
        fields = ('id', 'position', 'test', 'vocable', )


class VocableTestSerializer(serializers.ModelSerializer):

    next_vocable = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = VocableTest
        fields = ('id', 'next_vocable', 'count', )

    def get_next_vocable(self, instance):
        qs = TestVocable.objects.filter(test=instance, answers=None)
        qs = qs.order_by('position')

        if qs:
            return TestVocableSerializer(qs[0]).data

    def get_count(self, instance):
        return TestVocable.objects.filter(test=instance).count()


class VocableAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = VocableTestAnswer
        fields = ('vocable', )
    #
    # def validate_user(self, value):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         return user.pk

    # def validate_vocable(self, pk):
    #     try:
    #         return TestVocable.objects.get(pk=pk)
    #     except TestVocable.DoesNotExist:
    #         raise ValidationError('Test vocable does not exist')
