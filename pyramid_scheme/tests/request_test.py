from __future__ import absolute_import, division, print_function, unicode_literals

from io import BytesIO
from pyramid.testing import DummySession
import unittest

from ..request import make_request
from pyexpect import expect

class MakeRequestTest(unittest.TestCase):
    def test_can_set_request_method(self):
        expect(make_request(method='post').method) == 'POST'
        expect(make_request(method='put').method) == 'PUT'
        expect(make_request(method='get').method) == 'GET'
    
    def test_can_set_post_parameters(self):
        request = make_request(method='post', POST=dict(foo='bar'))
        expect(dict(request.POST)) == dict(foo='bar')
    
    def test_can_set_get_parameters(self):
        request = make_request(method='post', GET=dict(foo='bar'))
        expect(dict(request.GET)) == dict(foo='bar')
    
    def test_can_make_json_requests(self):
        request = make_request(method='post', json=dict(foo='bar'))
        expect(request.content_type) == 'application/json'
        expect(dict(request.json_body)) == dict(foo='bar')
    
    def test_has_sensible_default_url(self):
        request = make_request()
        expect(request.path_url) == 'http://test.example.com/'
    
    def test_can_override_default_url(self):
        request = make_request(url="http://fnord.example.com/foo")
        expect(request.host_url) == 'http://fnord.example.com'
        expect(request.path_url) == 'http://fnord.example.com/foo'
    
    def test_can_override_parts_of_default_url(self):
        request = make_request(url="/foo/bar")
        expect(request.path_url) == 'http://test.example.com/foo/bar'
    
    def test_can_make_xhrs(self):
        expect(make_request(method='post').is_xhr) == False
        expect(make_request(method='post', is_xhr=True).is_xhr) == True
    
    def test_can_set_content_length(self):
        expect(make_request().content_length) == None
        expect(make_request(POST=dict(fnord=23)).content_length) == 8
    
    def test_can_set_cookies(self):
        expect(make_request().cookies) == dict()
        expect(make_request(cookies=dict(fnord='foo')).cookies) == dict(fnord='foo')
    
    def test_can_create_multipart_request_for_file_upload(self):
        fake_file = BytesIO(b'foobar')
        request = make_request(method='post', files=dict(foo=fake_file))
        
        expect(request.content_type) == 'multipart/form-data'
        
        expect(list(request.POST.keys())) == ['foo']
        foo = dict(request.POST)['foo']
        expect(foo.file.read()) == b'foobar'

    def test_can_create_session(self):
        expect(make_request(method='post').session).isinstance(DummySession)
