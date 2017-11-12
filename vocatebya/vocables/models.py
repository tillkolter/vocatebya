from django.contrib.auth import get_user_model
from django.db import models

from words.models import Word

__author__ = 'tkolter'


User = get_user_model()

class VocableManager(models.Manager):

    def next_vocable(self, pk):
        vocable = Vocable.objects.get(vocable__pk=pk)
        vocable.increment_seen()
        return vocable


class Vocable(models.Model):

    objects = VocableManager()

    word = models.ForeignKey(Word)
    translation = models.CharField(max_length=32)


class VocableStats(models.Model):

    user = models.ForeignKey(User)
    vocable = models.ForeignKey(Vocable, related_name='stats')

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


class TimeStampsMixin:

    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)


class VocableTest(TimeStampsMixin, models.Model):
    pass


class VocableTestStats(models.Model):

    user = models.ForeignKey(User, related_name='tests')
    test = models.ForeignKey(VocableTest, related_name='stats')

    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    is_solved = models.BooleanField(default=False)

    # @property
    # def position(self):
    #     self.Vocable


class TestVocable(models.Model):

    test = models.ForeignKey(VocableTest, related_name='vocables')
    vocable = models.ForeignKey(Vocable, related_name='tests')
    position = models.IntegerField()

    class Meta:
        index_together = ('test', 'position', 'vocable')


class VocableTestAnswer(TimeStampsMixin, models.Model):

    user = models.ForeignKey(User, related_name='answers')
    vocable = models.ForeignKey(TestVocable, related_name='answers')

    solution = models.TextField()
    is_correct = models.BooleanField(default=False)
