from django.db import models

from words.models import Word

__author__ = 'tkolter'


class Vocable(models.Model):

    word = models.ForeignKey(Word)
    translation = models.CharField(max_length=32)


class VocableStats(models.Model):

    vocable = models.OneToOneField(Vocable)

    seen_count = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    tries_count = models.IntegerField(default=0)

    def __str__(self):
        return "{seen_count}".format(seen_count=self.seen_count)

    def increment_seen(self):
        self.seen_count += 1
        self.save(update_fields=['seen_count'])

    def increment_solved(self):
        self.correct_count += 1
        self.save(update_fields=['correct_count'])

    def increment_tries(self):
        self.tries_count += 1
        self.save(update_fields=['tries_count'])

    @property
    def solved(self):
        return self.correct_count