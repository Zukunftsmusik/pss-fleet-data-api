from typing import Union

import pytest
from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from starlette.datastructures import URL
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.exception_handlers import handle_http_exception
from src.api.models.exceptions import ApiError


class RequestMock(Request):
    def __init__(self):
        pass

    @property
    def url(self) -> URL:
        return URL("https://example.com")

    @property
    def method(self) -> str:
        return "GET"


test_cases = [
    # status_code
    pytest.param(status.HTTP_405_METHOD_NOT_ALLOWED, id="405")
]


test_cases_raises = [
    # status_code, expected_exception
    pytest.param(status.HTTP_400_BAD_REQUEST, StarletteHTTPException, id="400"),
    pytest.param(status.HTTP_401_UNAUTHORIZED, StarletteHTTPException, id="401"),
    pytest.param(status.HTTP_403_FORBIDDEN, StarletteHTTPException, id="403"),
    pytest.param(status.HTTP_404_NOT_FOUND, StarletteHTTPException, id="404"),
    pytest.param(status.HTTP_409_CONFLICT, StarletteHTTPException, id="409"),
    pytest.param(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, StarletteHTTPException, id="415"),
    pytest.param(status.HTTP_422_UNPROCESSABLE_ENTITY, StarletteHTTPException, id="422"),
    pytest.param(status.HTTP_429_TOO_MANY_REQUESTS, StarletteHTTPException, id="429"),
    pytest.param(status.HTTP_500_INTERNAL_SERVER_ERROR, StarletteHTTPException, id="500"),
]
"""status_code, expected_exception"""


@pytest.mark.parametrize(["status_code"], test_cases)
async def test_handle_http_exception(status_code: int):
    exc = StarletteHTTPException(status_code)
    request = RequestMock()

    response = await handle_http_exception(request, exc)
    assert isinstance(response, ORJSONResponse)
    assert response.status_code == status_code


@pytest.mark.parametrize(["status_code", "expected_exception"], test_cases_raises)
async def test_handle_http_exception_raises(status_code: int, expected_exception: Union[StarletteHTTPException, ApiError]):
    exc = StarletteHTTPException(status_code)

    with pytest.raises(expected_exception):
        await handle_http_exception(None, exc)
