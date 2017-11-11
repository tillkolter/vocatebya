from rest_framework import serializers
from rest_framework.exceptions import ParseError

from vocables.exceptions import VocableExistsError
from vocables.models import Vocable, VocableStats, VocableTest, TestVocable
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

    vocables = TestVocableSerializer(many=True, read_only=True)

    class Meta:
        model = VocableTest
        fields = ('id', 'vocables', )

