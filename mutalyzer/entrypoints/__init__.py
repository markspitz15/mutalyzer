"""
Entry points to Mutalyzer.
"""


from __future__ import unicode_literals

import locale
import sys


class _ReverseProxied(object):
    """
    Wrap the application in this middleware and configure the front-end server
    to add these headers, to let you quietly bind this to a URL other than `/`
    and to an HTTP scheme that is different than what is used locally.

    Example for nginx::

        location /myprefix {
            proxy_pass http://192.168.0.1:5001;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Scheme $scheme;
            proxy_set_header X-Script-Name /myprefix;
        }

    `Flask Snippet <http://flask.pocoo.org/snippets/35/>`_ from Peter Hansen.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, *args, **kwargs):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme

        remote_address = environ.get('HTTP_X_FORWARDED_FOR', '')
        if remote_address:
            environ['REMOTE_ADDR'] = remote_address
        return self.app(environ, *args, **kwargs)


def _cli_string(argument):
    """
    Decode a command line argument byte string to unicode using our best
    guess for the encoding (noop on unicode strings).
    """
    encoding = sys.stdin.encoding or locale.getpreferredencoding()

    if isinstance(argument, unicode):
        return argument
    return unicode(argument, encoding=encoding)
