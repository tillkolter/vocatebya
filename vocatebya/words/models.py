from django.contrib.postgres.fields import JSONField
from django.db import models

__author__ = 'tkolter'


class Word(models.Model):

    class Type:
        NOUN = 1
        VERB = 2
        DETERMINER = 3
        CHOICES = (
            (NOUN, 'Noun'),
            (VERB, 'Verb'),
            (DETERMINER, 'Determiner'),
        )

        choices = list(sorted(CHOICES, key=lambda x: x[1]))

    type = models.SmallIntegerField(choices=Type.choices)

    word = models.CharField(max_length=64)
    features = JSONField(null=True)
