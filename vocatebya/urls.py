from __future__ import unicode_literals

from django.conf import settings
from django.urls import reverse_lazy
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import SimpleRouter

from translation.views import TranslationView
from users.views import UserViewSet
from vocables.views import VocableViewSet, VocableTestViewSet, VocableAnswerView
from words.views import WordViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'vocable', VocableViewSet, base_name='vocable')
router.register(r'word', WordViewSet, base_name='word')
router.register(r'vocable-test', VocableTestViewSet, base_name='vocable_test')
router.register(r'vocable-answer', VocableAnswerView, base_name='vocable_answer')
router.register(r'translate', TranslationView, base_name='translate')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^api/v1/', include('authentication.urls')),
    url(r'^api/v1/', include(router.urls)),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    url(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
