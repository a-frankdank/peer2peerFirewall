# concatenate_test.py

import timeit

domain = 'some_really_long_example.com'
lang = 'en'
path = 'some/really/long/path/'
iterations = 1000000


def meth_f():
    return f'http://{domain}/{lang}/{path}'


def meth_plus():
    return 'http://' + domain + '/' + lang + '/' + path


def meth_join():
    return ''.join(['http://', domain, '/', lang, '/', path])


def meth_form():
    return 'http://{0}/{1}/{2}'.format(domain, lang, path)


def meth_intp():
    return 'http://%s/%s/%s' % (domain, lang, path)


f = timeit.Timer(stmt="meth_f()", setup="from __main__ import meth_f")
plus = timeit.Timer(stmt="meth_plus()", setup="from __main__ import meth_plus")
join = timeit.Timer(stmt="meth_join()", setup="from __main__ import meth_join")
form = timeit.Timer(stmt="meth_form()", setup="from __main__ import meth_form")
intp = timeit.Timer(stmt="meth_intp()", setup="from __main__ import meth_intp")

f.val = f.timeit(iterations)
plus.val = plus.timeit(iterations)
join.val = join.timeit(iterations)
form.val = form.timeit(iterations)
intp.val = intp.timeit(iterations)

min_val = min([f.val, plus.val, join.val, form.val, intp.val])

print('f %0.12f (%0.2f%% as fast)' % (f.val, (100 * min_val / f.val), ))
print('plus %0.12f (%0.2f%% as fast)' % (plus.val, (100 * min_val / plus.val), ))
print('join %0.12f (%0.2f%% as fast)' % (join.val, (100 * min_val / join.val), ))
print('form %0.12f (%0.2f%% as fast)' % (form.val, (100 * min_val / form.val), ))
print('intp %0.12f (%0.2f%% as fast)' % (intp.val, (100 * min_val / intp.val), ))