from django.apps import AppConfig

__author__ = 'tkolter'


class VocablesConfig(AppConfig):

    name = 'vocables'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import vocables.signals.handlers  # noqa
