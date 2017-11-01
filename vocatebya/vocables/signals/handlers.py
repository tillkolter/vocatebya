from django.db.models.signals import post_save
from django.dispatch import receiver

from vocables.models import VocableStats, Vocable

__author__ = 'tkolter'


@receiver(post_save, sender=Vocable)
def vocable_post_save(sender, **kwargs):
    """
    Handles Vocable post save signals

    * creates VocableStats object on Vocable creation

    :param sender:
    :param kwargs:
    :return:
    """
    instance = kwargs.get('instance')
    created = kwargs.get('created', False)
    if instance and created:
        stats = VocableStats.objects.create(vocable=instance)
        print(stats)