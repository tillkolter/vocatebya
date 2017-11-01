from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_jwt.serializers import jwt_payload_handler, \
    jwt_encode_handler

from vocables.models import Vocable, VocableStats
from words.models import Word

__author__ = 'tkolter'


User = get_user_model()

from configurations import importer
importer.install()


class ModelTest(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username="till")
        self.user.set_password("god123")
        self.user.save()
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

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
        response = self.client.post(
            url,
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vocable_model_creates_stats(self):
        vocable = Vocable.objects.create(
            word=Word.objects.create(word='Hello', type=1),
            translation='yada'
        )
        self.assertIsNotNone(VocableStats.objects.get(vocable=vocable))
