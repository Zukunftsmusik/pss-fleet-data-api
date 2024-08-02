import pytest
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.exception_handlers import handle_http_exception


test_cases = [
    # status_code, expected_exception
    pytest.param(400, id="400"),
    pytest.param(401, id="401"),
    pytest.param(403, id="403"),
    pytest.param(404, id="404"),
    pytest.param(409, id="409"),
    pytest.param(415, id="415"),
    pytest.param(422, id="422"),
    pytest.param(500, id="500"),
]
"""status_code, expected_exception"""


@pytest.mark.parametrize(["status_code"], test_cases)
async def test_handle_http_exception(status_code: int):
    exc = StarletteHTTPException(status_code)

    with pytest.raises(StarletteHTTPException):
        await handle_http_exception(None, exc)
