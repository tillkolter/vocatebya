import random
from django.db.models.aggregates import Count

from vocables.models import Vocable, VocableStats, VocableTest, TestVocable


def generate_test(user):
    vocables = Vocable.objects.all()
    queryset = vocables.raw("""
        SELECT v.*, COALESCE(s.seen_count, 0) as seen_count FROM vocables_vocable v
        LEFT JOIN (
          SELECT * FROM vocables_vocablestats
          WHERE user_id = '{user}'
        ) s
        ON v.id = s.vocable_id
        ORDER BY seen_count;
    """.format(user=user.id))

    count = vocables.count()
    r = range(min(30, count))
    x = [i for i in r]
    random.shuffle(x)

    test = VocableTest.objects.create(user=user)
    e = enumerate(x)

    for pos, index in e:
        vocable = queryset[index]
        TestVocable.objects.create(vocable=vocable, test=test, position=pos)

    return test