from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import str as text_type

from io import BytesIO
from urllib.parse import urljoin

from pyramid.request import Request as PyramidRequest
from pyramid.testing import DummySession
from requests import Request as RequestsRequest
from webob.request import environ_from_url


__all__ = ['make_request']

def make_request(
        # requests' parameters
        method='GET',
        url='',
        GET=None,   # == params 
        POST=None,  # == data
        json=None,
        cookies=None,
        files=None,
        
        # our own parameters
        is_xhr=False,
    ):
    """
        Build a WebOb/PyramidRequest using (mostly) the parameters used to
        build a "requests" request.
    
        Straight from requests' doc:
            :param method: method for the new :class:`Request` object.
            :param url: URL for the new :class:`Request` object.
            :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
            :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
            :param json: (optional) json data to send in the body of the :class:`Request`.
            :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
            :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': ('filename', fileobj)}``) for multipart encoding upload.
        
        Plus:
            :param is_xhr: (optional) ``bool`` that determines whether this is an XHR.
    """
    url = urljoin('http://test.example.com/', url)
    
    request = RequestsRequest(
        method=method,
        url=url, 
        params=GET,
        data=POST,
        json=json,
        cookies=cookies,
        files=files,
    ).prepare()

    wsgi_env = environ_from_url(request.url)
    if is_xhr:
        wsgi_env['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
    
    wsgi_env.update({
        # Relevant CGI parameters
        'REQUEST_METHOD': ensure_native_string_type(request.method),
        'CONTENT_TYPE': ensure_native_string_type(request.headers.get('Content-Type', '')),
        'CONTENT_LENGTH': ensure_native_string_type(request.headers.get('Content-Length', '')),
        
        # FUTURE: this could use all of requests's headers to generate HTTP_* parameters
        'HTTP_COOKIE': ensure_native_string_type(request.headers.get('Cookie', '')),
        
        # Relevant WSGI parameters
        'wsgi.input': BytesIO(ensure_bytes(request.body)),
    })
    
    pyramid_request = PyramidRequest(wsgi_env, charset='utf-8')
    pyramid_request.session = DummySession()
    
    # Trigger parsing
    pyramid_request.body
    return pyramid_request

def ensure_bytes(str_or_bytes):
    if isinstance(str_or_bytes, text_type):
        return str_or_bytes.encode('utf-8')
    return str_or_bytes

def ensure_native_string_type(text_or_bytes):
    import sys
    PY3 = sys.version_info[0] == 3
    if PY3:
        # PEP-3333, Py3: All WSGI environ values must be native (Unicode) strings
        if isinstance(text_or_bytes, text_type):
            return text_or_bytes
        return text_or_bytes.decode('utf-8')
    else:
        # PEP-3333, Py2: All WSGI environ values must be native (Byte) strings in ISO-8859-1.
        if isinstance(text_or_bytes, text_type):
            return text_or_bytes.encode('latin-1')
        return text_or_bytes
