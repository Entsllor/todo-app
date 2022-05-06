import re

from flask import Flask

FLASK_URL_PARAM_PATTERN = re.compile(r'<[^>]*>')


class Url(str):
    def __call__(self, *args, **kwargs):
        return self.format(*args, **kwargs)


class AppUrls(dict):
    def __getattr__(self, item):
        return self[item]


def get_name_of_url_param(url_param: str) -> str:
    """
    >>> get_name_of_url_param('<int:user_id>')
    'user_id'
    >>> get_name_of_url_param('<string:name>')
    'name'
    >>> get_name_of_url_param('<name>')
    'name'
    >>> get_name_of_url_param('string:name')
    'name'
    >>> get_name_of_url_param('name')
    'name'
    """
    url_param = url_param.removeprefix('<').removesuffix('>')
    return url_param.split(':')[-1]


def flask_url_string_to_format_string(url: str) -> str:
    """
    >>> flask_url_string_to_format_string('test/<int:test_id>/')
    'test/{test_id}/'
    >>> flask_url_string_to_format_string('test/<int:test_id>/<int:user_id>/')
    'test/{test_id}/{user_id}/'
    >>> flask_url_string_to_format_string('test/')
    'test/'
    """
    return FLASK_URL_PARAM_PATTERN.sub(
        lambda match: '{' + get_name_of_url_param(match.group()) + '}',
        string=url
    )


def get_urls(app: Flask) -> AppUrls:
    urls = {}
    for url_object in app.url_map.iter_rules():
        endpoint_name = url_object.endpoint.split('.')[-1]
        url = Url(flask_url_string_to_format_string(url_object.rule))
        urls[endpoint_name] = url
    return AppUrls(**urls)
