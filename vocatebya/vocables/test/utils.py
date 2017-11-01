from vocables.models import Vocable
from words.models import Word

__author__ = 'tkolter'


class VocableTestMixin:

    def _create_vocable(self, source='Hello', target='yada'):
        vocable = Vocable.objects.create(
            word=Word.objects.create(word=source, type=1),
            translation=target
        )
        return vocable
