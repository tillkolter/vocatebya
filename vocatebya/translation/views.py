import json

from django.conf import settings
from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from yandex_translate import YandexTranslate

from yandex_dictionary import YandexDictionary, YandexDictionaryException

__author__ = 'tkolter'


class TranslationView(viewsets.ViewSet):

    def list(self, request):
        text = request.query_params.get('text')
        source_lang = request.query_params.get('source', 'de')
        target_lang = request.query_params.get('target', 'ru')

        words = text.split()
        results = []
        if len(words) > 1:
            translator = YandexTranslate(settings.YANDEX_TRANSLATE_API_KEY)
            lang = '{}-{}'.format(source_lang, target_lang)
            translation = translator.translate(text, lang)
            result_code = translation['code']
            if result_code == 200:
                results.append(
                    {
                        'source': {
                            'text': text
                        },
                        'translations': [
                            {'text': translation['text']}
                        ]
                    }
                )
            else:
                exception = APIException('Translation Error')
                exception.status_code = result_code
                raise exception
        else:
            try:
                yandex_dictionary_key = settings.YANDEX_DICTIONARY_API_KEY
                translator = YandexDictionary(yandex_dictionary_key)
                translation = translator.lookup(text, source_lang, target_lang)
                definitions = translation.pop('def')
                if definitions:

                    for definition in definitions:
                        source_dict = dict(
                            ipa=definition['ts'],
                            pos=definition['pos'],
                            text=text,
                        )
                        flexion = definition.get('fl')
                        if flexion:
                            source_dict['flexion'] = flexion

                        genus = definition.get('gen')
                        if genus:
                            source_dict['genus'] = genus

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
                                translation_result['genus'] = target_gen

                            target_synonyms = translation.get('syn')
                            if target_synonyms:
                                translation_result['synonyms'] = target_synonyms

                            translation_result['text'] = translation.get('text')
                            translation_result['pos'] = translation.get('pos')

                            translation_results.append(translation_result)

                        results.append({
                            'source': source_dict,
                            'translations': translation_results
                        })

            except YandexDictionaryException as e:
                api_exception = APIException(e.args[0])
                api_exception.status_code = e.status_code
                raise api_exception

        return Response(results)
