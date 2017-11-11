import random

from vocables.models import Vocable, VocableStats, VocableTest, TestVocable


def generate_test():
    queryset = Vocable.objects.all()
    queryset = queryset.order_by('vocablestats__seen_count')

    count = queryset.count()
    r = range(min(30, count))
    x = [i for i in r]
    random.shuffle(x)

    test = VocableTest.objects.create()
    e = enumerate(x)
    print(e)
    for pos, index in e:
        print('pos {}, index {}'.format(pos, index))
        vocable = queryset[index]
        TestVocable.objects.create(vocable=vocable, test=test, position=pos)
