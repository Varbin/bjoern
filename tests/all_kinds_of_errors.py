#!/usr/bin/env python
from _background_server import BackgroundBjoern

import sys
import traceback

try:
    from http import client as httplib
except ImportError:  # Py 2
    import httplib

def valid(environ, start_response):
    start_response('200 ok', [('Header', 'Value')])
    return [b'yo']


def test_valid():
    with BackgroundBjoern(valid, 'localhost', 8000):
        h = httplib.HTTPConnection('localhost', 8000)
        h.request("GET", "/")
        response = h.getresponse()
        assert response.status == 200
        assert response.read() == b'yo'

def invalid_header_type(environ, start_response):
    start_response('200 ok', None)
    return [b'yo']

def test_invalid_header_type():
    with BackgroundBjoern(invalid_header_type, 'localhost', 8000):
        h = httplib.HTTPConnection('localhost', 8000)
        h.request("GET", "/")
        response = h.getresponse()
        assert response.status == 500
        assert response.read() != b'yo'

def invalid_header_tuple1(environ, start_response):
    start_response('200 ok', [()])
    return [b'yo']

def test_invalid_header_tuple1():
    with BackgroundBjoern(invalid_header_tuple1, 'localhost', 8000):
        h = httplib.HTTPConnection('localhost', 8000)
        h.request("GET", "/")
        response = h.getresponse()
        assert response.status == 500
        assert response.read() != b'yo'

def invalid_header_tuple2(environ, start_response):
    start_response('200 ok', [('a', 'b', 'c')])
    return [b'yo']

def test_invalid_header_tuple2():
    with BackgroundBjoern(invalid_header_tuple2, 'localhost', 8000):
        h = httplib.HTTPConnection('localhost', 8000)
        h.request("GET", "/")
        response = h.getresponse()
        assert response.status == 500
        assert response.read() != b'yo'

def invalid_header_tuple3(environ, start_response):
    start_response('200 ok', [('a',)])
    return [b'yo']

def test_invalid_header_tuple3():
    with BackgroundBjoern(invalid_header_tuple3, 'localhost', 8000):
        h = httplib.HTTPConnection('localhost', 8000)
        h.request("GET", "/")
        response = h.getresponse()
        assert response.status == 500
        assert response.read() != b'yo'

def invalid_header_tuple_item(environ, start_response):
    start_response('200 ok', (object(), object()))
    return [b'yo']
    
def test_invalid_header_tuple_item():
    with BackgroundBjoern(invalid_header_tuple_item, 'localhost', 8000):
        h = httplib.HTTPConnection('localhost', 8000)
        h.request("GET", "/")
        response = h.getresponse()
        assert response.status == 500
        assert response.read() != b'yo'

def invalid_response_type(environ, start_response):
    start_response('200 ok', [('Header', 'Value')])
    return None
    
def test_invalid_response_type():
    with BackgroundBjoern(invalid_response_type, 'localhost', 8000):
        h = httplib.HTTPConnection('localhost', 8000)
        h.request("GET", "/")
        response = h.getresponse()
        assert response.status == 500

def invalid_response_type_py3(environ, start_response):
    start_response('200 ok', [('Header', 'Value')])
    return ['yo']

def test_invalid_response_type_py3():
    with BackgroundBjoern(invalid_response_type_py3, 'localhost', 8000):
        h = httplib.HTTPConnection('localhost', 8000)
        h.request("GET", "/")
        response = h.getresponse()
        if sys.version_info[0] == 2:
            assert response.status == 200
            assert response.read() == 'yo'
        else:
            assert response.status == 500

if __name__ == "__main__":
    import __main__
    for i in dir(__main__):
        if i.startswith('test_'):
            print(i)  # For Py2 and Py3
            try:
                eval(i)()
            except Exception as e:
                print("- Failure:")
                traceback.print_exc()
            else:
                print("- Success")
