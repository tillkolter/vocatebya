from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from vocables.models import Vocable
from vocables.test.utils import VocableTestMixin

__author__ = 'tkolter'


class ViewsTest(VocableTestMixin, APITestCase):

    def setUp(self):
        from rest_framework_jwt.serializers import jwt_payload_handler, \
            jwt_encode_handler
        User = get_user_model()
        super().setUp()
        self.user = User.objects.create(username="till")
        self.user.set_password("god123")
        self.user.save()
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

    def test_create_vocable(self):
        """
        Ensure we can create a vocable.
        """
        url = reverse('vocable-list')
        data = {
            'word': {
                'word': 'Liebe',
                'features': '',
                'type': 1
            },
            'translation': "любо́вь"
        }
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post(url, data, format='json',)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_vocable(self):
        vocable = self._create_vocable()
        url = reverse('vocable-detail', args=(vocable.pk,))

        data = {
            'word': {
                'word': 'Liebe',
                'features': '',
                'type': 1
            },
            'translation': "любо́вь"
        }

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        self.client.post(url, data, format='json')

        old_word = vocable.word.word
        vocable = Vocable.objects.get(pk=vocable.pk)
        self.assertNotEquals(old_word, vocable.word.word)
        self.assertEquals('Liebe', vocable.word.word)
