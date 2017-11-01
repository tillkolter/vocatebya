from django.contrib.auth import get_user_model
from django.test import testcases

from vocables.models import VocableStats
from vocables.test.utils import VocableTestMixin

__author__ = 'tkolter'


User = get_user_model()


class ModelTest(VocableTestMixin, testcases.TestCase):

    def test_create_vocable_model_creates_stats(self):
        vocable = self._create_vocable()
        self.assertIsNotNone(VocableStats.objects.get(vocable=vocable))
