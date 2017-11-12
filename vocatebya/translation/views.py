import json

from django.conf import settings
from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from yandex_dictionary import YandexDictionary

__author__ = 'tkolter'


class TranslationView(viewsets.ViewSet):

    def list(self, request):
        translate = YandexDictionary(settings.YANDEX_DICTIONARY_API_KEY)
        text = request.query_params.get('text')
        source_lang = request.query_params.get('source', 'de')
        target_lang = request.query_params.get('target', 're')
        lookup_str = translate.lookup(text, source_lang, target_lang)
        translation = json.loads(lookup_str)
        definitions = translation.pop('def')
        if definitions:
            results = []
            for definition in definitions:
                source_dict = dict(
                    flexion=definition['fl'],
                    pos=definition['pos'],
                    gen=definition['gen'],
                    text=text,
                )
                translations = definition['tr']
                translation_results = []
                for translation in translations:
                    translation_result = {}
                    examples = translation.get('ex')
                    if examples:
                        translation_result['examples'] = examples

                    meaning = translation.get('mean')
                    if meaning:
                        translation_result['meaning'] = meaning

                    target_gen = translation.get('gen')
                    if target_gen:
                        translation_result['gen'] = target_gen

                    target_synonym = translation.get('syn')
                    if target_synonym:
                        translation_result['synonym'] = target_synonym

                    translation_result['text'] = translation.get('text')
                    translation_result['pos'] = translation.get('pos')

                    translation_results.append(translation_result)

                results.append({
                    'source': source_dict,
                    'target': translation_results
                })

            return Response(results)
        else:
            raise APIException('Translation Error')
