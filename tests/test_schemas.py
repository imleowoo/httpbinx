"""Schema tests."""

import warnings

from pydantic import PydanticDeprecatedSince20

from httpbinx.schemas import RequestInfo


def test_request_info_properties_do_not_use_deprecated_pydantic_schema_api():
    with warnings.catch_warnings():
        warnings.simplefilter('error', PydanticDeprecatedSince20)
        properties = RequestInfo.get_properties()

    assert properties == (
        'url',
        'args',
        'headers',
        'origin',
        'form',
        'data',
        'files',
        'json',
        'method',
        'extras',
    )
