from rest_framework import serializers

from words.models import Word

__author__ = 'tkolter'


class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        fields = ('word', 'features', 'type', )
